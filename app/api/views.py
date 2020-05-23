# -*- coding: utf-8 -*-
from . import api
from flask import request, jsonify, make_response, Response
from app.model.onlinestore import LrUser, LrGuanggao, LrCategory, LrProduct, LrBrand, LrAttribute, LrGuige, LrShoppingChar, LrOrder, LrAddress, LrPost, LrShangchang, LrChinaCity
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


@api.route("/Product/index", methods=['GET', 'POST'])
def product_index():
    pro_id = request.form['pro_id']
    if not pro_id:
        return jsonify({'status':0, 'err':'商品不存在或已下架！'})
    product_row = LrProduct.query.filter_by(id=pro_id, status=0, is_down=0).first()
    if not product_row:
        return jsonify({'status':0, 'err':'商品不存在或已下架！'})
    columns = LrProduct.__table__.columns.keys()
    product = dict((c, getattr(product_row, c)) for c in columns)

    product['brand'] = LrBrand.query.filter_by(id=product_row.brand_id).first().name
    product['cat_name'] = LrCategory.query.filter_by(id=product_row.cid).first().name
    img = filter(None,product_row.photo_string.split(','))
    img_list = []
    for tmp in img:
        img_list.append(tmp)
    if not img_list:
        img_list.append(product_row.photo_d)
    product['img_arr'] = img_list

    commodityAttr = []
    attrValueList = []

    if product_row.pro_buff:
        pro_buff = filter(None, product_row.pro_buff.split(','))
        for val in pro_buff:
            attr_name = LrAttribute.query.filter_by(id=val).first().attr_name
            guigerows = LrGuige.query.filter_by(attr_id=val, pid=pro_id).with_entities(LrGuige.id, LrGuige.name).all()
            guigelist = []
            for row in guigerows:
                guigelist.append(dict((c, getattr(row, c)) for c in row._fields))
            ggss = []
            gg = []
            for val in guigerows:
                gg.append({'attrKey':attr_name, 'attrValue':val.name})
                ggss.append(val.name)
            commodityAttr.append({'attrValueList':gg})
            attrValueList.append({'attrKey':attr_name,'attrValueList':ggss})
    content = str.replace(product_row.content, 'xxx', '/minipetmrschool/Data/')
    product['content'] = 'test'

    product_rows = LrProduct.query.limit(10)
    columns = LrProduct.__table__.columns.keys()
    product_list = []
    for row in product_rows:
        product_list.append(dict((c, getattr(row, c)) for c in columns))

    return jsonify({'status': 1, 'pro':product, 'commodityAttr':commodityAttr, 'attrValueList':attrValueList, 'newGoods':product_list})


@api.route("/Shopping/index", methods=['GET', 'POST'])
def shopping_index():
    user_id = request.form['user_id']
    if not user_id:
        return jsonify({'status':0})
    cart_rows = LrShoppingChar.query.with_entities(LrShoppingChar.id, LrShoppingChar.uid, LrShoppingChar.pid, LrShoppingChar.price,
                                                   LrShoppingChar.num) \
        .filter_by(uid=user_id).all()
    cart_list = []
    for row in cart_rows:
        pro_info = LrProduct.query.filter_by(id=row.pid).with_entities(LrProduct.name, LrProduct.photo_x).first()
        row_dic = dict((c, getattr(row, c)) for c in row._fields)
        row_dic.update({'pro_name': pro_info.name, 'photo_x': pro_info.photo_x})
        cart_list.append(row_dic)
    return jsonify({'status': 1, 'cart':cart_list})


@api.route("/User/getorder", methods=['GET', 'POST'])
def user_getorder():
    uid = request.form['userId']
    if not uid:
        return jsonify({'status':0, 'err':'非法操作.'})
    order = {}
    order['pay_num'] = len(LrOrder.query.filter_by(uid=uid, state=10, status=0).all())
    order['rec_num'] = len(LrOrder.query.filter_by(uid=uid, state=30, status=0, back=0).all())
    order['finish_num'] = len(LrOrder.query.filter(LrOrder.uid==uid, LrOrder.state>30, LrOrder.status==0, LrOrder.back==0).all())
    order['refund_num'] = len(LrOrder.query.filter(LrOrder.back>0).all())
    return jsonify({'status': 1, 'orderInfo': order})


@api.route("/Payment/buy_cart", methods=['GET', 'POST'])
def payment_buy_cart():
    uid = request.form['uid']
    cart_id = request.form['cart_id']
    if not uid:
        return jsonify({'status': 0, 'err': '登录状态异常.'})
    if not cart_id:
        return jsonify({'status': 0, 'err': '网络异常.'})
    address = LrAddress.query.filter_by(uid=uid).order_by(LrAddress.is_default.desc(), LrAddress.id.desc()).first()
    pro = []
    price = 0
    cart_id_list = filter(None, cart_id.split(','))
    for val in cart_id_list:
        check_cart = LrShoppingChar.query.filter_by(id=val).first().id
        if not check_cart:
            return jsonify({'status': 0, 'err': '非法操作.'})

        cart = LrShoppingChar.query.outerjoin(LrProduct, LrProduct.id==LrShoppingChar.pid) \
            .outerjoin(LrShangchang, LrShangchang.id == LrShoppingChar.shop_id) \
            .filter(LrShoppingChar.uid == uid, LrShoppingChar.id == val) \
            .with_entities(LrProduct.num,
                           LrShoppingChar.id,
                           LrShoppingChar.pid,
                           LrShangchang.name,
                           LrProduct.name,
                           LrProduct.shop_id,
                           LrProduct.photo_x,
                           LrProduct.price_yh,
                           LrShoppingChar.num,
                           LrShoppingChar.buff,
                           LrShoppingChar.price).first()
        pro_tmp = dict(zip(['pnum','id','pid','sname','name','shop_id','photo_x','price_yh','num','buff','price'], list(cart)))
        if not pro_tmp['buff']:
            pro_tmp['zprice'] = pro_tmp['price'] * pro_tmp['num']
        else:
            pro_tmp['price'] = pro_tmp['price_yh']
            pro_tmp['zprice'] = pro_tmp['price'] * pro_tmp['num']
        price = price + pro_tmp['zprice']
        pro.append(pro_tmp)
        yunfei = LrPost.query.filter_by(pid=cart.shop_id).first()
        columns = LrPost.__table__.columns.keys()
        yunfei = dict((c, getattr(yunfei, c)) for c in columns)
    if yunfei:
        if yunfei['price_max'] > 0 and yunfei['price_max'] <= price:
            yunfei['price'] = 0
    if not address:
        addemt = 1
    else:
        addemt = 0
    columns = LrAddress.__table__.columns.keys()
    address_dict = dict((c, getattr(address, c)) for c in columns)

    return jsonify({'status':1, 'vou':'', 'price':price, 'pro':pro, 'adds':address_dict, 'addemt':addemt, 'yun':yunfei})


@api.route("/Address/index", methods=['GET', 'POST'])
def address_index():
    user_id = request.form['user_id']
    if not user_id:
        return jsonify({'status': 0, 'err': '网络异常.'})
    addrows = LrAddress.query.filter_by(uid=user_id).order_by(LrAddress.is_default.desc(), LrAddress.id.desc()).all()
    columns = LrAddress.__table__.columns.keys()
    addlist = []
    for row in addrows:
        addlist.append(dict((c, getattr(row, c)) for c in columns))
    return jsonify({'status': 1, 'adds': addlist})


@api.route("/Address/get_province", methods=['GET', 'POST'])
def address_get_province():
    china_city_rows = LrChinaCity.query.filter_by(tid=0).with_entities(LrChinaCity.id,LrChinaCity.name).all()
    china_city_list = []
    for row in china_city_rows:
        china_city_list.append(dict((c, getattr(row, c)) for c in row._fields))
    return jsonify({'status': 1, 'list': china_city_list})


@api.route("/Address/get_city", methods=['GET', 'POST'])
def address_get_city():
    sheng = request.form['sheng']
    if not sheng:
        return jsonify({'status': 0, 'err': '请选择省份.'})
    province_rows = LrChinaCity.query.filter_by(tid=0).with_entities(LrChinaCity.id,LrChinaCity.name).all()
    city_rows = LrChinaCity.query.filter_by(tid=province_rows[int(sheng)-1].id).with_entities(LrChinaCity.id, LrChinaCity.name).all()
    city_list = []
    for row in city_rows:
        city_list.append(dict((c, getattr(row, c)) for c in row._fields))
    return jsonify({'status': 1, 'city_list': city_list, 'sheng':province_rows[int(sheng)-1].id})


@api.route("/Address/get_area", methods=['GET', 'POST'])
def address_get_area():
    city = request.form['city']
    sheng = request.form['sheng']
    if not city:
        return jsonify({'status': 0, 'err': '请选择城市.'})
    city_rows = LrChinaCity.query.filter_by(tid=sheng).with_entities(LrChinaCity.id, LrChinaCity.name).all()
    area_rows = LrChinaCity.query.filter_by(tid=city_rows[int(city) - 1].id).with_entities(LrChinaCity.id, LrChinaCity.name).all()
    area_list = []
    for row in area_rows:
        area_list.append(dict((c, getattr(row, c)) for c in row._fields))
    return jsonify({'status': 1, 'area_list': area_list, 'city': city_rows[int(city) - 1].id})


@api.route("/Address/get_code", methods=['GET', 'POST'])
def address_get_code():
    quyu = request.form['quyu']
    city = request.form['city']
    area_rows = LrChinaCity.query.filter_by(tid=city).with_entities(LrChinaCity.id, LrChinaCity.name).all()
    code_row = LrChinaCity.query.filter_by(id=area_rows[int(quyu) - 1].id).with_entities(LrChinaCity.code).first()
    area_list = []
    for row in area_rows:
        area_list.append(dict((c, getattr(row, c)) for c in row._fields))
    return jsonify({'status': 1, 'code': code_row.code, 'area': area_rows[int(quyu) - 1].id})


@api.route("/Address/add_adds", methods=['GET', 'POST'])
def address_add_adds():
    user_id = request.form['user_id']
    if not user_id:
        return jsonify({'status': 0, 'err': '网络异常.'})
    name = request.form['receiver']
    tel = request.form['tel']
    sheng = request.form['sheng']
    city = request.form['city']
    quyu = request.form['quyu']
    address = request.form['adds']
    code = request.form['code']
    uid = user_id
    if not name or not tel or not address:
        return jsonify({'status': 0, 'err': '请先完善信息后再提交.'})
    if not sheng or not city or not quyu:
        return jsonify({'status': 0, 'err': '请选择省市区.'})
    #{user_id:uid,receiver:rec,tel:tel,sheng:sheng,city:city,quyu:quyu,adds:address,code:code}
    check_id = LrAddress.query.filter_by(name=name, tel=tel, sheng=sheng, city=city, quyu=quyu, address=address, code=code, uid=uid).first()
    if check_id:
        return jsonify({'status': 0, 'err': '该地址已经添加了.'})
    province_name = LrChinaCity.query.filter_by(id=sheng).first().name
    city_name = LrChinaCity.query.filter_by(id=sheng).first().name
    quyu_name = LrChinaCity.query.filter_by(id=sheng).first().name
    address_xq = province_name + ' ' + city_name + ' ' + quyu_name + ' ' + address

    address_new = LrAddress(
        name=name,
        tel=tel,
        sheng=sheng,
        city=city,
        quyu=quyu,
        address=address,
        address_xq = address_xq,
        code = code,
        uid = uid
    )
    db.session.add(address_new)
    db.session.commit()
    arr = {}
    if address_new.id:
        arr['addr_id'] = address_new.id
        arr['rec'] = address_new.name
        arr['tel'] = address_new.tel
        arr['addr_xq'] = address_new.address_xq
        return jsonify({'status': 1, 'add_arr': arr})
    else:
        return jsonify({'status': 0, 'err': '操作失败.'})


@api.route("/Address/set_default", methods=['GET', 'POST'])
def address_set_default():
    uid = request.form['uid']
    if not uid:
        return jsonify({'status': 0, 'err': '登录状态异常.'})
    addr_id = request.form['addr_id']
    if not addr_id:
        return jsonify({'status': 0, 'err': '地址信息错误.'})
    check = LrAddress.query.filter_by(uid=uid, is_default=1).first()
    if check:
        try:
            check.is_default = 0
            db.session.commit()
        except Exception as e:
            return jsonify({'status': 0, 'err': '设置失败.'})
    address = LrAddress.query.filter_by(id=addr_id, uid=uid).first()
    try:
        address.is_default = 1
        db.session.commit()
    except Exception as e:
        return jsonify({'status': 0, 'err': '设置失败.'})
    return jsonify({'status': 1})


@api.route("/getimage/<path:image_path>")
def show_image(image_path):
    with open(basedir + "/static/img/" + image_path, 'rb') as f:
        image = f.read()
    pic_url = Response(image, mimetype="image/jpeg")
    return pic_url
