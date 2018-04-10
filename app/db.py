import logging
from mongoengine import connect, StringField, Document, IntField, DateTimeField, ReferenceField, BooleanField, Q, \
    CASCADE, NULLIFY
import time
from datetime import datetime
from .Auth import Auth
from flask import current_app as app

time_format = '%Y-%m-%dT%H:%M:%S.%f'
_logger = logging.getLogger("SBS_db")


def config_connect(logger, database_name="SBS"):
    global _logger
    _logger = logger  # type: logging.Logger
    connect(database_name)


class User(Document):
    """
    Class for binding users' information in database. It also provides API to get token for Authentication.
    Attributes:
        reservations (User): reservations of this user
        privilege (Int): privilege of user
                        0 -- Simple user
                        1 -- Admin
    """
    allow_change = ["password"]
    username = StringField(required=True, max_length=200)
    password = StringField(required=True)
    privilege = IntField(required=False, default=0)

    @property
    def reservations(self):
        reservations = Reservation.objects(owner=self)
        return reservations

    def update_with_dict(self, user: dict):
        for key in user:
            if key in self.allow_change:
                self[key] = user[key]
        self.save()

    @staticmethod
    def login(username, password):
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
                "uid": str(self.id),
                "privilege": str(self.privilege)
                }

    @staticmethod
    def verify_auth_token(token):
        """
        Verify auth token and return owner of this token.
        Args:
            token (str): Input token

        Returns:
            user (User): Owner of this token.

        """
        playload = Auth.decode_auth_token(token)
        users = User.objects(username=playload['data']['username'])
        if len(users) > 0:
            return users[0]
        else:
            return None


class Reservation(Document):
    """ Class for binding reservations' information in database
    """
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
    book_time = DateTimeField(default=datetime.now(), required=True)
    start_time = DateTimeField(default=datetime.now(), required=True)
    end_time = DateTimeField(default=datetime.now(), required=True)
    detail = StringField(required=False)
    allowed = BooleanField(required=False)

    def get_dict(self):
        return {"id": str(self.id),
                "owner": self.owner.username,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat(),
                "allowed": self.allowed}

    @staticmethod
    def reserve(owner: User, start_time: str, end_time: str, detail: str = ""):
        """
        Create a reservation
        Args:
            owner (User): owner of this reservation
            start_time (datetime): start time of this reservation
            end_time (datetime): end time of this reservation, must later than start_time
            detail (str): Detail information

        Returns:
            reservation (Reservation): return this reservation, or None if can't create it

        """
        start_time = datetime.strptime(start_time, time_format)
        end_time = datetime.strptime(end_time, time_format)
        reservations = Reservation.get_between(start_time, end_time)
        if len(reservations) > 0:
            # Already has reservations
            return None
        else:
            reservation = Reservation()
            reservation.owner = owner
            reservation.start_time = start_time
            reservation.end_time = end_time
            reservation.detail = detail
            reservation.save()
            _logger.debug(
                f"Create a reservation by owner {owner.username}, from {start_time} to {end_time}")
            return reservation

    @staticmethod
    def get_between(start_time, end_time):
        """
        Return all reservations between start_time and end_time
        Args:
            start_time (datetime):
            end_time (datetime):

        Returns list(Reservation):

        """
        reservations = Reservation.objects(
            (Q(start_time__gte=start_time) & Q(start_time__lt=end_time))
            | Q(end_time__lte=end_time) & Q(end_time__gt=start_time))
        return reservations

    def accept(self):
        self.allowed = True
        self.save()

    def reject(self):
        self.allowed = 0


class UserError(Exception):
    """ Error to raise while search users' information in database. 
    """
    pass
