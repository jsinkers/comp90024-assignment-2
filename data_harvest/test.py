import tweepy
import INFO
import couchdb as DB
import time


# 1. filter coordinate 2. keep streaming


class tweet(tweepy.StreamingClient):
    def __init__(self, token):
        super(tweet, self).__init__(token)
        self.client = tweepy.StreamingClient(bearer_token=token)

    def on_tweet(self, tweet):
        if tweet.geo != None:
            print(tweet.geo)


if __name__ == '__main__':

    bear = INFO.BEAR_TOKEN
    t = tweet(bear)
    rule = 'place:melbourne'
    t.add_rules(tweepy.StreamRule(rule))
    t.filter()
    t.get_rules()