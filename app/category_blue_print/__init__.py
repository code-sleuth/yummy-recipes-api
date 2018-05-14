from flask import Blueprint

category_blue_print = Blueprint('category_blue_print', __name__)

from . import views
