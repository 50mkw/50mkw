# -*- coding: utf-8 -*-
from . import home
from flask import request, jsonify, make_response
from .models import LrUser
from datatables import ColumnDT


@home.route('/')
def index():
    return 'Hello World!'


@home.route('/test')
def test():
    return 'Hello World test!'


@home.route("/queryUser", methods=['GET', 'POST'])
def query_user():
    rows = LrUser.query.filter_by(id=11).order_by(LrUser.addtime).all()
    labels = []
    for i in LrUser.__table__.columns.keys():
        labels.append(ColumnDT(i))
    columns = LrUser.__table__.columns.keys()
    obj_arr = []
    for row in rows:
        obj_arr.append(dict((c, getattr(row, c)) for c in columns))
    ret = dict()
    ret['dataInfo'] = obj_arr
    return jsonify(ret)
