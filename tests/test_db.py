import datetime
import sys
import unittest
import logging
from app.db import Reservation, User

logging.basicConfig(level=logging.DEBUG,
                    stream=sys.stdout,
                    format='%(filename)s [%(levelname)s] %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )
logger = logging.getLogger("test")


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        u = User.objects(username="test_user", password="password")
        if len(u) > 0:
            u.delete()
        u = User()
        u.username = "test_user"
        u.password = "password"
        u.save()
        self.user = u
        now = datetime.datetime.now()
        r = Reservation.get_between(now, now + datetime.timedelta(days=1))
        r.delete()

    def test_step1_create_reservation(self):
        now = datetime.datetime.now()
        r = Reservation.reserve(self.user, now.isoformat(), (now + datetime.timedelta(days=1)).isoformat())
        self.reservation = r
        self.assertEqual(r.owner.username, "test_user")

    def test_step2_check_reservation(self):
        reservations = self.user.reservations
        User.objects(username="test_user")[0].delete()
        self.assertEqual(len(Reservation.objects()), 0)
