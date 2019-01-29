'''
    Sentiment Analysis of tweets related to iPhoneX
    Author: Girija Godbole (NET ID: gsg160130)
'''

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import csv
from textblob.classifiers import NaiveBayesClassifier
import codecs


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from my twitter dev account.
        consumer_key = 'aPV5hG444p7uM5Vzf7Bim9rpy'
        consumer_secret = 'A7Z6LXA8cnd7IHCRg4YAYNtvOeL0xbxYx627MpteOh5kgA48L1'
        access_token = '171481117-HrCa6l4cJmxiKfHIHCE5by49B8O7rdwa6Cr4q4qO'
        access_token_secret = 'L4pnVZ8uAlHJ25YhsxhKkoxRRCZwNZnse1Usyd9nT89NC'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")



    def read_csv_training_data(self):
        '''
              Utility function to read the data txt file and get the text and labelled sentiments. We store these into the 'train' list.
        '''
        train = []
        with open('new_amazon.txt', 'rb') as csvfile:
            training_data = csv.reader(csvfile, delimiter="\t")
            for row in training_data:
                train.append((row[0], row[1],))
            return train


    def train(self):
        '''
              Utility function to train the Naive Bayes Model.
        '''
        rows = self.read_csv_training_data()
        print "Training the model. Please wait..."
        cl = NaiveBayesClassifier(rows)
        print "Our model is now trained!!"
        return cl

    def get_tweet_sentiment(self, tweet, trained_handle):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob.
        '''
        # using the classify function to classify our text
        sentiment = trained_handle.classify(tweet)
        return sentiment


    def get_tweets(self, trained_handle, query, count):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(lang= 'en', q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text, trained_handle)
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():

    # creating object of TwitterClient Class
    api = TwitterClient()
    #training the model
    trained_handle = api.train()
    # calling function to get tweets
    tweets = api.get_tweets(trained_handle, query='iphoneX', count=10)
    # # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == '1']
    # # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == '0']
    # # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))

    # # printing few positive tweets
    print("\n\nPositive tweets:")
    #
    for tweet in ptweets[:20]:
        print(tweet['text'])
    #
    # # printing few negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:20]:
        print(tweet['text'])


if __name__ == "__main__":
    # calling main function
    main()