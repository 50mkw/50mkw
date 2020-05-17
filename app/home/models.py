# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, String, text, Text, ForeignKey, Float, Enum, DECIMAL
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, MEDIUMTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db



Base = declarative_base()
metadata = Base.metadata


class LrAddres(db.Model):
    __tablename__ = 'lr_address'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, unique=True, comment='地址id')
    name = Column(String(10), nullable=False, comment='收货人')
    tel = Column(CHAR(15), nullable=False, comment='联系方式')
    sheng = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='省id')
    city = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='市id')
    quyu = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='区域id')
    address = Column(String(255), nullable=False, comment='收货地址（不加省市区）')
    address_xq = Column(String(255), nullable=False, comment='省市区+详细地址')
    code = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='邮政编号')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    is_default = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='是否默认地址 1默认')


class LrAdminApp(db.Model):
    __tablename__ = 'lr_admin_app'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True)
    pid = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    name = Column(String(50), nullable=False, comment='系统名称')
    uname = Column(String(50), comment='用户名称')
    bname = Column(String(20), comment='备案人')
    nyear = Column(INTEGER(11), server_default=text("'0'"))
    start_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"), comment='项目开通时间')
    end_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"), comment='项目到期时间')
    photo = Column(String(100), comment='中心认证照')
    content = Column(Text)
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='添加时间')
    iphone_key = Column(String(255))
    android_key = Column(String(255))
    iphone_version = Column(INTEGER(5), nullable=False, server_default=text("'1'"))
    logo = Column(String(100))
    android_version = Column(INTEGER(5), nullable=False, server_default=text("'0'"))
    android_version2 = Column(String(50), nullable=False, server_default=text("''"))
    logo2 = Column(String(100))
    view_img = Column(String(100))
    iphone_app_url = Column(String(255))
    android_app_url = Column(String(255))
    android_appkey = Column(String(255))
    android_master_secret = Column(String(255))
    iphone_pem = Column(String(255))
    weixinid = Column(String(255), comment='微信号')
    baiduid = Column(String(255), comment='百度市场id')
    baidukey = Column(String(255), comment='百度市场key')
    key = Column(String(255), comment='key=（appkey-1）*2')
    ispcshop = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='是否开通pc')
    current_version = Column(CHAR(50), nullable=False, server_default=text("'5.0.00'"), comment='当前版本')
    tuiguang = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='开通推广')
    pcnav_color = Column(String(50), nullable=False, server_default=text("'c81622'"), comment='pc版导航条颜色')
    ahover_color = Column(String(50), nullable=False, server_default=text("'f97293'"), comment='pc版导航条鼠标hover值')
    theme_color = Column(String(20), server_default=text("'#21b7a1'"), comment='app主题颜色')
    version = Column(String(200), nullable=False)


class LrAdminuser(db.Model):
    __tablename__ = 'lr_adminuser'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='用户表：包括后台管理员、商家会员和普通会员')
    name = Column(String(20), nullable=False, comment='登陆账号')
    uname = Column(String(10), comment='昵称')
    pwd = Column(String(50), nullable=False, comment='MD5密码')
    qx = Column(TINYINT(4), nullable=False, server_default=text("'5'"), comment='权限 4超级管理员 5普通管理员')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='创建日期')
    _del = Column('del', TINYINT(2), nullable=False, server_default=text("'0'"), comment='状态')


class LrAttribute(db.Model):
    __tablename__ = 'lr_attribute'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='属性名称')
    attr_name = Column(String(20), nullable=False)
    sort = Column(INTEGER(3), nullable=False, comment='排序')
    addtime = Column(INTEGER(11), nullable=False, comment='添加时间')


class LrBrand(db.Model):
    __tablename__ = 'lr_brand'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='产品品牌表')
    name = Column(String(100), nullable=False, comment='品牌名称')
    brandprice = Column(Float(8), nullable=False, server_default=text("'0.00'"), comment='起始价格')
    photo = Column(String(100), comment='图片')
    type = Column(TINYINT(2), server_default=text("'0'"), comment='是否推荐')
    addtime = Column(INTEGER(11), comment='添加时间')
    shop_id = Column(INTEGER(11), server_default=text("'0'"), comment='店铺id')


class LrCategory(db.Model):
    __tablename__ = 'lr_category'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='分类id')
    tid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='父级分类id')
    name = Column(String(50), nullable=False, comment='栏目名称')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='添加时间')
    concent = Column(String(255), comment='栏目简介')
    bz_1 = Column(String(100), comment='缩略图')
    bz_2 = Column(String(255), comment='备注字段')
    bz_3 = Column(String(100), comment='图标')
    bz_4 = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='备用字段')
    bz_5 = Column(String(100), comment='推荐略缩图')


class LrChinaCity(db.Model):
    __tablename__ = 'lr_china_city'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='主键id')
    tid = Column(INTEGER(11), server_default=text("'0'"), comment='父级id')
    name = Column(String(255))
    code = Column(String(255))
    head = Column(String(1))
    type = Column(TINYINT(2), nullable=False, server_default=text("'0'"))


class LrFankui(db.Model):
    __tablename__ = 'lr_fankui'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True)
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    message = Column(String(255), nullable=False, comment='反馈内容')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='反馈时间')


class LrGroupJoin(db.Model):
    __tablename__ = 'lr_group_joins'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='团购用户信息表')
    hid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='hot id 团购id')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户id')
    jointime = Column(INTEGER(10), nullable=False, server_default=text("'0'"), comment='参团时间')
    status = Column(INTEGER(2), nullable=False, server_default=text("'0'"), comment='0:报名中 1:待付款 2:已经生成订单 3:取消 4:过期')


class LrGuanggao(db.Model):
    __tablename__ = 'lr_guanggao'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='子页广告管理表')
    name = Column(String(20), comment='广告名称')
    photo = Column(String(100), comment='图片')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='添加时间')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    type = Column(Enum('product', 'news', 'partner', 'index'), server_default=text("'index'"), comment='广告类型')
    action = Column(String(255), nullable=False, comment='链接值')
    position = Column(TINYINT(2), server_default=text("'1'"), comment='广告位置 1首页轮播')


class LrGuige(db.Model):
    __tablename__ = 'lr_guige'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='规格id')
    pid = Column(INTEGER(11), nullable=False, comment='产品id')
    attr_id = Column(INTEGER(11), server_default=text("'0'"), comment='产品属性id')
    name = Column(String(50), nullable=False, comment='规格名称')
    price = Column(DECIMAL(9, 2), server_default=text("'0.00'"), comment='规格价格')
    stock = Column(INTEGER(11), nullable=False, comment='库存')
    img = Column(String(100), comment='属性图片')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='添加时间')


class LrHot(db.Model):
    __tablename__ = 'lr_hot'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(8), primary_key=True, comment='团购商品表')
    pid = Column(INTEGER(8), nullable=False, server_default=text("'0'"), comment='商品ID')
    price = Column(DECIMAL(8, 2), server_default=text("'0.00'"), comment='价格')
    start = Column(INTEGER(10), server_default=text("'0'"), comment='开团时间')
    end = Column(INTEGER(10), server_default=text("'0'"), comment='结束时间')
    addtime = Column(INTEGER(10), server_default=text("'0'"), comment='添加时间')
    sort = Column(INTEGER(10), server_default=text("'0'"), comment='排序')
    type = Column(INTEGER(2), server_default=text("'0'"))
    amount = Column(INTEGER(5), server_default=text("'0'"), comment='团购 开团的数量')
    count = Column(INTEGER(6), server_default=text("'0'"), comment='团购 参团人数')
    hstatus = Column(INTEGER(2), server_default=text("'0'"), comment='是否被删除 1已被删除')


class LrIndeximg(db.Model):
    __tablename__ = 'lr_indeximg'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True)
    cid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='分类ID')
    name = Column(String(50), comment='分类产品')
    photo = Column(String(100), nullable=False, comment='图片')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序')


class LrNew(db.Model):
    __tablename__ = 'lr_news'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True)
    cid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='新闻分类ID')
    name = Column(String(50), nullable=False, comment='新闻标题')
    digest = Column(String(255), comment='摘要')
    content = Column(Text, comment='新闻内容')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='发表时间')
    click = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='点击量')
    pinglun = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='评论数量')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序')
    photo = Column(String(100), comment='简介图片')
    source = Column(String(20), comment='来源')


class LrNewsCat(db.Model):
    __tablename__ = 'lr_news_cat'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='新闻分类表')
    name = Column(String(50), comment='分类名称')
    addtime = Column(INTEGER(11), comment='添加时间')


class LrOrder(db.Model):
    __tablename__ = 'lr_order'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='订单id')
    order_sn = Column(String(20), nullable=False, comment='订单编号')
    pay_sn = Column(String(20), comment='支付单号')
    shop_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商家ID')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    price = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"), comment='价格')
    amount = Column(DECIMAL(9, 2), server_default=text("'0.00'"), comment='优惠后价格')
    addtime = Column(INTEGER(10), nullable=False, server_default=text("'0'"), comment='购买时间')
    _del = Column('del', TINYINT(2), nullable=False, server_default=text("'0'"), comment='删除状态')
    type = Column(Enum('weixin', 'alipay', 'cash'), server_default=text("'weixin'"), comment='支付方式')
    price_h = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"), comment='真实支付金额')
    status = Column(TINYINT(2), nullable=False, server_default=text("'10'"), comment='订单状态码：0,已取消; 10,待付款; 20,待发货; 30,待收货; 40,待评价; 50,交易完成; 51,交易关闭')
    vid = Column(INTEGER(11), server_default=text("'0'"), comment='优惠券ID')
    receiver = Column(String(15), nullable=False, comment='收货人')
    tel = Column(CHAR(15), nullable=False, comment='联系方式')
    address_xq = Column(String(50), nullable=False, comment='地址详情')
    code = Column(INTEGER(11), nullable=False, comment='邮编')
    post = Column(INTEGER(11), comment='快递ID')
    remark = Column(String(255), comment='买家留言')
    post_remark = Column(String(255), nullable=False, comment='邮费信息')
    product_num = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='商品数量')
    trade_no = Column(String(50), comment='微信交易单号')
    kuaidi_name = Column(String(10), comment='快递名称')
    kuaidi_num = Column(String(20), comment='运单号')
    back = Column(Enum('1', '2', '0'), server_default=text("'0'"), comment='标识客户是否有发起退款1申请退款 2已退款')
    back_remark = Column(String(255), comment='退款原因')
    back_addtime = Column(INTEGER(11), server_default=text("'0'"), comment='申请退款时间')
    order_type = Column(TINYINT(2), server_default=text("'1'"), comment='订单类型 1普通订单 2抢购订单')


class LrOrderProduct(db.Model):
    __tablename__ = 'lr_order_product'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='订单商品信息表')
    pid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商品id')
    pay_sn = Column(String(20), comment='支付单号')
    order_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='订单id')
    name = Column(String(50), nullable=False, comment='产品名称')
    price = Column(DECIMAL(8, 2), nullable=False, server_default=text("'0.00'"), comment='价格')
    photo_x = Column(String(100), comment='商品图')
    pro_buff = Column(String(255), comment='产品属性')
    addtime = Column(INTEGER(11), nullable=False, comment='添加时间')
    num = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='购买数量')
    pro_guige = Column(String(50), comment='规格id和规格名称')


class LrPost(db.Model):
    __tablename__ = 'lr_post'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='物流快递表')
    name = Column(String(20), nullable=False, comment='快递名称')
    price = Column(DECIMAL(11, 0), nullable=False, server_default=text("'0'"), comment='价格')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序')
    price_max = Column(DECIMAL(11, 0), nullable=False, server_default=text("'0'"), comment='满多少包邮')
    pid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商品ID')


class LrProduct(db.Model):
    __tablename__ = 'lr_product'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='产品表')
    shop_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商铺id')
    brand_id = Column(INTEGER(11), comment='品牌ID')
    name = Column(String(50), nullable=False, comment='产品名称')
    intro = Column(String(100), comment='广告语')
    pro_number = Column(String(100), comment='产品编号')
    price = Column(DECIMAL(8, 2), nullable=False, server_default=text("'0.00'"), comment='价格')
    price_yh = Column(DECIMAL(8, 2), nullable=False, server_default=text("'0.00'"), comment='优惠价格')
    price_jf = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='赠送积分')
    photo_x = Column(String(100), comment='小图')
    photo_d = Column(String(100), comment='大图')
    photo_string = Column(Text, comment='图片组')
    content = Column(Text, comment='商品详情')
    addtime = Column(INTEGER(11), comment='添加时间')
    updatetime = Column(INTEGER(11), nullable=False, comment='修改时间')
    sort = Column(INTEGER(11), server_default=text("'0'"), comment='排序')
    renqi = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='人气')
    shiyong = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='购买数')
    num = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='数量')
    type = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='是否推荐 1推荐  0不推荐')
    _del = Column('del', TINYINT(2), nullable=False, server_default=text("'0'"), comment='删除状态')
    del_time = Column(INTEGER(10), server_default=text("'0'"), comment='删除时间')
    pro_buff = Column(String(255), comment='产品属性')
    cid = Column(INTEGER(11), nullable=False, comment='分类id')
    company = Column(CHAR(10), comment='单位')
    is_show = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='是否新品')
    is_down = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='下架状态')
    is_hot = Column(TINYINT(1), server_default=text("'0'"), comment='是否热卖')
    is_sale = Column(TINYINT(1), server_default=text("'0'"), comment='是否折扣')
    start_time = Column(INTEGER(11), server_default=text("'0'"), comment='抢购开始时间')
    end_time = Column(INTEGER(11), server_default=text("'0'"), comment='抢购结束时间')
    pro_type = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='产品类型 1普通 2抢购产品')


class LrProductDp(db.Model):
    __tablename__ = 'lr_product_dp'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='产品评论表')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='会员id')
    pid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商品id')
    order_id = Column(INTEGER(11), server_default=text("'0'"), comment='评论订单id')
    num = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='评分数')
    concent = Column(String(255))
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='评论时间')
    audit = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='审核状态')
    reply_status = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='回复状态')
    reply_content = Column(Text, comment='回复内容')
    reply_time = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='回复时间')


class LrProductSc(db.Model):
    __tablename__ = 'lr_product_sc'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='商品收藏表')
    pid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商品ID')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    status = Column(TINYINT(2), server_default=text("'1'"), comment='状态 1正常 0删除')


class LrProgram(db.Model):
    __tablename__ = 'lr_program'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='小程序配置表')
    xcxid = Column(String(50), comment='小程序ID')
    key = Column(String(50), comment='小程序key')
    wxid = Column(String(50), comment='公众号ID')
    mch = Column(String(50), comment='小程序支付商户号')
    seckey = Column(String(50))
    title = Column(String(20), nullable=False, comment='小程序名称')
    name = Column(String(20), nullable=False, comment='负责人')
    describe = Column(String(200), comment='简单描述')
    logo = Column(String(100), comment='logo')
    copyright = Column(String(100), comment='版权信息')
    service_wx = Column(String(50), comment='平台客服微信号')
    tel = Column(String(20), comment='平台客服电话')
    email = Column(String(20), comment='邮箱')
    uptime = Column(INTEGER(11), server_default=text("'0'"), comment='修改时间')


class LrSccat(db.Model):
    __tablename__ = 'lr_sccat'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='产品品牌表')
    name = Column(String(100), nullable=False, comment='品牌名称')
    addtime = Column(INTEGER(11), comment='添加时间')
    shop_id = Column(INTEGER(11), server_default=text("'0'"), comment='店铺id')


class LrSearchRecord(db.Model):
    __tablename__ = 'lr_search_record'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='搜索记录表')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='会员ID')
    keyword = Column(String(255), nullable=False, comment='搜索内容')
    num = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='搜索次数')
    addtime = Column(INTEGER(11), server_default=text("'0'"), comment='搜索时间')


class LrShangchang(db.Model):
    __tablename__ = 'lr_shangchang'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True)
    cid = Column(INTEGER(11), server_default=text("'0'"), comment='店铺类别id')
    name = Column(String(20), nullable=False, comment='店铺名称')
    uname = Column(String(10), nullable=False, comment='负责人名称')
    logo = Column(String(100), comment='店铺LOGO')
    vip_char = Column(String(100), comment='店铺公告、广告图')
    sheng = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='省id')
    city = Column(INTEGER(11), server_default=text("'0'"), comment='市id')
    quyu = Column(INTEGER(11), server_default=text("'0'"), comment='区域id')
    address = Column(String(255), comment='地址')
    address_xq = Column(String(255), comment='省市区+地址')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序')
    location_x = Column(String(20), nullable=False, server_default=text("'0'"), comment='纬度')
    location_y = Column(String(20), nullable=False, server_default=text("'0'"), comment='经度')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='创建日期')
    updatetime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='更新日期')
    content = Column(Text, comment='店铺介绍')
    intro = Column(String(200), comment='店铺广告语')
    grade = Column(INTEGER(2), nullable=False, server_default=text("'10'"), comment='评分等级1~10')
    tel = Column(CHAR(15), comment='联系电话')
    utel = Column(CHAR(15), comment='负责人手机')
    status = Column(TINYINT(2), server_default=text("'1'"), comment='显示/隐藏')
    type = Column(TINYINT(2), nullable=False, server_default=text("'0'"))
    qq = Column(String(255), comment='qq')
    wx_appid = Column(String(32), comment='APPID')
    wx_mch_id = Column(String(32), comment='微信支付商户号')
    wx_key = Column(String(100), comment='API密钥')
    wx_secret = Column(String(64), comment='AppSecret是APPID对应的接口密码')


class LrShangchangDp(db.Model):
    __tablename__ = 'lr_shangchang_dp'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='店铺收藏表')
    shop_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商铺id')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='会员id')
    grade = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='评分数')
    concent = Column(String(255), comment='评论内容')
    addtime = Column(INTEGER(11))
    audit = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='审核状态')


class LrShangchangSc(db.Model):
    __tablename__ = 'lr_shangchang_sc'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='会员店铺收藏记录表')
    shop_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='店铺ID')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    status = Column(TINYINT(2), server_default=text("'1'"), comment='收藏状态 1收藏 0删除')


class LrShoppingChar(db.Model):
    __tablename__ = 'lr_shopping_char'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='购物车表')
    pid = Column(INTEGER(11), nullable=False, comment='商品ID')
    price = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"), comment='商品单价')
    num = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='数量')
    buff = Column(String(255), nullable=False, comment='属性（序列化格式）')
    addtime = Column(INTEGER(10), nullable=False, comment='添加时间')
    uid = Column(INTEGER(11), nullable=False, comment='用户ID')
    shop_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商家ID')
    gid = Column(INTEGER(11), server_default=text("'0'"), comment='规格id')
    type = Column(TINYINT(2), server_default=text("'2'"), comment='0是热卖，1是团购，2是普通商品')


class LrUser(db.Model):
    __tablename__ = 'lr_user'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='用户表：包括后台管理员、商家会员和普通会员')
    name = Column(String(20), nullable=False, comment='登陆账号')
    uname = Column(String(10), comment='昵称')
    pwd = Column(String(50), nullable=False, comment='MD5密码')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='创建日期')
    jifen = Column(Float(11), server_default=text("'0'"), comment='积分')
    photo = Column(String(255), comment='头像')
    tel = Column(CHAR(15), comment='手机')
    qq_id = Column(String(20), nullable=False, server_default=text("'0'"), comment='qq')
    email = Column(String(50), comment='邮箱')
    sex = Column(TINYINT(2), nullable=False, server_default=text("'0'"), comment='性别')
    _del = Column('del', TINYINT(2), nullable=False, server_default=text("'0'"), comment='状态')
    openid = Column(String(50), nullable=False, comment='授权ID')
    source = Column(String(10), nullable=False, comment='第三方平台(微信，QQ)')


class LrUserVoucher(db.Model):
    __tablename__ = 'lr_user_voucher'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='会员优惠券领取记录')
    uid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='会员ID')
    vid = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='优惠券id')
    shop_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='商铺ID')
    full_money = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"), comment='满多少钱')
    amount = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"), comment='减多少钱')
    start_time = Column(INTEGER(11), server_default=text("'0'"), comment='开始时间')
    end_time = Column(INTEGER(11), server_default=text("'0'"), comment='结束时间')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='领取时间')
    status = Column(TINYINT(2), server_default=text("'1'"), comment='使用状态 1未使用 2已使用 3已失效')


class LrVoucher(db.Model):
    __tablename__ = 'lr_voucher'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='店铺优惠券表')
    shop_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='店铺ID')
    title = Column(String(100), comment='优惠券名称')
    full_money = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"), comment='满多少钱')
    amount = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"), comment='减多少钱')
    start_time = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='开始时间')
    end_time = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='结束时间')
    point = Column(INTEGER(11), server_default=text("'0'"), comment='所需积分')
    count = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='发行数量')
    receive_num = Column(INTEGER(11), server_default=text("'0'"), comment='领取数量')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='添加时间')
    type = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='优惠券类型')
    _del = Column('del', TINYINT(1), server_default=text("'0'"), comment='删除状态')
    proid = Column(Text, comment='产品ID')


class LrWeb(db.Model):
    __tablename__ = 'lr_web'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='单网页信息表：关于我们、客服中心等')
    pid = Column(INTEGER(11), server_default=text("'0'"))
    uname = Column(String(255), comment='名称1')
    ename = Column(String(255), comment='名称2')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序')
    concent = Column(MEDIUMTEXT, comment='内容介绍')
    addtime = Column(INTEGER(11), server_default=text("'0'"), comment='发表时间')


class LrZhuti(db.Model):
    __tablename__ = 'lr_zhuti'
    __table_args__ = {'schema': '50mkw'}
    __bind_key__ = '50mkw'

    id = Column(INTEGER(11), primary_key=True, comment='子页广告管理表')
    name = Column(String(20), comment='广告名称')
    subtitle = Column(String(100))
    price_info = Column(String(20))
    photo = Column(String(100), comment='图片')
    addtime = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='添加时间')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    type = Column(Enum('product', 'news', 'partner', 'index'), server_default=text("'index'"), comment='广告类型')
    action = Column(String(255), nullable=False, comment='链接值')
    position = Column(TINYINT(2), server_default=text("'1'"), comment='广告位置 1首页轮播')

