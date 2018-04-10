import jwt
import datetime
from flask import current_app as app


class Auth():
    @staticmethod
    def encode_auth_token(username, login_time) -> str:
        """ Get Token
        :param username: int
        :param login_time: int(timestamp)
        :return: string
        :rtype: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
                'iat': datetime.datetime.utcnow(),
                'data': {
                    'username': username,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            raise e
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validate JWT
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config['SECRET_KEY'], options={
                'Verify_exp': False})
            if ('data' in payload and 'username' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return -2
        except jwt.InvalidTokenError:
            return -1
