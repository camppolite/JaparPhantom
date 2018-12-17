import os
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(16)
    )

    # apply the blueprints to the app
    from tavern import auth, blog, home
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    return app
