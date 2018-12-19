#!/usr/bin/env python

import os
from flask import Flask
import logging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("logger.py")

app = Flask(__name__, instance_relative_config=True)
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
app.config.from_mapping(
    SECRET_KEY=os.urandom(16)
)
app.config.from_pyfile("config.py", silent=True)

# apply the blueprints to the app
from japar import auth, blog, home
app.register_blueprint(home.bp)
app.register_blueprint(auth.bp)
# app.register_blueprint(blog.bp)


if __name__ == '__main__':
    app.run()

