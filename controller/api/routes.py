from flask import Blueprint

from core.hooks import resp_err, resp_success
from core.decorators import is_connection
from core.helpers.helper_zulu import get_the_east, get_tonight_show

api_bp = Blueprint("api", __name__)
