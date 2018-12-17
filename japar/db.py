import pymysql.cursors

from flask import g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = pymysql.connect(host='192.168.64.133',
                               port=3306,
                               user='root',
                               password='123456',
                               db='shenghuokezhan',
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
