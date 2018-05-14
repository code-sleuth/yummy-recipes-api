from flask import Blueprint

users_blue_print = Blueprint('users_blue_print', __name__)

from . import views