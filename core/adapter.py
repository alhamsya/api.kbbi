# Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Config
from config.apps import setup
from config.views import register_bp
from core.error import error_handler

db = SQLAlchemy()


def create_app(config_name):
    '''The application factory function'''

    app = Flask(__name__)
    app.config.from_object(setup[config_name])
    setup[config_name].init_app(app)

    # link extensions to app
    db.init_app(app)

    # for error handle
    error_handler(app)

    # register blueprints
    register_bp(app)

    return app
