import json
import logging
import unittest
from datetime import datetime, timedelta
from app import db

import run

logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s [%(levelname)s] %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )
logger = logging.getLogger("test")

base_url = "http://127.0.0.1:5000/"

json_header = {"Content-Type": 'application/json'}
admin_json_header = {"Content-Type": 'application/json'}


class TestUserAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = logger
        run.flask_app.config['TESTING'] = True
        cls.app = run.flask_app.test_client()
        r = cls.app.delete("/api/v1.0/users/_test")
        cls.logger.debug("\ndelete _test account with %s " % r.status_code)

    def test_step1_register(self):
        r = self.app.post("/api/v1.0/users", headers=json_header,
                          data='{"username": "_test", "password": "password"}')
        self.assertEqual(r.status_code, 201)
        data = json.loads(r.data)
        self.assertEqual(data['username'], "_test")
        self.logger.debug(data)

    def test_step2_login(self):
        r = self.app.post("/api/v1.0/sessions", headers=json_header,
                          data='{"username": "_test", "password": "password"}')
        data = json.loads(r.data)
        self.assertEqual(r.status_code, 201)
        json_header['Authentication-Token'] = data['token']
        self.assertIsNotNone(data['token'])
        self.logger.debug("Get a token : %s" % data['token'])
        self.logger.debug(data)

    def test_step3_token(self):
        r = self.app.post("/api/v1.0/test/token",
                          headers=json_header)
        self.assertEqual(r.status_code, 201)
        self.logger.debug(r.data)

    def test_step4_update_user(self):
        r = self.app.put("/api/v1.0/users/_test",
                         headers=json_header, data='{"password":"111"}')
        self.assertEqual(r.status_code, 201)
        self.logger.debug(r.data)
        r = self.app.post("/api/v1.0/sessions", headers=json_header,
                          data='{"username": "_test", "password": "111"}')
        self.assertEqual(r.status_code, 201)

    def test_step5_delete_user(self):
        r = self.app.delete("/api/v1.0/users/_test", headers=json_header, data='{}')
        self.assertEqual(r.status_code, 204)


class TestReservationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = logger
        run.flask_app.config['TESTING'] = True
        cls.app = run.flask_app.test_client()
        cls.app.delete("/api/v1.0/users/test_user")
        cls.app.delete("/api/v1.0/users/test_admin")
        r = cls.app.post("/api/v1.0/users", headers=json_header,
                         data='{"username": "test_user", "password": "password"}')
        cls.logger.info("register user with status code %s" % r.status_code)
        admin = db.User()
        admin.username = "test_admin"
        admin.password = "password"
        admin.privilege = 1
        admin.save()

    def test_step1_get_token(self):
        # Get test_user token
        r = self.app.post("/api/v1.0/sessions", headers=json_header,
                          data='{"username": "test_user", "password": "password"}')
        data = json.loads(r.data)
        self.assertEqual(r.status_code, 201)
        self.assertIsNotNone(data['token'])
        json_header['Authentication-Token'] = data['token']
        # Get test_admin token
        r = self.app.post("/api/v1.0/sessions", headers=json_header,
                          data='{"username": "test_admin", "password": "password"}')
        data = json.loads(r.data)
        self.assertEqual(r.status_code, 201)
        self.assertIsNotNone(data['token'])
        admin_json_header['Authentication-Token'] = data['token']

    def test_step2_apply_reservations(self):
        r = self.app.post("/api/v1.0/reservations", headers=json_header,
                          data=json.dumps(
                              {'start_time': datetime.now().isoformat(),
                               'end_time': (datetime.now() + timedelta(days=1)).isoformat()}))
        self.assertEqual(r.status_code, 201)
        r = self.app.get("/api/v1.0/reservations", headers=json_header)
        data = json.loads(r.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['owner'], "test_user")
        self.logger.info(data)
        u_id = data[0]['id']
        r = self.app.post(f"/api/v1.0/reservations/{u_id}/allowed", headers=admin_json_header)
        self.assertEqual(r.status_code, 201)
        data = json.loads(r.data)
        self.assertEqual(data['allowed'], True)
