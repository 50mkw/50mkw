# -*- coding: utf-8 -*-
from . import api
from flask import request, jsonify, make_response, Response
from app.model.onlinestore import LrUser, LrGuanggao, LrCategory, LrProduct
from datatables import ColumnDT
import requests
from datetime import datetime
import time
from app import db, basedir


@api.route('/')
def index():
    return 'Hello World!'


@api.route("/queryOpenId", methods=['GET', 'POST'])
def query_openid():
    code = request.form['code']
    appKey = request.form['appKey']
    appId = request.form['appId']
    apistr = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + appKey + '&js_code=' + code + '&grant_type=authorization_code'
    ret = requests.get(url=apistr).json()
    return ret


@api.route("/queryUser", methods=['GET', 'POST'])
def query_user():
    row = LrUser.query.filter_by(id=11).order_by(LrUser.addtime).first()
    columns = LrUser.__table__.columns.keys()
    ret = dict((c, getattr(row, c)) for c in columns)
    return jsonify(ret)


@api.route("/Index/index", methods=['GET', 'POST'])
def index_index():
    guanggao_rows = LrGuanggao.query.with_entities(LrGuanggao.id, LrGuanggao.name, LrGuanggao.photo, LrGuanggao.action)\
        .order_by(LrGuanggao.sort.desc(), LrGuanggao.id).limit(10)
    guanggao_list = []
    for row in guanggao_rows:
        guanggao_list.append(dict((c, getattr(row, c)) for c in row._fields))

    category_rows = LrCategory.query.filter_by(tid=1).with_entities(LrCategory.id, LrCategory.name, LrCategory.bz_1).limit(8)
    category_list = []
    for row in category_rows:
        category_list.append(dict((c, getattr(row, c)) for c in row._fields))

    product_rows = LrProduct.query.with_entities(LrProduct.id, LrProduct.name, LrProduct.intro, LrProduct.photo_x,
                                                 LrProduct.price_yh, LrProduct.price, LrProduct.shiyong)\
        .filter_by(status=0, pro_type=1, is_down=0, type=1)\
        .order_by(LrProduct.sort.desc(), LrProduct.id.desc()).limit(8)
    product_list = []
    for row in product_rows:
        product_list.append(dict((c, getattr(row, c)) for c in row._fields))

    ret = {}
    ret['ggtop'] = guanggao_list
    ret['prolist'] = product_list
    ret['newGoods'] = product_list
    ret['category'] = category_list
    ret['goodsCount'] = '100'
    return jsonify(ret)


@api.route("/Login/authlogin", methods=['GET', 'POST'])
def login_authlogin():
    openid = request.form['openid']
    nickname = request.form['NickName']
    headurl = request.form['HeadUrl']
    gender = request.form['gender']
    sessionid = request.form['SessionId']
    if not openid:
        return jsonify({'status':0, 'err':'授权失败!'})
    user_row = LrUser.query.filter_by(openid=openid).first()

    if user_row:
        uid = user_row.id
        user_row = LrUser.query.filter_by(id=uid).first()
        if user_row.status == 1:
            return jsonify({'status': 0, 'err': '账号状态异常!'})
        err = {}
        err['ID'] = uid
        err['NickName'] = nickname
        err['HeadUrl'] = headurl
        return jsonify({'status': 1, 'arr': err})
    else:
        user = LrUser(
            name=nickname,
            uname=nickname,
            photo=headurl,
            sex=gender,
            openid=openid,
            source='wx',
            #addtime=datetime.now(),
            addtime=int(time.time())
        )
        db.session.add(user)
        db.session.commit()
        err = {}
        err['ID'] = user.id
        err['NickName'] = nickname
        err['HeadUrl'] = headurl
        return jsonify({'status': 1, 'arr': err})
    return jsonify({'status':0, 'err':'授权失败!'})


@api.route("/Category/index", methods=['GET', 'POST'])
def category_index():
    category_rows = LrCategory.query.with_entities(LrCategory.id, LrCategory.tid, LrCategory.name, LrCategory.concent, LrCategory.bz_1, LrCategory.bz_2) \
        .filter_by(tid=1).all()
    category_list = []
    for row in category_rows:
        category_list.append(dict((c, getattr(row, c)) for c in row._fields))
    son_category_rows = LrCategory.query.with_entities(LrCategory.id, LrCategory.name, LrCategory.bz_1) \
        .filter_by(tid=category_rows[0].id).all()
    son_category_list = []
    for row in son_category_rows:
        son_category_list.append(dict((c, getattr(row, c)) for c in row._fields))
    product_rows = len(LrCategory.query.all())
    return jsonify({'status': 1, 'list': category_list, 'catList':son_category_list, 'goodsCount':product_rows})


@api.route("/Category/getcat", methods=['GET', 'POST'])
def category_getcat():
    catid = request.form['cat_id']
    if not catid:
        return jsonify({'status':0, 'err':'没有找到产品数据.'})
    category_rows = LrCategory.query.with_entities(LrCategory.id, LrCategory.name, LrCategory.bz_1) \
        .filter_by(tid=catid).all()
    category_list = []
    for row in category_rows:
        category_list.append(dict((c, getattr(row, c)) for c in row._fields))
    return jsonify({'status':1, 'catList':category_list})


@api.route("/getimage/<path:image_path>")
def show_image(image_path):
    with open(basedir + "/static/img/" + image_path, 'rb') as f:
        image = f.read()
    pic_url = Response(image, mimetype="image/jpeg")
    return pic_url
