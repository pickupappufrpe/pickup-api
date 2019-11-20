from flask import Blueprint

referee = Blueprint('referee', __name__)

from . import views