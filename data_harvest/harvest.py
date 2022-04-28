import time
import tweepy
import couchdb as DB
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import geopandas as gpd
from shapely.geometry import Point
import INFO_1

# Twitter filter Stream API streamer using geolocation filtering for Melbourne
class tweet(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super(tweet, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        self.__userName = 'admin'
        self.__passWord = 'password'
        # TODO: username, password, IP address, and ports are ideally environment variables
        # self.__url = 'http://' + self.__userName + ':' + self.__passWord + '@172.26.131.244:5984/'
        self.__url = 'http://admin:password@localhost:5984/'
        print("Connecting to server...")
        self.server = DB.Server(self.__url)
        print("Connected to server")
        self.db = self.server['twitter_new']

        self.analyser = SentimentIntensityAnalyzer()
        # load suburb data
        self.sa2_main16_df = load_sa2_data()
        print("Harvester setup complete")

    def on_status(self, status):  # get the tweets from tweeter

        data = status._json
        print(f"Filtered tweet id: {data['id']}")

        # Extract the text from the tweet
        try:
            if 'extended_tweet' in data.keys():
                text = data['extended_tweet']['full_text']
            elif 'full_text' in status.retweeted_status.extended_tweet.keys():
                text = status.retweeted_status.extended_tweet['full_text']
            else:
                text = data['text']
        except (KeyError, AttributeError):
                print("Tweet KeyError - using default tweet text")
                text = data['text']

        # store the document in the database as a dictionary with keys {tweet, sentiment, sa2}
        tweet_info = dict()
        tweet_info['_id'] = str(data['id'])
        tweet_info['type'] = 'version_2'
        tweet_info['tweet'] = data
        sentiment = self.analyser.polarity_scores(text)
        tweet_info['sentiment'] = sentiment

        coords = get_tweet_coordinates(data)
        if coords is not None:
            tweet_info['sa2'] = get_sa2_main16(coords, self.sa2_main16_df)

        self.store_tweets(tweet_info)

    def store_tweets(self, tweets):
        try:
            doc_id, doc_rev = self.db.save(tweets)
            print(f"Document stored in database: id: {doc_id}, rev: {doc_rev}")
        except DB.http.ResourceConflict: 
            print(f"Document already present in database. Not updated")



# load Statistical Area 2 (SA2) data for the greater melbourne region from the specified shapefile
def load_sa2_data():
    # TODO: this could be modified to use a GeoJSON file and have a smaller data file. May not be worth it
    # TODO: ideally this would be set as an environment variable? Will leave up to you to decide
    # read the shape file
    sa2_data = "../data/1270055001_sa2_2016_aust_shape.zip"
    sa2_df = gpd.read_file(sa2_data)
    # filter to only include melbourne
    sa2_df = sa2_df[sa2_df['GCC_NAME16'] == 'Greater Melbourne']
    return sa2_df[['SA2_MAIN16', 'geometry']]


# return the SA2 main code for 2016 boundaries
def get_sa2_main16(coordinates, sa2_main16_df):
    if coordinates is None:
        return None

    point = Point([coordinates['longitude'], coordinates['latitude']])
    # TODO: this is inelegant and inefficient, but works. Refactor if you wish
    # check if point falls in the sa2 geometry
    row_filter = sa2_main16_df.apply(lambda row: row['geometry'].contains(point) or row['geometry'].intersects(point),
                                     axis=1)
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


if __name__ == '__main__':
    bear_token = INFO_1.BEAR_TOKEN
    consumer_key = INFO_1.API_KEY
    consumer_secret = INFO_1.KEY_SECRET
    access_token = INFO_1.ACCESS_TOKEN
    access_secret = INFO_1.TOKEN_SECRET

    t = tweet(consumer_key, consumer_secret, access_token, access_secret)
    print("Setup complete")
    # coordinates for Melbourne based on a bounding box for the Greater Melbourne region
    coordinates = [144.33363404800002, -38.50298801599996, 145.8784120140001, -37.17509899299995]

    print("Filtering tweets...")
    t.filter(locations=coordinates)
