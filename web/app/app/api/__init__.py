from flask import Blueprint

api = Blueprint('api', __name__)

from . import article
from . import keyword
from . import scraping
from . import frontend
