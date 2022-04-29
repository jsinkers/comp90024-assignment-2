from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import geopandas as gpd
from shapely.geometry import Point
import couchdb as DB
import time


class search(tweepy.API):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super(search, self).__init__()
        self.__userName = 'admin'
        self.__passWord = 'password'
        self.__url = 'http://' + self.__userName + ':' + self.__passWord + '@172.26.131.244:5984/'
        print("Connecting to server...")
        '''
        self.server = DB.Server(self.__url)
        print("Connected to server")
        self.db = self.server['twitter_new']
        '''
        self.analyser = SentimentIntensityAnalyzer()
        self.__auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.__auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.__auth, wait_on_rate_limit=True)
        # self.sa2_main16_df = load_sa2_data()
        print("Harvester setup complete")

    def search_tweet(self):

        query = 'place:melbourne'
        start = '202203290600'
        label = '30days'
        status = self.api.search_30_day(label=label, query=query, fromDate=start, maxResults=10,
                                        )
        responses = tweepy.Paginator(status)
        return responses

    def doc(self):

        iter = 0
        id_holder = []
        while True:
            iter += 1
            new = 0
            repeated = 0
            print("{} search".format(iter))
            responses = self.search_tweet()
            for each in responses.method:
                tweet_info = dict()
                tweet = each._json
                if tweet['id'] not in id_holder:
                    new += 1
                    id_holder.append(tweet['id'])
                else:
                    repeated += 1
            print("{} search, {} new data, {} repeated data".format(iter, new, repeated))


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
    t.doc()
