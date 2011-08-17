#!/usr/bin/env python
import sys
import time
import tweepy
from optparse import OptionParser

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

def retweet():
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

def verify(auth):
    # 1285931
    redirect_url = auth.get_authorization_url()
    print "go to this url %s" % redirect_url
    verify_pin = raw_input('Type the pin: ')
    auth.set_access_token(verify_pin)
    # save auth.access_token.key
    # and  auth.access_token.secret

def main(args=[]):
    parser = OptionParser()
    parser.add_option("-r", "--register", action="store_false", default=False
                      help="Register your twitter account")
    parser.add_option("-a", "--account", type="string",
                      help="Run the bot for that account")
    parser.add_option("-l", "--list", type="string",
                      help="Retweet from this list")
    parser.add_option("-k", "--keyword", type="string",
                      help="Keyword that triggers the retweet")
    options, args = parser.parse_args()

    if options.register:
        verify()

if __name__ == '__main__':
    main(sys.argv[1:])

