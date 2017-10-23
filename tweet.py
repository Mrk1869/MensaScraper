#coding:utf-8

import urllib2
import twitter
import json
import datetime
import key

class Tweet:

    def __init__(self):
        self.api = twitter.Api(
            consumer_key = key.Twitter.consumer_key,
            consumer_secret = key.Twitter.consumer_secret,
            access_token_key = key.Twitter.access_token,
            access_token_secret = key.Twitter.access_token_secret,
        )
        d = datetime.datetime.today()
        self.today = str(d.month)+u"月"+str(d.day)+u"日 "

    def tweet(self, str):
        self.api.PostUpdate(str)
        print "Tweeted."

    def tweetMenu(self):
        url = "http://api.mrk1869.com/mensa/v1/"
        html = urllib2.urlopen(url).read()
        data = json.loads(html)
        res2 =  "MENU2: "+ data['menu2']['name'] + " " + data['menu2']['image']
        self.tweet(self.today+res2)
        res1 =  "MENU1: "+ data['menu1']['name'] + " " + data['menu1']['image']
        self.tweet(self.today+res1)


if __name__ == '__main__':
    tweet = Tweet()
    tweet.tweetMenu()
