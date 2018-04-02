import unittest
import logging
import run
import json
logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s [%(levelname)s] %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )
logger = logging.getLogger("test")

base_url = "http://127.0.0.1:5000/"

json_headers = {"Content-Type": 'application/json'}


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.logger = logger
        run.flask_app.config['TESTING'] = True
        self.app = run.flask_app.test_client()
        r = self.app.delete("/api/v1.0/users/_test")
        self.logger.debug("\ndelete _test account with %s " % r.status_code)

    def test_step1_register(self):
        r = self.app.post("/api/v1.0/users", headers=json_headers,
                          data='{"username": "_test", "password": "password"}')
        self.assertEqual(r.status_code, 201)
        data = json.loads(r.data)
        self.assertEqual(data['username'], "_test")
        self.logger.debug(data)

    def test_step2_login(self):
        r = self.app.post("/api/v1.0/login", headers=json_headers,
                          data='{"username": "_test", "password": "password"}')
        data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        json_headers['Authentication-Token'] = data['token']
        self.assertIsNotNone(data['token'])
        self.logger.debug("Get a token : %s" % data['token'])
        self.logger.debug(data)

    def test_step3_token(self):
        r = self.app.post("/api/v1.0/test/token",
                          headers=json_headers)
        self.assertEqual(r.status_code, 200)
        self.logger.debug(r.data)

    def test_step4_update_user(self):
        r = self.app.put("/api/v1.0/users/_test",
                         headers=json_headers, data='{"password":"111"}')
        self.assertEqual(r.status_code, 200)
        self.logger.debug(r.date)
        r = self.app.post("/api/v1.0/login", headers=json_headers,
                          data='{"username": "_test", "password": "111"}')
        self.assertEqual(r.status_code, 200)
