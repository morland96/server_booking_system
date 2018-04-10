#!python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
from app.db import User, Reservation, config_connect
import json
import click
import logging
import logging.handlers
import sys
import pymongo
from app.config import Config

flask_app = Flask(__name__,
                  static_folder="./dist/static",
                  template_folder="./dist")
__version__ = '1.0'

# Set config
flask_app.config.from_object(Config())
time_format = '%Y-%m-%dT%H:%M:%S.%f'
# Add StremHandler and FileHandler
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("SBS.log")
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
flask_app.logger.addHandler(stream_handler)
flask_app.logger.addHandler(file_handler)
flask_app.logger.setLevel(logging.DEBUG)
log = flask_app.logger.info
d_log = flask_app.logger.debug

client = pymongo.MongoClient()
config_connect(flask_app.logger)
db = client.SBS


@click.command()
@click.option('--version', is_flag=True, help="Show the version")
@click.option('--initdb', is_flag=True, help="Init the database")
@click.option('--cleandb', is_flag=True, help="Clean the database")
@click.option('--level', type=str, default="INFO")
def cli(version, initdb, cleandb, level):
    if level:
        # logger.setLevel(level)
        pass
    if version:
        click.echo(__version__)
    elif initdb:
        # Initlize database. Any existing collection will be removed.
        # Set defualt admin account with password "admin"
        click.echo("Initializing database....")
        if "users" in db.collection_names():
            log("[users] existing in database, it will be cleaned up....")
            db.drop_collection("users")
        db.create_collection("users")
        admin = {
            "username": "admin",
            "password": "admin",
            "type": 0
        }
        log("Insterting default admin account. ")
        db.users.insert(admin)
        log("Done!")

    elif cleandb:
        if "SBS" in client.database_names():
            client.drop_database("SBS")
        pass
    else:
        # logger.setLevel(level)
        start_app()


def start_app():
    flask_app.run(debug=True)


@flask_app.route('/', defaults={'path': ''})
@flask_app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@flask_app.route('/__webpack_hmr')
def npm():
    return redirect("http://localhost:8080/__webpack_hmr")


"""
Group of API for users.
POST    /api/v1.0/users         Register a user
DELETE  /api/v1.0/<username>    Delete a user  
UPDATE  /api/v1.0/<username>    Update a user need token
POST    /api/v1.0/login         Login and get a token for request query
POST    /api/v1.0/test_token    Check token if it's works
"""


@flask_app.route('/api/v1.0/users', methods=['POST'])
def register_user():
    data = request.get_data()
    data = json.loads(data)
    username = data['username']
    password = data['password']
    users = User.objects(username=username, password=password)
    if len(users) > 0:
        return jsonify({'id': -1}), 409
    else:
        user = User()
        user.username = username
        user.password = password
        user.privilege = 0
        user.save()
        return jsonify(user.get_dict()), 201


@flask_app.route('/api/v1.0/users/<string:username>', methods=['DELETE'])
def delete_user(username):
    user = User.objects(username=username)
    if len(user) == 0:
        return jsonify({'status': -1}), 404
    user.delete()
    return jsonify({'status': 0}), 204


@flask_app.route('/api/v1.0/users/<string:username>', methods=['PUT'])
def update_user(username):
    user = User.verify_auth_token(
        request.headers.get('Authentication-Token'))
    if user.username == username:
        new_user = json.loads(request.get_data())
        user.update_with_dict(new_user)
        return jsonify(user.get_dict()), 201
    else:
        return 403


@flask_app.route('/api/v1.0/sessions', methods=['POST'])
def login():
    data = request.get_data()
    try:
        data = json.loads(data)
    except Exception as e:
        return jsonify({}), 406
    username = data['username']
    password = data['password']
    user = User.login(username, password)
    if user is not None:
        return jsonify({"user": user.get_dict(), "token": user.token}), 201
    else:
        return jsonify({"id": 0}), 401


@flask_app.route('/api/v1.0/test/token', methods=['POST'])
def test_token():
    user = User.verify_auth_token(
        request.headers.get('Authentication-Token'))
    if user is not None:
        return jsonify(user.get_dict()), 201
    else:
        return jsonify({}), 403


"""
Group of API for booking
"""


@flask_app.route('/api/v1.0/reservations', methods=['POST'])
def create_reservation():
    """Apply for a reservation"""
    user = User.verify_auth_token(request.headers.get('Authentication-Token'))
    if user is not None:
        data = json.loads(request.get_data())
        r = Reservation.reserve(user, data['start_time'], data['end_time'])
        return jsonify(r.get_dict()), 201
    else:
        return jsonify({}), 403


@flask_app.route('/api/v1.0/reservations/<string:r_id>/allowed', methods=['POST'])
def approve_reservation(r_id):
    user = User.verify_auth_token(request.headers.get('Authentication-Token'))
    if user is not None:
        if user.privilege > 0:  # Check if user is an administrator.
            r = Reservation.objects(id=r_id)
            if len(r) == 0:
                return jsonify({"msg": "Id not exist"}), 404
            else:
                r[0].accept()
                return jsonify(r[0].get_dict()), 201
        else:
            return jsonify({"msg": "Not permitted"}), 403


@flask_app.route('/api/v1.0/reservations', methods=['GET'])
def get_all_reservations():
    l_reservations = []
    reservations = Reservation.objects()
    for r in reservations:
        l_reservations.append(r.get_dict())
    return jsonify(l_reservations), 200


if __name__ == '__main__':
    cli()
