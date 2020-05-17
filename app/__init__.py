from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.home import home as home_blueprint

app.register_blueprint(home_blueprint, url_prefix="/home")