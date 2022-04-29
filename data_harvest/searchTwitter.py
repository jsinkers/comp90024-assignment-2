import time

import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import couchdb as DB

# rename this import to reference the key file used
import INFO as INFO
from sa2_data import *


# Twitter search API harvester using place filtering for Melbourne
class search(tweepy.API):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super(search, self).__init__()
        # CouchDB setup
        self.__userName = INFO.USERNAME
        self.__passWord = INFO.PASSWORD
        self.__url = f'http://{self.__userName}:{self.__passWord}@{INFO.IP_ADDR}:{INFO.PORT}/'
        print("Connecting to server...")
        self.server = DB.Server(self.__url)
        self.db = self.server['twitter_new']
        print("Connected to server")

        # Twitter API setup
        self.__auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.__auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.__auth, wait_on_rate_limit=True)

        # Geocoding and sentiment analysis setup
        self.sa2_main16_df = load_sa2_data()
        self.analyser = SentimentIntensityAnalyzer()
        print("Harvester setup complete")

    def search_tweet(self):
        # Search for tweets in Melbourne using 30 day search api
        query = 'place:melbourne'
        start = '202203290600'
        label = '30days'
        status = tweepy.Cursor(self.api.search_30_day,
                               label=label,
                               query=query,
                               fromDate=start,
                               maxResults=10
                               ).pages()
        for page in status:
            for tweet in page:
                tweet = tweet._json
                print(f"Tweet id: {tweet['id']}, date created: {tweet['created_at']}")
                tweet_info = self.prepare_tweet_document(tweet)
                self.store_tweets(tweet_info)
                time.sleep(1)

    def prepare_tweet_document(self, tweet):
        # extract the tweet text
        text = self.get_tweet_text(tweet)
        # set up the document for the database
        tweet_info = dict()
        tweet_info['_id'] = str(tweet['id'])
        tweet_info['type'] = 'search'
        tweet_info['tweet'] = tweet
        sentiment = self.analyser.polarity_scores(text)
        tweet_info['sentiment'] = sentiment
        coords = get_tweet_coordinates(tweet)
        if coords is not None:
            tweet_info['sa2'] = get_sa2_main16(coords, self.sa2_main16_df)
        return tweet_info

    def get_tweet_text(self, tweet):
        try:
            if 'extended_tweet' in tweet.keys():
                text = tweet['extended_tweet']['full_text']
            else:
                text = tweet['text']
        except (KeyError, AttributeError):
            print("Warning: Tweet KeyError - using default tweet text")
            text = tweet['text']
        return text

    def store_tweets(self, tweet):
        try:
            doc_id, doc_rev = self.db.save(tweet)
            print(f"Document stored in database: id: {doc_id}, rev: {doc_rev}")
        except DB.http.ResourceConflict:
            print(f"Document already present in database. Not updated")


if __name__ == '__main__':
    bear_token = INFO.BEAR_TOKEN
    consumer_key = INFO.API_KEY
    consumer_secret = INFO.KEY_SECRET
    access_token = INFO.ACCESS_TOKEN
    access_secret = INFO.TOKEN_SECRET

    t = search(consumer_key, consumer_secret, access_token, access_secret)
    print("Setup complete")
    # coordinates for Melbourne based on a bounding box for the Greater Melbourne region
    coordinates = [144.33363404800002, -38.50298801599996, 145.8784120140001, -37.17509899299995]

    print("Searching tweets...")
    t.search_tweet()
