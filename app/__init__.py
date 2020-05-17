from flask import Flask

app = Flask(__name__)

from app.home import home as home_blueprint

app.register_blueprint(home_blueprint, url_prefix="/home")