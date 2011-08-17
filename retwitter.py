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

    _auth=None
    @property
    def auth(self):
        if self._auth:
            return self._auth
        try:
            self.c_key = self.config['consumer_key']
            self.c_secret = self.config['consumer_secret']
            self._auth = tweepy.OAuthHandler(self.c_key, self.c_secret)

        except KeyError, e:
            if self.debug:
                print e
            print "You need to configure both the consumer key and secret"
            print "Try the --config-key and --config-secret options"
            sys.exit(1)

        except tweepy.TweepError, e:
            if self.debug:
                print e
            print "Authorization error, check that your app's key and secret are valid"
            sys.exit(1)
        return self._auth

    _api=None
    @property
    def api(self):
        if self._api:
            return self._api
        self._api = tweepy.API(self.auth)
        return self._api

    def load_user(self, account):
        try:
            a_key = self.config[account]['key']
            a_secret = self.config[account]['secret']
            self.auth.set_access_token(a_key, a_secret)

        except KeyError, e:
            if self.debug:
                print e
            if e.args[0] == 'account':
                print "User account not registered"
            else:
                print "Access token invalid, please register account again"
            sys.exit(1)

        except tweepy.TweepError, e:
            if self.debug:
                print e.msg
            print "Authorization error, check that your app's key and secret are valid"
            sys.exit(1)

    def get_list_timeline(self, listname, since_id=None):
        twitter_list = self.api.get_list(self.auth.username, listname)
        if since_id:
            return twitter_list.timeline(since_id=since_id)
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
        parser.add_option("-d", "--debug", action="store_true", default=False,
                          help="Debug")

        options, args = parser.parse_args()

        self.debug = options.debug

        if options.config_key and options.config_secret:
            self.config_app(options.config_key, options.config_secret)
            self.config.write()
            return 0

        if options.register:
            self.register()
            self.config.write()
            return 0

        if options.account and options.list and options.keyword:
            self.load_user(options.account.lower())
            self.work(options.account, options.list, options.keyword)
            self.config.write()
        return 0
            
    def work(self, account, listname, keyword):

        try:
            last_id = self.config[account][listname]
        except KeyError, e:
            if e.args[0] == account:
                self.config[account] = {}
            last_id = None

        tweets = self.get_list_timeline(listname, last_id)
        retweets = []
        for tweet in tweets:
            if tweet.text.lower().find(keyword.lower()) != -1:
                retweets.append(tweet)

        for tweet in reversed(retweets[:5]):
            if self.debug:
                print tweet.text
                continue
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
        username = self.auth.get_username().lower()
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

