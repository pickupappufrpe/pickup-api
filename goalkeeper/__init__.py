from flask import Blueprint

goalkeeper = Blueprint('goalkeeper', __name__)

from . import views