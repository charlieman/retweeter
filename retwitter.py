#!/usr/bin/env python
import time
import tweepy

from config import consumer_key, consumer_secret, access_token_secret, access_token_key

username = 'AQPGLUG'
listname = 'miembros'

def findaqpglug(timeline):
    for tweet in timeline:
        if tweet.text.lower().find('aqpglug') != -1:
            yield tweet

def get_auth_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    return api, auth

def main():
    api, auth = get_auth_api()
    user = api.get_user(auth.username)
    members_list = api.get_list(user.screen_name, listname)
    retweets = []
    for tweet in members_list.timeline():
        retweets.append(tweet)
        #if tweet.text.lower().find('aqpglug') != -1:
        #    retweets.append(tweet)

    for tweet in retweets[:5]:
        print tweet.text
        #tweepy.retweet(tweet.id)
        #time.sleep(60)
        time.sleep(2)

if __name__ == '__main__':
    main()

