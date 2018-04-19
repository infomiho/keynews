from flask import jsonify, request

from . import api
from .. import db

# Catch all for the frontend
@api.route('/', defaults={'path': ''}, methods=['GET'])
@api.route('/<path:path>')
def serve(path):
    return db.app.send_static_file('index.html')
