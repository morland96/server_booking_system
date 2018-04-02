import logging
from mongoengine import connect, StringField, Document, IntField, DateTimeField, ReferenceField
import time
import datetime
from .Auth import Auth

_logger = logging.getLogger("SBS_db")


def config_connect(logger, database_name="SBS"):
    global _logger
    _logger = logger  # type: logging.Logger
    connect(database_name)


class User(Document):
    """
    Class for binding users' information in database. It also provides API to get token for Authentication.
    TODO: make privilege usable.
    """
    allow_change = ["password"]
    username = StringField(required=True, max_length=200)
    password = StringField(required=True)
    privilege = IntField(required=False)

    def update_with_dict(self, user: dict):
        for key in user:
            if key in self.allow_change:
                self[key] = user[key]
        self.save()

    @staticmethod
    def login(username, password):
        """
        Login and get toekn
        :param username:
        :param password:
        :return: :class:`User <User>` object, string| None
        :rtype: User or None
        """
        users = User.objects(username=username, password=password)
        if users.count() == 0:
            _logger.debug(
                "Logging failed with username '{0},{1}'".format(username, password))
            return None
        elif users.count() == 1:
            user = users[0]
            user.token = (Auth.encode_auth_token(
                users[0].username, int(time.time()))).decode()
            return user
        else:
            try:
                raise UserError("Mutilple User found, please check database")
            except UserError as e:
                print(e)
            return None

    @staticmethod
    def get_user(username=None, uid=None):
        users = None
        if username is not None:
            users = User.objects(username=username)
        elif uid is not None:
            users = User.objects(id=uid)
        if users.count() > 0:
            return users[0]
        return None

    def get_dict(self):
        return {"username": self.username,
                "uid": str(self.id)
                }

    @staticmethod
    def verify_auth_token(token):
        playload = Auth.decode_auth_token(token)
        users = User.objects(username=playload['data']['username'])
        if len(users) > 0:
            return users[0]
        else:
            return None


class Reservation(Document):
    """ Class for bingding reservations' information in database
    """
    booktime = DateTimeField(default=datetime.now(), required=True)
    start_time = DateTimeField(default=datetime.now(), required=True)
    end_time = DateTimeField(default=datetime.now(), required=True)
    owner = ReferenceField()

    def reserve():
        pass


class UserError(Exception):
    """ Error to raise while search users' information in database 
    """
    pass
