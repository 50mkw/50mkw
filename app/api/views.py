# -*- coding: utf-8 -*-
from . import api
from flask import request, jsonify, make_response, Response
from app.model.onlinestore import LrUser, LrGuanggao, LrCategory, LrProduct, LrBrand, LrAttribute, LrGuige, \
    LrShoppingChar, LrOrder, LrAddress, LrPost, LrShangchang, LrChinaCity, LrOrderProduct, LrUserVoucher, \
    LrSearchRecord
from datatables import ColumnDT
from sqlalchemy import func, desc
import requests
from datetime import datetime
import time, random, hashlib
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


@api.route("/Product/lists", methods=['GET', 'POST'])
def product_lists():
    id = request.form.get('cat_id', type=int, default=None)
    brand_id = request.form.get('brand_id', type=int, default=None)
    page = request.form.get('page', type=int, default=None)
    ptype = request.form.get('ptype', type=str, default=None)
    type = request.form.get('type', type=str, default=None)
    keyword = request.form.get('keyword', type=str, default=None)

    if type == 'ids':
        order = LrProduct.id.desc()
    elif type == 'sale':
        order = LrProduct.shiyong.desc()
    elif type == 'price':
        order = LrProduct.price_yh.desc()
    elif type == 'hot':
        order = LrProduct.renqi.desc()
    else:
        order = LrProduct.addtime.desc()
    product_row = LrProduct.query.filter_by(pro_type=1,status=0,is_down=0)
    if id:
        product_row = product_row.filter_by(cid=id)
    if brand_id:
        product_row = product_row.filter_by(brand_id=brand_id)
    if keyword:
        product_row = product_row.filter(LrProduct.name.ilike('%'+keyword+'%'))
    if ptype and ptype == 'new':
        product_row = product_row.filter_by(is_show=1)
    elif ptype and ptype == 'hot':
        product_row = product_row.filter_by(is_hot=1)
    if ptype and ptype == 'zk':
        product_row = product_row.filter_by(is_sale=1)
    product_row = product_row.order_by(order).offset(page).limit(20).all()
    product_list = []
    columns = LrProduct.__table__.columns.keys()
    for row in product_row:
        product_list.append(dict((c, getattr(row, c)) for c in columns))
    cat = LrCategory.query.filter_by(id=id).first()
    cat_name = ''
    cat_pic = ''
    if cat:
        cat_name = cat.name
        cat_pic = cat.bz_2
    return jsonify({'status':1, 'pro':product_list, 'cat_name':cat_name, 'cat_pic':cat_pic})


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


@api.route("/Shopping/add", methods=['GET', 'POST'])
def shopping_add():
    uid = request.form['uid']
    if not uid:
        return jsonify({'status':0,'err':'登录状态异常.'})
    pid = request.form['pid']
    num = request.form['num']
    if not pid or not num:
        return jsonify({'status':0,'err':'参数错误.'})
    check = check_cart(pid)
    if check['status'] == 0:
        return jsonify({'status': 0, 'err': check['err']})
    check_info = LrProduct.query.filter_by(id=pid, status=0, is_down=0).first()
    num = int(num)
    if check_info.num <= num:
        return jsonify({'status': 0, 'err': '库存不足!'})
    cart_info = LrShoppingChar.query.filter_by(pid=pid, uid=uid).first()
    if cart_info:
        if check_info.num <= cart_info.num + num:
            return jsonify({'status': 0, 'err': '库存不足!'})
        cart_info.num = cart_info.num + num
        db.session.commit()
        return jsonify({'status': 1, 'cart_id': cart_info.id})
    else:
        new_cart = LrShoppingChar(
            pid=pid,
            num=num,
            addtime=int(time.time()),
            uid=uid,
            shop_id=check_info.shop_id,
            type=check_info.pro_type,
            price=check_info.price_yh,
            buff=''
        )
        try:
            db.session.add(new_cart)
            db.session.commit()
            return jsonify({'status': 1, 'cart_id': new_cart.id})
        except Exception as e:
            return jsonify({'status': 0, 'err': '加入失败.'})


@api.route("/Shopping/up_cart", methods=['GET', 'POST'])
def shopping_up_cart():
    uid = request.form['user_id']
    cart_id = request.form['cart_id']
    num = request.form['num']
    if not uid or not cart_id or not num:
        return jsonify({'status':0,'err':'网络异常.'})
    cart = LrShoppingChar.query.filter_by(id=cart_id).first()
    if not cart:
        return jsonify({'status': 0, 'err': '购物车信息错误!'})
    check_info = LrProduct.query.filter_by(id=cart.pid, status=0, is_down=0).first()
    num = int(num)
    if check_info.num <= num:
        return jsonify({'status': 0, 'err': '库存不足!'})
    try:
        cart.num = num
        db.session.commit()
        return jsonify({'status': 1, 'succ': '操作成功!'})
    except Exception as e:
        return jsonify({'status': 0, 'err': '操作失败.'})


@api.route("/Shopping/delete", methods=['GET', 'POST'])
def shopping_delete():
    cart_id = request.form['cart_id']
    cart = LrShoppingChar.query.filter_by(id=cart_id).first()
    if not cart:
        return jsonify({'status': 1})
    try:
        db.session.delete(cart)
        db.session.commit()
        return jsonify({'status': 1})
    except Exception as e:
        return jsonify({'status': 0})


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
        check_cart_row = LrShoppingChar.query.filter_by(id=val).first()
        if not check_cart_row:
            return jsonify({'status': 0, 'err': '非法操作.'})
        #check_cart = check_cart_row.id

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
    city_name = LrChinaCity.query.filter_by(id=city).first().name
    quyu_name = LrChinaCity.query.filter_by(id=quyu).first().name
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


@api.route("/Address/del_adds", methods=['GET', 'POST'])
def address_del_adds():
    user_id = request.form['user_id']
    if not user_id:
        return jsonify({'status': 0, 'err': '登录状态异常.'})
    id_arr = request.form['id_arr']
    id_list_filter = filter(None, id_arr.split(','))
    id_list = []
    for tmp in id_list_filter:
        id_list.append(tmp)
    if id_list:
        add_rows = LrAddress.query.filter(LrAddress.uid==user_id, LrAddress.id.in_(id_list)).all()
        try:
            # db.session.delete(add_rows)
            for add_row in add_rows:
                db.session.delete(add_row)
            db.session.commit()
            return jsonify({'status': 1})
        except Exception as e:
            return jsonify({'status': 0, 'err': '操作失败.'})
    else:
        return jsonify({'status': 0, 'err': '没有找到要删除的数据.'})


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


@api.route("/Payment/payment", methods=['GET', 'POST'])
def payment_payment():
    uid = request.form['uid']
    if not uid:
        return jsonify({'status': 0, 'err': '登录状态异常.'})
    cart_id = request.form['cart_id']
    if not cart_id:
        return jsonify({'status': 0, 'err': '数据异常.'})
    shop = []
    cart_id_filter = filter(None, cart_id.split(','))
    cart_id_list = []
    for tmp in cart_id_filter:
        cart_id_list.append(tmp)
    num = 0
    for val in cart_id_list:
        cart = LrShoppingChar.query.outerjoin(LrProduct, LrProduct.id==LrShoppingChar.pid) \
            .filter(LrShoppingChar.uid == uid, LrShoppingChar.id == val) \
            .with_entities(LrShoppingChar.pid,
                           LrShoppingChar.num,
                           LrShoppingChar.shop_id,
                           LrShoppingChar.buff,
                           LrShoppingChar.price,
                           LrProduct.price_yh,).first()
        pro_tmp = dict(zip(['pid','num','shop_id','buff','price','price_yh'], list(cart)))
        num = num + pro_tmp['num']
        if not pro_tmp['buff']:
            ozprice = pro_tmp['price'] * pro_tmp['num']
        else:
            pro_tmp['price'] = pro_tmp['price_yh']
            ozprice = pro_tmp['price'] * pro_tmp['num']
        shop.append(pro_tmp)

    yunfei = request.form['yunfei']
    if yunfei:
        yunPrice = LrPost.query.filter_by(id=yunfei).first()
        post = yunPrice.id
        price = ozprice + yunPrice.price
    else:
        post = 0
        price = ozprice
    amount = price
    vid = request.form['vid']
    if int(vid):
        vouinfo = LrUserVoucher.query.filter_by(status=1, uid=uid, vid=vid).first()
        chk = LrOrder.query.filter(LrOrder.uid==uid, LrOrder.vid==vid, LrOrder.status>0).all()
        if not vouinfo or chk:
            return jsonify({'status': 0, 'err': '此优惠券不可用，请选择其他.'})
        if vouinfo.end_time < time.time():
            return jsonify({'status': 0, 'err': '优惠券已过期了.'})
        if vouinfo.start_time > time.time():
            return jsonify({'status': 0, 'err': '优惠券还未生效.'})
        amount = price - vouinfo.amount
    addtime = int(time.time())
    status = 0
    type = request.form['type']
    state = 10
    adds_id = request.form['aid']
    if not adds_id:
        return jsonify({'status': 0, 'err': '请选择收货地址.'})
    adds_info = LrAddress.query.filter_by(id=adds_id).first()
    receiver = adds_info.name
    tel = adds_info.tel
    address_xq = adds_info.address_xq
    code = adds_info.code
    product_num = num
    remark = request.form['remark']
    order_sn = build_order_no()

    order = LrOrder(
        order_sn=order_sn,
        shop_id=shop[0]['shop_id'],
        uid=uid,
        price=price,
        amount=amount,
        addtime=addtime,
        status=status,
        type=type,
        state=state,
        vid=vid,
        receiver=receiver,
        tel=tel,
        address_xq=address_xq,
        code=code,
        post=post,
        remark=remark,
        product_num=product_num,
        post_remark=''
    )
    try:
        db.session.add(order)
        db.session.commit()
        for val in cart_id_list:
            cart = LrShoppingChar.query.outerjoin(LrProduct, LrProduct.id == LrShoppingChar.pid) \
                .filter(LrShoppingChar.uid == uid, LrShoppingChar.id == val) \
                .with_entities(LrShoppingChar.pid,
                               LrShoppingChar.num,
                               LrShoppingChar.shop_id,
                               LrShoppingChar.buff,
                               LrShoppingChar.price,
                               LrProduct.name,
                               LrProduct.photo_x,
                               LrProduct.price_yh,
                               LrProduct.num).first()
            pro_tmp = dict(zip(['pid', 'num', 'shop_id', 'buff', 'price', 'name', 'photo_x', 'price_yh', 'pnum'], list(cart)))
            if not pro_tmp['buff']:
                pro_tmp['price'] = pro_tmp['price_yh']
            buff_text = ''
            if pro_tmp['buff']:
                buff_list = filter(None, pro_tmp['buff'].split(','))
                if buff_list:
                    for buff in buff_list:
                        ggid = LrGuige.query.filter_by(id=buff).first()
                        buff_text = buff_text + ggid.name + ' '
            order_pro = LrOrderProduct(
                pid=pro_tmp['pid'],
                name=pro_tmp['name'],
                order_id=order.id,
                price=pro_tmp['price'],
                photo_x=pro_tmp['photo_x'],
                pro_buff=buff_text.strip(' '),
                addtime=int(time.time()),
                num=pro_tmp['num'],
                pro_guige=''
            )
            try:
                db.session.add(order_pro)
                db.session.commit()
            except Exception as e:
                err_str = '下单 失败!' + e
                return jsonify({'status': 0, 'err': err_str})
            check_pro = LrProduct.query.filter_by(id=pro_tmp['pid'], status=0, is_down=0).first()

            check_pro.num = check_pro.num - pro_tmp['num']
            check_pro.shiyong = check_pro.shiyong + pro_tmp['num']
            db.session.commit()

            cart_row = LrShoppingChar.query.filter_by(uid=uid, id=val).first()
            db.session.delete(cart_row)
            db.session.commit()
    except Exception as e:
        return jsonify({'status': 0, 'err': e})
    arr = {}
    arr['order_id'] = order.id
    arr['order_sn'] = order.order_sn
    arr['pay_type'] = request.form['type']
    return jsonify({'status': 1, 'arr': arr})


@api.route("/Order/index", methods=['GET', 'POST'])
def order_index():
    uid = request.form['uid']
    if not uid:
        return jsonify({'status': 0, 'err': '登录状态异常.'})
    pages = request.form['page']
    if not pages:
        pages = 0
    order_type = request.form['order_type']
    status = 0
    back = 0
    state = 10
    if order_type:
        if order_type == 'pay':
            state = 10
        elif order_type == 'deliver':
            state = 20
        elif order_type == 'receive':
            state = 30
        elif order_type == 'evaluate':
            state = 40
        elif order_type == 'finish':
            state = 50
        else:
            state = 10
    count = len(LrOrder.query.filter_by(status=status, back=str(back), state=state, uid=uid).all())
    eachpage = 7
    order_status = {'0':'已取消', '10':'待付款', '20':'待发货', '30':'待收货', '40':'待评价', '50':'交易完成', '51':'交易关闭'}
    order_row = LrOrder.query.filter_by(status=status, back=str(back), state=state, uid=uid)\
        .with_entities(LrOrder.id, LrOrder.order_sn, LrOrder.pay_sn, LrOrder.state, LrOrder.price, LrOrder.type, LrOrder.product_num)\
        .offset(pages).limit(7).all()
    order_list = []
    for row in order_row:
        order = dict((c, getattr(row, c)) for c in row._fields)
        order['desc'] = order_status[str(row.state)]
        order_product_rows = LrOrderProduct.query.filter_by(order_id=row.id).all()
        order_product_photo_x_list = []
        order_product_pid_list = []
        order_product_name_list = []
        order_product_price_list = []
        for val in order_product_rows:
            order_product_photo_x_list.append(val.photo_x)
            order_product_pid_list.append(val.pid)
            order_product_name_list.append(val.name)
            order_product_price_list.append(val.price)
        order['photo_x'] = order_product_photo_x_list
        order['pid'] = order_product_pid_list
        order['name'] = order_product_name_list
        order['price_yh'] = order_product_price_list
        order['pro_count'] = len(order_product_pid_list)
        order_list.append(order)
    return jsonify({'status':1, 'ord':order_list, 'eachpage':eachpage})


@api.route("/Order/order_details", methods=['GET', 'POST'])
def order_order_details():
    order_id = request.form['order_id']
    order_info = LrOrder.query.filter_by(id=order_id, status=0)\
        .with_entities(LrOrder.id, LrOrder.order_sn, LrOrder.shop_id, LrOrder.state, LrOrder.addtime, LrOrder.price,
                       LrOrder.type, LrOrder.post, LrOrder.tel, LrOrder.receiver, LrOrder.address_xq, LrOrder.remark).first()
    if not order_info:
        jsonify({'status': 0, 'err': '订单信息错误.'})
    order_status = {'0': '已取消', '10': '待付款', '20': '待发货', '30': '待收货', '40': '待评价', '50': '交易完成', '51': '交易关闭'}
    pay_type = {'cash': '现金支付', 'alipay':'支付宝', 'weixin':'微信支付'}
    order_info_dict = dict((c, getattr(order_info, c)) for c in order_info._fields)
    shop = LrShangchang.query.filter_by(id=order_info.shop_id).first()
    order_info_dict['shop_name'] = shop.name
    order_info_dict['order_status'] = order_status[str(order_info.state)]
    order_info_dict['pay_type'] = pay_type[order_info.type]
    order_info_dict['addtime'] = datetime.fromtimestamp(order_info.addtime).strftime("%Y-%m-%d %H:%M:%S")
    order_info_dict['yunfei'] = 0
    if order_info.post:
        order_info_dict['yunfei'] = LrPost.query.filter_by(id=order_info.post).first().price
    pro_rows = LrOrderProduct.query.filter_by(order_id=order_info.id).all()
    pro_list = []
    columns = LrOrderProduct.__table__.columns.keys()
    for row in pro_rows:
        pro_list.append(dict((c, getattr(row, c)) for c in columns))
    return jsonify({'status': 1, 'pro': pro_list, 'ord': order_info_dict})


@api.route("/Order/orders_edit", methods=['GET', 'POST'])
def order_orders_edit():
    order_id = request.form['id']
    type = request.form['type']
    order = LrOrder.query.filter_by(id=order_id, status=0).first()
    if not order or not type:
        return jsonify({'status': 0, 'err': '订单信息错误.'})
    if type == 'cancel':
        order.state = 0
    elif type == 'receive':
        order.state = 40
    elif type == 'refund':
        order.back = 1
        order.back_remark = request.form['back_remark']
    try:
        db.session.commit()
        return jsonify({'status': 1})
    except Exception as e:
        return jsonify({'status': 0, 'err': '操作失败.'})


@api.route("/Wxpay/wxpay", methods=['GET', 'POST'])
def wxpay_wxpay():
    pay_sn = request.form['order_sn']
    if not pay_sn:
        return jsonify({'status': 0, 'err': '支付信息错误!'})
    order_info = LrOrder.query.filter_by(order_sn=pay_sn).first()
    if not order_info:
        return jsonify({'status': 0, 'err': '没有找到支付订单!'})
    if order_info.state != 10:
        return jsonify({'status': 0, 'err': '订单状态异常!'})
    user = LrUser.query.filter_by(id=order_info.uid).first()
    if not user:
        return jsonify({'status': 0, 'err': '用户状态异常!'})
    openId = user.openid

    # $tools = new \JsApiPay();
    # # 统一下单
    # $input = new \WxPayUnifiedOrder();
    # $input->SetBody("信真小铺商品购买_".trim($order_info['order_sn']));
    # $input->SetAttach("信真小铺商品购买_".trim($order_info['order_sn']));
    # $input->SetOut_trade_no($pay_sn);
    # $input->SetTotal_fee(floatval($order_info['amount'])*100);
    # $input->SetTime_start(date("YmdHis"));
    # $input->SetTime_expire(date("YmdHis", time() + 3600));
    # $input->SetGoods_tag("信真小铺商品购买_".trim($order_info['order_sn']));
    # $input->SetNotify_url('https://mini.laohuzx.com/index.php/Api/Wxpay/notify');
    # $input->SetTrade_type("JSAPI");
    # $input->SetOpenid($openId);
    # $order = \WxPayApi::unifiedOrder($input);
    arr = {}
    arr['appId'] = ''
    arr['nonceStr'] = ''
    arr['package'] = ''
    arr['signType'] = "MD5"
    arr['timeStamp'] = ''
    arr['paySign'] = ''
    return jsonify({'status': 1, 'arr': arr})


@api.route("/Search/index", methods=['GET', 'POST'])
def search_index():
    uid = request.form.get('uid', type=int, default=None)
    remen_rows = LrSearchRecord.query.with_entities(LrSearchRecord.keyword,func.sum(LrSearchRecord.num).label('sum'))\
        .group_by(LrSearchRecord.keyword).order_by(desc('sum')).all()
    history_rows = LrSearchRecord.query.filter_by(uid=uid).order_by(LrSearchRecord.addtime.desc()).limit(20)
    remen_list = []
    history_list = []
    columns = LrSearchRecord.__table__.columns.keys()
    for row in remen_rows:
        remen_list.append(dict((c, getattr(row, c)) for c in row._fields))
    for row in history_rows:
        history_list.append(dict((c, getattr(row, c)) for c in columns))
    return jsonify({'remen':remen_list, 'history':history_list})


@api.route("/Search/searches", methods=['GET', 'POST'])
def search_searches():
    uid = request.form.get('uid', type=int, default=None)
    #keyword = request.form.get('keyword', type=str, default=None) #无法获取中文参数
    keyword = request.form['keyword']
    if not keyword:
        return jsonify({'status': 0, 'err': '请输入搜索内容!'})
    if uid:
        check_row = LrSearchRecord.query.filter_by(uid=uid, keyword=keyword).first()
        if check_row:
            check_row.num = check_row.num + 1
            db.session.commit()
        else:
            new_row = LrSearchRecord(uid=uid,
                                     keyword=keyword,
                                     addtime=int(time.time()))
            db.session.add(new_row)
            db.session.commit()
    page = request.form.get('page', type=int, default=0)
    prorows = LrProduct.query.filter_by(status=0,pro_type=1,is_down=0).filter(LrProduct.name.ilike('%'+keyword+'%'))\
        .order_by(LrProduct.addtime.desc()).with_entities(LrProduct.id,LrProduct.name,LrProduct.photo_x,
                                                          LrProduct.shiyong,LrProduct.price,LrProduct.price_yh).all()
    prolist = []
    for row in prorows:
        prolist.append(dict((c, getattr(row, c)) for c in row._fields))

    page2 = request.form.get('page2', type=int, default=0)

    storerows = LrShangchang.query.filter_by(status=1).filter(LrShangchang.name.ilike('%' + keyword + '%')) \
        .order_by(LrShangchang.sort.desc(), LrShangchang.type.desc())\
        .with_entities(LrShangchang.id, LrShangchang.name, LrShangchang.uname,
                       LrShangchang.logo, LrShangchang.tel, LrShangchang.sheng,
                       LrShangchang.city, LrShangchang.quyu).offset(page2).limit(6).all()
    store_list = []
    for row in storerows:
        row_dict = dict((c, getattr(row, c)) for c in row._fields)
        row_dict['sheng'] = LrChinaCity.query.filter_by(id=row_dict['sheng']).first().name
        row_dict['city'] = LrChinaCity.query.filter_by(id=row_dict['city']).first().name
        row_dict['quyu'] = LrChinaCity.query.filter_by(id=row_dict['quyu']).first().name
        pro_rows = LrProduct.query.filter_by(status=0, is_down=0, shop_id=row.id).with_entities(LrProduct.id,LrProduct.photo_x,LrProduct.price_yh).limit(4).all()
        pro_list = []
        for row in pro_rows:
            pro_list.append(dict((c, getattr(row, c)) for c in row._fields))
        row_dict['pro_list'] = pro_list
        store_list.append(row_dict)
    return jsonify({'status':1, 'pro': prolist, 'shop': store_list})


@api.route("/getimage/<path:image_path>")
def show_image(image_path):
    with open(basedir + "/static/img/" + image_path, 'rb') as f:
        image = f.read()
    pic_url = Response(image, mimetype="image/jpeg")
    return pic_url


def build_order_no():
    random_str = '{0:%Y%m%d%H%M%S%f}'.format(datetime.now()) + ''.join([str(random.randint(1, 10)) for i in range(5)])
    return hashlib.md5(random_str.encode('utf-8')).hexdigest()[8:-8]


def check_cart(pid):
    check_info = LrProduct.query.filter_by(id=pid, status=0, is_down=0).first()
    if not check_info:
        return {'status': 0, 'err':'商品不存在或已下架.'}
    else:
        return {'status': 1}
