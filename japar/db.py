import pymysql.cursors
from flask import g
import os


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    try:
        from boto.s3.connection import S3Connection
    except ImportError:
        import configparser
        config = configparser.ConfigParser()
        print("从本地读取数据库配置信息")
        config.read("../config/database.conf")

        mysql = config["MySQL"]
        host = mysql["host"]
        port = mysql["port"]
        user = mysql["user"]
        password = mysql["password"]
        db = mysql["db"]
    else:
        from urllib.parse import urlparse
        if 'CLEARDB_DATABASE_URL' in os.environ:
            print("从服务器环境变量读取数据库配置信息")
            url = urlparse(os.environ['CLEARDB_DATABASE_URL'])
            dbconf = url.netloc
            host = dbconf.split("@")[1]
            port = 3306
            user = dbconf.split(":")[0]
            password = dbconf.split("@")[0].split(":")[1]
            db = url.path[1:]
    finally:
        if 'db' not in g:
            print("连接数据库...")
            g.db = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   db=db,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
            print("连接数据库成功")

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
