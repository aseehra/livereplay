import unittest
from datetime import datetime

from playback import *

class TestPlaybackUtilities(unittest.TestCase):
    def testDatetimeFromUser(self):
        userStr = '131001 1535'
        startTime = datetimeFromUser(userStr)
        actual = datetime(2013, 10, 1, 15, 35)
        self.assertEquals(startTime, actual)
