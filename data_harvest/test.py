import tweepy
import INFO
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
        id_holder = []
        query = 'place:melbourne'
        start = '202203290600'
        label = '30days'
        status = tweepy.Cursor(self.api.search_30_day,
                label = label,
                query=query,
                fromDate= start,
                maxResults=10
                ).pages()

        for each in status:
            for tweet in each:
                tweet_info = dict()
                doc = tweet._json
                if doc['id'] not in id_holder:
                    id_holder.append(doc['id'])
                else:
                    print('exist')
            print(len(id_holder))

  
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
