# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 12:57:30 2018

@author: sachi
"""
import re
import tweepy
import nltk
from tweepy import OAuthHandler
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud

stop_words = set(stopwords.words('english'))
cust_stop_words = set(['CO','Hi','$','I','-',"'",'...','It','n\'t','@',':','RT','the','is',',','https','a','an','and','to','#','(',')','!','.','``','\'\'',';','&','amp','\'s','The'])
finstop = set(list(stop_words)+list(cust_stop_words))
                       
class TwitterClient(object):
    def __init__(self):
        
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'XXXXXXXXXXXXX'
        consumer_secret = 'XX'
        access_token = 'XXX'
        access_token_secret = 'XX'
 
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
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            all_tweets = []
            last_id=-1
            while len(all_tweets) < count:
                print("loop : {}".format(len(all_tweets)))
                lcount = count - len(all_tweets)
                fetched_tweets = self.api.search(q = query, count = lcount, max_id=str(last_id-1))
                print("max_id : {}".format(last_id))
                if not fetched_tweets:
                    print("Breaking")
                    break
                all_tweets.extend(fetched_tweets)
                #print(dir(fetched_tweets))
                last_id=fetched_tweets[-1].id
             
            all_words = []
            for t in all_tweets:
                if t.lang == 'en':
                    all_words+=word_tokenize(t.text)
            
            return all_words
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
            
    def cleantweets(self,words):
        return [ word for word in words if word not in finstop]
    
    def mostcommanwords(self,all_words):
            
            freq = nltk.FreqDist(all_words)
            text = freq.most_common(50)
            print(text)
        
        
    def plotwordcloud(self,all_words):
              
            text = " ".join(all_words)
            import matplotlib.pyplot as plt
            # lower max_font_size
            wordcloud = WordCloud(max_font_size=80).generate(text)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.show()
        
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = 'trump', count = 100)
    
    tweets = api.cleantweets(tweets)
    api.mostcommanwords(tweets)
    api.plotwordcloud(tweets)
    

 
if __name__ == "__main__":
    # calling main function
    main()
