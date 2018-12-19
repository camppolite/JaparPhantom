import pymysql.cursors
from flask import g
import os


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    from urllib.parse import urlparse
    url = urlparse(os.environ['CLEARDB_DATABASE_URL'])
    print(url)

    try:
        from boto.s3.connection import S3Connection
    except ImportError:
        import configparser
        config = configparser.ConfigParser()
        config.read("../config/database.conf")
        mysql = config["MySQL"]
        host = mysql["host"]
        port = mysql["port"]
        user = mysql["user"]
        password = mysql["password"]
        db = mysql["db"]
    else:
        from urllib.parse import urlparse
        if 'DATABASE_URL' in os.environ:
            url = urlparse(os.environ['CLEARDB_DATABASE_URL'])
            print(url)
        s3 = S3Connection(os.environ['CLEARDB_DATABASE_URL'], os.environ['CLEARDB_DATABASE_URL'])
        print(s3)


    if 'db' not in g:
        g.db = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               password=password,
                               db=db,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
