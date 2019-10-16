from flask import Blueprint

address = Blueprint('address', __name__)

from . import views