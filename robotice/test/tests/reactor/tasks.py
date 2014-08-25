import os
import sys
import unittest

sys.path.append('/srv/robotice/service')

from utils import setup_app


class ReactorTestCase(unittest.TestCase):

    def setUp(self):
        self.config = setup_app('monitor')

    def test_commit_action(self):
        pass

if __name__ == '__main__':
    unittest.main()
