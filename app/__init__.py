from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.api import api as api_blueprint

app.register_blueprint(home_blueprint, url_prefix="/home")
app.register_blueprint(api_blueprint, url_prefix="/api")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
