import tweepy
import pandas as pd
import INFO


class tweet:

    def __init__(self, bear_token):
        self.client = tweepy.Client(bearer_token=bear_token)
        # self.id_holder = []

    def tweets_harvest(self):  # get the tweets from tweeter
        query = 'melbourne'
        # query = '(😃 OR 😡) 😬 -is:retweet'
        response = self.client.search_recent_tweets(query=query, max_results=100, until_id =1519550905217019907)
        temp = []
        #print(response)
        for each in response.data:
            print(each)
            temp.append(each.text)
        return temp

    def dataBaseConnection(self):
        pass

    def store_tweets(self, tweets):
        self.dataBaseConnection()
        pass


if __name__ == '__main__':
    bear_token = INFO.BEAR_TOKEN
    t = tweet(bear_token)
    t.tweets_harvest()
