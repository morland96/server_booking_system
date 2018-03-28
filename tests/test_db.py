import unittest
import logging
from backend.db import User, config_connect
logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s [%(levelname)s] %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )
logger = logging.getLogger("test")


class TestDB(unittest.TestCase):
    def setUp(self):
        global logger
        self.logger = logger  # type: logging.Logger
        config_connect(self.logger, "SBS")
        users = User.objects(username="unittest_account")
        if users.count() > 0:
            users.delete()
        user = User()
        user.username = "unittest_account"
        user.password = "password"
        user.save()
        self.test_user = user

    def test_add_user(self):
        self.logger.debug("saved user")
        users = User.objects(username="unittest_account")
        self.assertEqual(users[0].username, "unittest_account")
        self.assertEqual(users.count(), 1)

    def test_login(self):
        user = User.login("unittest_account", "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "unittest_account")
        self.logger.debug(user.id)

    def tearDown(self):
        self.test_user.delete()
