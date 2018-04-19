from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
cache = None
cache_timeout=1800

def create_app(config_name):

    app = Flask(__name__, static_folder="static", template_folder="static")

    from flask_cache import Cache
    global cache
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    from config import config
    app.config.from_object(config[config_name])

    CORS(app)

    db.init_app(app)
    db.app = app
    ma.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='')

    return app
