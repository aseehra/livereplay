class LiveReplayError(Exception):
    def __init__(self, msg):
        super(LiveReplayError, self).__init__(msg)
    def msg(self):
        return self.args[0]

class TwitterError(LiveReplayError):
    pass

class TwitterAuthenticationError(TwitterError):
    pass
