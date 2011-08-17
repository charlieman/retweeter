#!/usr/bin/env python
import os
import sys
import time
import tweepy
from optparse import OptionParser
from configobj import ConfigObj

class App(object):
    def __init__(self):
        self.config_file = os.path.expanduser('~/.retweeter.ini')
        self.config = ConfigObj(self.config_file)

    def load_auth(self):
        try:
            self.c_key = self.config['consumer_key']
            self.c_secret = self.config['consumer_secret']
            self.auth = tweepy.OAuthHandler(self.c_key, self.c_secret)

        except KeyError, e:
            print "You need to configure both the consumer key and secret"
            print "Try the --config-key and --config-secret options"
            sys.exit(1)

        except tweepy.TweepError, e:
            print "Authorization error, check that your app's key and secret are valid"
            sys.exit(1)

    def load_user(self, account):
        try:
            a_key = self.config[account]['access_token_key']
            a_secret = self.config[accout]['access_token_secret']
            self.auth.set_access_token(a_key, a_secret)

        except KeyError, e:
            if e.args[0] == 'account':
                print "User account not registered"
            else:
                print "Access token invalid, please register account again"
            sys.exit(1)

        except tweepy.TweepError, e:
            print "Authorization error, check that your app's key and secret are valid"
            sys.exit(1)

    def get_list_timeline(self, listname):
        twitter_list = api.get_list(auth.username, listname)
        return twitter_list.timeline()

    def run(self, args):
        parser = OptionParser()
        parser.add_option("-r", "--register", action="store_true", default=False,
                          help="Register your twitter account")
        parser.add_option("-a", "--account", type="string",
                          help="Run the bot for that account")
        parser.add_option("-l", "--list", type="string",
                          help="Retweet from this list")
        parser.add_option("-k", "--keyword", type="string",
                          help="Keyword that triggers the retweet")
        parser.add_option("--config-key", type="string",
                          help="Configure application's consumer key")
        parser.add_option("--config-secret", type="string",
                          help="Configure application's consumer secret")

        options, args = parser.parse_args()

        if options.config_key and options.config_secret:
            self.config_app(options.config_key, options.config_secret)
            self.config.write()
            self.load_auth()
            return 0

        if options.register:
            self.load_auth()
            self.register()
            self.config.write()
            return 0

        if options.account and options.list and options.keyword:
            self.load_user(options.account)
            self.work(account, listname, keyword)
            self.config.write()
        return 0
            
    def work(self, account, listname, keyword):

        try:
            last_id = self.config[account][listname]
        except KeyError, e:
            last_id = None

        self.api = tweepy.API(self.auth)
        tweets = self.get_list_timeline(options.list)
        retweets = []
        for tweet in tweets:
            if tweet.text.lower().find(options.keyword) != -1:
                retweets.append(tweet)


        for tweet in reversed(retweets[:5]):
            tweepy.retweet(tweet.id)
            time.sleep(60)
        
        last_id = tweets[0].id
        self.config[account][listname] = last_id


    def register(self):
        # 1285931
        redirect_url = self.auth.get_authorization_url()
        print "Go to this url: %s" % redirect_url
        print "and grant access, it will return an access number"

        # TODO: do this in a loop to avoid empty pin
        verify_pin = raw_input('Type the pin: ')
        self.auth.get_access_token(verify_pin)
        username = self.auth.get_username()
        # TODO: check if username exist and ask if it's ok to overwrite
        self.config[username] = {}
        self.config[username]['key'] = self.auth.access_token.key
        self.config[username]['secret'] = self.auth.access_token.secret

    def config_app(self, consumer_key, consumer_secret):
        self.config['consumer_key'] = consumer_key
        self.config['consumer_secret'] = consumer_secret

if __name__ == '__main__':
    app = App()
    app.run(sys.argv[1:])

