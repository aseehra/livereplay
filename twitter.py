import base64
from datetime import datetime

import rauth
import requests.exceptions

from errors import *
from constants import *
from api_constants import *

class TwitterSession(object):
    def __init__(self):
        self._twitterAuth = rauth.OAuth1Service(
                name='livereplay',
                consumer_key = TWITTER_KEY,
                consumer_secret = TWITTER_SECRET,
                request_token_url = 'https://api.twitter.com/oauth/request_token',
                authorize_url = 'https://api.twitter.com/oauth/authorize',
                access_token_url = 'https://api.twitter.com/oauth/access_token',
                base_url = 'https://api.twitter.com/1.1/')
        params = {'oauth_callback': 'oob'}
        try:
            self._requestToken, self._requestTokenSecret = \
                    self._twitterAuth.get_request_token()
                    #self._twitterAuth.get_request_token(params = params)
        except requests.exceptions.ConnectionError:
            raise TwitterAuthenticationError('Count not connect to twitter.')

    def authenticate(self):
        authUrl = self._twitterAuth.get_authorize_url(self._requestToken)
        print('Authentication url:\n{}'.format(authUrl))
        pin = raw_input('Enter pin code: ')
        params = {'oauth_verifier': pin}
        try:
            self.session = self._twitterAuth.get_auth_session(
                    self._requestToken,
                    self._requestTokenSecret,
                    params = params)
        except requests.exceptions.ConnectionError:
            self.session = None
            raise TwitterAuthenticationError('Could not connect to twitter.')
        except KeyError:
            self.session = None
            raise TwitterAuthenticationError('Invalid verfication key.')

    def getHomeTimelineFragment(self, maxId = None, excludeReplies = True):
        if not self.session:
            raise TwitterAuthenticationError('Twitter not authenticated')
        params = {
                'count': 200,
                'exclude_replies': excludeReplies}
        if maxId:
            params['max_id'] = maxId
        try:
            result = self.session.get(
                    'statuses/home_timeline.json',
                    params = params)
        except requests.exceptions.RequestException:
            raise TwitterError('There was a problem connecting to Twitter')

        code = result.status_code
        if code != TWITTER_STATUS.OK:
            if code == TWITTER_STATUS.UNAUTHORIZED:
                raise TwitterAuthenticationError('LiveReplay not authorized')
            if code == TWITTER_STATUS.TOO_MANY_REQUESTS:
                raise TwitterError('Rate limit reached')
            else:
                raise TwitterError('Twitter error: {}'.format(code))
        return result.json()

    def getHomeTimeline(self, beginTime):
        ''' Gets full home timeline, through provided datetime '''
        timeline = []
        lastTime = datetime.utcnow()
        lastId = None
        while lastTime > beginTime:
            timeline.extend(self.getHomeTimelineFragment(lastId))
            lastTime = datetimeFromTwitterTimestamp(timeline[-1]['created_at'])
            lastId = timeline[-1]['id']
        return timeline

    def getHomeRequestsRemaining(self):
        if not self.session:
            raise TwitterAuthenticationError('Twitter not authenticated')
        params = { 'resources': 'statuses' }
        try:
            result = self.session.get(
                    'application/rate_limit_status.json')
        except requests.exceptions.RequestException:
            raise TwitterError('Could not connect to Twitter')

        code = result.status_code
        if code != TWITTER_STATUS.OK:
            if code == TWITTER_STATUS.UNAUTHORIZED:
                raise TwitterAuthenticationError(
                        'Could not authenticate to Twitter')
            else:
                raise TwitterError('Twitter error: {}'.format(code))
        remaining = \
                result.json()['resources']['statuses']['/statuses/home_timeline']['remaining']
        return remaining

def datetimeFromTwitterTimestamp(stringTime):
    return datetime.strptime(stringTime, '%a %b %d %H:%M:%S +0000 %Y')

def formatTweetForConsole(tweetJson):
    time = datetimeFromTwitterTimestamp(tweetJson['created_at'])
    text = tweetJson['text']
    username = tweetJson['user']['screen_name']
    formatStr = u'@{} [{}]\n{}'
    return formatStr.format(username, time.isoformat(' '), text).encode('utf-8')

if __name__ == '__main__':
    twitter = TwitterSession()
#    twitter.authenticate()
#    print twitter.getHomeRequestsRemaining()
    with open('testTweet.json', 'r') as fp:
        import json
        testJson = json.load(fp)
    print formatTweetForConsole(testJson[0])
