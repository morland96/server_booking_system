import pymongo
import logging

_client = pymongo.MongoClient()
_logger = logging.getLogger()
_collection = pymongo.mongo_client.database.Collection


def setDatabase(client, logger):
    global _client
    global _logger
    _client = client
    _logger = logger


class RootDB(object):
    """
        Base class of mongodb model. RootDB.client can be set from global namespace of db.py to initlize all model's connection
    """

    def __init__(self):
        self.sbs: _collection = _client.sbs
        self.logger = _logger
        self.logger.debug("init RootBD class")


class User(dict):

    def __init__(self):
        self.user: _collection = RootDB.sbs.user

    def _insert_user(self):
        self.user.insert()

    def show_client(self):
        print(self.db.sbs)
