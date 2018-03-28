import logging
from mongoengine import connect, StringField, Document

_logger = logging.getLogger("SBS_db")


def config_connect(logger, database_name="SBS"):
    global _logger
    _logger = logger  # type: logging.Logger
    connect(database_name)


class User(Document):
    username = StringField(required=True, max_length=200)
    password = StringField(required=True)

    def login(username, password):
        users = User.objects(username=username, password=password)
        if users.count() == 0:
            _logger.debug(f"Logging failed with username '{username}'")
            return None
        elif users.count() == 1:
            return users[0]
        else:
            try:
                raise UserError("Mutilple User found, please check database")
            except UserError as e:
                print(e)

    def get_user(username=None, uid=None):
        users = None
        if username is not None:
            users = User.objects(username=username)
        elif uid is not None:
            users = User.objects(uid=uid)
        if users.count() > 0:
            return users[0]
        return None


class UserError(Exception):
    pass
