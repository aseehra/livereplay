import unittest
from datetime import datetime, timedelta
import json

from twitter import *
from errors import *

class TestTwitterExceptions(unittest.TestCase):
    def testExceptionMsg(self):
        msg = 'This is my message'
        exp = LiveReplayError(msg)
        self.assertEquals(exp.msg(), msg)

class TestTwitterUtilities(unittest.TestCase):
    def testDatetimeFromTwitterTimestamp(self):
        stamp = 'Wed Oct 09 17:19:48 +0000 2013'
        date = datetime(2013, 10, 9, 17, 19, 48)
        self.assertEquals(datetimeFromTwitterTimestamp(stamp), date)

    def testTwitterConsoleFormat(self):
        with open('testTweet.json', 'r') as fp:
            tweet = json.load(fp)
        print('\n' + formatTweetForConsole(tweet[0]) + '\n')

class TestTwitterFetchTimeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.twitter = TwitterSession()
        cls.twitter.authenticate()

    def testTimelineMaxTime(self):
        result = self.twitter.getHomeTimeline(datetime.max)
        self.assertEquals(len(result), 0)

    def testTimelineYesterday(self):
        now = datetime.utcnow()
        yesterday = now -  timedelta(days = 1)
        response = self.twitter.getHomeTimeline(yesterday)
        lastDate = datetimeFromTwitterTimestamp(response[-1]['created_at'])
        assert(lastDate <= yesterday)
