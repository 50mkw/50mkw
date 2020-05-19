# -*- coding: utf-8 -*-
from . import api
from flask import request, jsonify, make_response
from app.model.onlinestore import LrUser
from datatables import ColumnDT
import requests


@api.route('/')
def index():
    return 'Hello World!'


@api.route("/queryOpenId", methods=['GET', 'POST'])
def query_user():
    code = request.args.get('code', 1, type=str)
    appId = request.args.get('appId', 1, type=str)
    appKey = request.args.get('appKey', 1, type=str)
    apistr = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + appKey + '&js_code=' + code + '&grant_type=authorization_code'
    return requests.get(url=apistr)


@api.route("/queryUser", methods=['GET', 'POST'])
def query_user():
    row = LrUser.query.filter_by(id=11).order_by(LrUser.addtime).first()
    columns = LrUser.__table__.columns.keys()
    ret = dict((c, getattr(row, c)) for c in columns)
    return jsonify(ret)

