import tweepy
import INFO
import couchdb as DB
import time


# 1. filter coordinate 2. keep streaming


class tweet(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super(tweet, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        # self.client = tweepy.StreamingClient()
        # self.id_holder = []
        self.__userName = 'admin'
        self.__passWord = 'password'
        self.__url = 'http://' + self.__userName + ':' + self.__passWord + '@172.26.131.244:5984/'
        self.server = DB.Server(self.__url)
        self.db = self.server['twitter']

    def on_status(self, status):  # get the tweets from tweeter

        data = status._json
        try:
            text = data['extended_tweet']['full_text']
        except:
            try:
                text = status.retweeted_status.extended_tweet['full_text']
            except:
                text = data['text']

        tweet_info = dict()
        tweet_info['tweetID'] = data["id"]
        tweet_info['in_reply_to_user_id'] = data['in_reply_to_user_id']
        tweet_info['text'] = text
        tweet_info['create_at'] = data['created_at']
        tweet_info['retweeted'] = data['retweeted']
        tweet_info['coordinate'] = data['coordinates']
        tweet_info['entities'] = data['entities']
        tweet_info['retweet_count'] = data['retweet_count']
        tweet_info['userID'] = data["user"]["id"]
        tweet_info['followers_count'] = data['user']['followers_count']
        tweet_info['lang'] = data['user']['lang']
        # print(tweet_info)
        self.store_tweets(tweet_info)

    def store_tweets(self, tweets):
        # self.db = self.server.create('test2')
        doc = tweets
        print(doc)
        self.db.save(doc)

    def on_error(self, status):
        if status == 420:
            print("Error 420 !")
        else:
            return False


if __name__ == '__main__':
    bear_token = INFO.BEAR_TOKEN
    consumer_key = INFO.API_KEY
    consumer_secret = INFO.KEY_SECRET
    access_token = INFO.ACCESS_TOKEN
    access_secret = INFO.TOKEN_SECRET
    t = tweet(consumer_key, consumer_secret, access_token, access_secret)
    keywords = ['scott morrison', 'scomo', 'prime minister', 'scummo', 'scumo', 'scotty from marketing',
                '@ScottMorrisonMP', '#auspol', '#ausvotes', '#ausvotes2022', '#ausvotes22', '#scottyfrommarketing',
                '#ScottyFromPhotoOps', '#ScottyTheGaslighter', '#ScottyThePathologicalLiar']
    coordinates = [144.33363404800002, -38.50298801599996, 145.8784120140001, -37.17509899299995]
    t.filter(track=keywords, locations=coordinates)
    #t.sample()
