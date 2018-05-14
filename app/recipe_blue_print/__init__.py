from flask import Blueprint

recipe_blue_print = Blueprint('recipe_blue_print', __name__)

from . import views