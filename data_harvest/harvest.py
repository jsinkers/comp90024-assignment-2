import time

import tweepy
import couchdb as DB
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

import INFO


# load Statistical Area 2 (SA2) data for the greater melbourne region from the specified shapefile
def load_sa2_data():
    # TODO: change this to use a GeoJSON file already trimmed down
    # read the shape file cont
    sa2_data = "../data/1270055001_sa2_2016_aust_shape.zip"
    sa2_df = gpd.read_file(sa2_data)
    # filter to only include melbourne
    sa2_df = sa2_df[sa2_df['GCC_NAME16'] == 'Greater Melbourne']
    return sa2_df[['SA2_MAIN16', 'geometry']]


# return the SA2 main code for 2016 boundaries
def get_sa2_main16(coordinates):
    if coordinates is None:
        return None
    
    point = Point([coordinates['longitude'], coordinates['latitude']])
    # check if point falls in cell
    row_filter = sa2_main16_df.apply(lambda row: row['geometry'].contains(point) or row['geometry'].intersects(point), axis=1)
    filtered_rows = sa2_main16_df[row_filter]
    if (filtered_rows.size == 0):
        return None

    return filtered_rows['SA2_MAIN16'].iloc[0]


def get_tweet_coordinates(tweet_doc):
    """
    Given a tweet doc extract the tweet coordinates
    :param tweet: tweet in JSON format
    :return: dictionary of latitude, longitude
    """
    hasCoordinates = tweet_doc['coordinates']
    if hasCoordinates:
        return {"longitude": hasCoordinates['coordinates'][0], "latitude": hasCoordinates['coordinates'][1]}
    

# 1. filter coordinate 2. keep streaming
class tweet(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super(tweet, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        self.__userName = 'admin'
        self.__passWord = 'password'
        self.__url = 'http://' + self.__userName + ':' + self.__passWord + '@172.26.131.244:5984/'
        self.server = DB.Server(self.__url)
        self.db = self.server['twitter']
        self.analyser = SentimentIntensityAnalyzer()
        # load suburb data
        self.sa2_main16_df = sa2_df[['SA2_MAIN16', 'geometry']]


    def on_status(self, status):  # get the tweets from tweeter

        data = status._json
        print(data['id'])
        try:
            text = data['extended_tweet']['full_text']
        except:
            try:
                text = status.retweeted_status.extended_tweet['full_text']
            except:
                text = data['text']

        tweet_info = dict()
        tweet_info['tweet'] = data

        sentiment = self.analyser.polarity_scores(tweet['text'])
        tweet_info['sentiment'] = sentiment

        coords = get_tweet_coordinates(data)
        if coords is not None:
            tweet_info['sa2'] = get_sa2_main16(coords)

        self.store_tweets(tweet_info)

    def store_tweets(self, tweets):
        doc = tweets
        print(doc)
        self.db.save(doc)

    def on_error(self, status):
        if status == 420:
            print("Status code 420 received - too many api calls")
        else:
            return False


if __name__ == '__main__':
    bear_token = INFO.BEAR_TOKEN
    consumer_key = INFO.API_KEY
    consumer_secret = INFO.KEY_SECRET
    access_token = INFO.ACCESS_TOKEN
    access_secret = INFO.TOKEN_SECRET
    t = tweet(consumer_key, consumer_secret, access_token, access_secret)
    # coordinates for Melbourne based on a bounding box for the Greater Melbourne region
    coordinates = [144.33363404800002, -38.50298801599996, 145.8784120140001, -37.17509899299995]
    t.filter(locations=coordinates)
