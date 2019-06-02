import os
import platform
from datetime import timedelta

from flask import session
from flask_migrate import Migrate
from flask_cors import CORS

from core.adapter import create_app
from config.models import *

core = create_app(os.environ.get('FLASK_CONFIG') or 'development')
core.config['JSON_SORT_KEYS'] = False
if core.config['DEBUG'] is True:
    CORS(core, supports_credentials=True)

migrate = Migrate(core, db)


@core.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@core.before_request
def make_session_permanent():
    session.permanent = True
    core.permanent_session_lifetime = timedelta(
        minutes=core.config['SESSIONS_TIMEOUT'])


if __name__ == "__main__":
    core.run(host="0.0.0.0", threaded=True)
