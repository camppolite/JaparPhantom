#!/usr/bin/env python

import os
from flask import Flask


LISTEN_PORT = 33321


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=os.urandom(16)
)

# apply the blueprints to the app
from japar import auth, blog, home
app.register_blueprint(home.bp)
# app.register_blueprint(auth.bp)
# app.register_blueprint(blog.bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=LISTEN_PORT)

