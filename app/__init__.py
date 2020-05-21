# -*- coding: utf-8 -*-
from flask import Flask, make_response, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import json
from decimal import Decimal
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))

from app.home import home as home_blueprint
from app.api import api as api_blueprint

app.register_blueprint(home_blueprint, url_prefix="/home")
app.register_blueprint(api_blueprint, url_prefix="/api")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        # if isinstance(o,ObjectId):
        #     return str(o)
        if isinstance(o,Decimal):
            return str(o)
        return json.JSONEncoder.default(self,o)


app.json_encoder = JSONEncoder


# @app.route('/getimage',methods=['POST'])
# def getimage():
#     img = request.files.get('file')
#     path = basedir+"/static/img/"
#     imgName = img.filename
#     file_path = path+imgName
#     img.save(file_path)
#     url = '/static/img/'+imgName
#     return url

# @app.route("/getimage/<image_path>")
# def show_image(image_path):
# 	'''
# 	利用图片url用于显示
# 	'''
# 	with open(basedir + "/static/img/" + image_path, 'rb') as f:
# 		image = f.read()
# 	pic_url = Response(image, mimetype="image/jpeg")
# 	return pic_url