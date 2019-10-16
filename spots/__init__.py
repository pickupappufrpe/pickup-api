from flask import Blueprint

spot = Blueprint('spot', __name__)

from . import views