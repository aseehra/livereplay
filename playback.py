from datetime import datetime
import json
import time

import twitter
from errors import *

class LiveReplay(object):
    def __init__(self, startTime):
        self.startTime = startTime
        self._twitter = twitter.TwitterSession()
        self.authenticated = False

    def fetchTweets(self):
        if not self.authenticated:
            self._twitter.authenticate()
            self.authenticated = True
        self.tweetsJson = self._twitter.getHomeTimeline(self.startTime)

    def saveTweets(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.tweetsJson, fp)

    def loadTweets(self, filename):
        with open(filename, 'r') as fp:
            self.tweetsJson = json.load(fp)

    def play(self):
        beginLocal = datetime.utcnow()
        for tweet in reversed(self.tweetsJson):
            tweetCreated = twitter.datetimeFromTwitterTimestamp(
                    tweet['created_at'])
#            if tweetCreated < self.startTime:
#                continue

            now = datetime.utcnow()
            localDelta = now - beginLocal
            effectiveTime = self.startTime + localDelta
            if effectiveTime < tweetCreated:
                sleepDelta = tweetCreated - effectiveTime
                time.sleep(sleepDelta.seconds)
            print(twitter.formatTweetForConsole(tweet))
            print

def datetimeFromUser(userStr):
    formatStr = '%y%m%d %H%M'
    return datetime.strptime(userStr, formatStr)

if __name__ == '__main__':
    startTimeStr = raw_input('Start time (UTC) [YYMMDD HHmm]: ')
    startTime = datetimeFromUser(startTimeStr)
    player = LiveReplay(startTime)

    print('Options: (1) Fetch & save (2) Replay saved.')
    option = int(input('Option? '))
    if option == 1:
        player.fetchTweets()
        player.saveTweets('/tmp/tweets.json')
        print len(player.tweetsJson)
    else:
        player.loadTweets('/tmp/tweets.json')
        raw_input('Ready? [Y]')
        player.play()
