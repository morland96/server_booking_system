import unittest
import pymongo
import logging
from backend.db import setDatabase, User, RootDB
logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s [%(levelname)s] %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )
logger = logging.getLogger("test")


class TestDB(unittest.TestCase):
    def setUp(self):
        self.client = pymongo.MongoClient()
        setDatabase(self.client, logger)

    def testRootDB(self):
        RootDB()

    def testUser(self):
        user = User()
        user.show_client()
