#!python3
from flask import Flask, render_template
import click
import logging
import logging.handlers
import sys
import pymongo
app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
__version__ = '1.0'

# Add StremHandler and FileHandler
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("SBS.log")
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(stream_handler)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)
log = app.logger.info
d_log = app.logger.debug

client = pymongo.MongoClient()
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
        d_log("Starting SBS")
        start_app()


def start_app():
    app.run(debug=True)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    cli()
