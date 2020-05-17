"# 50mkw" 

使用下面的命令生成依赖的库

`pip freeze > requirements.txt`

`virtualenv -p /usr/bin/python2.7 venv`

## gunicorn
搭建好以后跑一下，没问题的话就可以。但是这是基于flask自带的web服务器，所以在阿里云上要用gunicorn来代替，它能让你的程序跑起来。
### 安装
`pip install gunicorn`
### 使用gunicorn 启动工程
通过命令行启动它`gunicorn -w worker数量 -b ip:端口号 运行文件名：flask实例名`例：`gunicorn -w 3 -b 127.0.0.1:5000 helloworld:app`后台运行`gunicorn -D -w 3 -b 127.0.0.1:5000 helloworld:app`

gunicorn命令的参数:
- \- D 表示后台运行
- \- w 表示有3 个 工作线程（感觉有些类似 nginx 的 master-worker 模型）
- \- b 指定ip 和端口
- \- 这里采用本机访问， 主要是为了使用nginx 进行代理， 方便管理
- \- application 表存放 写着全局变量 app 的那个工程文件夹
- \- 在我们的这个工程中， 即包含 init.py 的那个文件
- \- app 为全局变量 （app = Flask(\_\_name\_\_)）
- \- ps： 在下面图示文件夹中运行 gunicorn 指令

到达这一步，可以在linux服务器本地上访问(127.0.0.1:8000)
注意：如果想通过本地Windows访问的话,还需安装nginx,把ip改为阿里云的公网的ip.

## nginx
详细流程参考 [https://www.runoob.com/linux/nginx-install-setup.html]()

nginx安装
```
cd /usr/local/src
wget http://nginx.org/download/nginx-1.1.10.tar.gz
tar -zxvf nginx-1.1.10.tar.gz
cd nginx-1.1.10
./configure
make
make install
```
nginx配置

1. 安装完的nginx 在 /usr/local/nginx 目录下， 我们可以找到conf文件夹下的 nginx.conf 文件， 将其修改
2. 添加nginx 需要监听的端口信息
```
server {
    listen 8001;
    server_name localhost;
    location /{
        #root html;
        #index index.html index.htm;
        # 请求转发到gunicorn服务器
        proxy_pass http://127.0.0.1:5000;
        # 请求转发到多个gunicorn服务器
        # proxy_pass http://flask;
        # 设置请求头，并将头信息传递给服务器端 
        proxy_set_header Host $host;
        # 设置请求头，传递原始请求ip给 gunicorn 服务器
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

实际上， 我们将外部通过 8088 端口发送过来的请求， 代理给了 127.0.0.1:5000 也就是我们的 flask 项目
部署项目时 请求流程

Client <===> Nginx <===> gunicorn <===> Flask服务

记得修改完配置文件，需要重新载入配置文件！！！

检查配置文件nginx.conf是否正确
`$ /usr/local/nginx/sbin/nginx -t`

启动nginx
`$ /usr/local/nginx/sbin/nginx`

nginx其他命令

```
$ /usr/local/nginx/sbin/nginx -s reload # 重新载入配置文件
$ /usr/local/nginx/sbin/nginx -s reopen # 重启nginx
$ /usr/local/nginx/sbin/nginx -s stop # 停止nginx
```

nginx快速停止

```
$ ps -ef | grep nginx #查看进程号
$ kill -9 25276 #杀死进程
$ pkill -9 nginx # 强制停止
```

如果有自己的域名和ssl证书，将calculator.conf配置文件修改如下:

```
server{
    listen         443;
    server_name    your.domain;
    ssl on;
    ssl_certificate path/to/your/ssl.pem;
    ssl_certificate_key path/to/your/ssl.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    charset UTF-8;

    client_max_body_size 75M;

    location ~ ^/calculate {
        uwsgi_pass unix:///path/to/calculator/calculator.sock;
        include /etc/nginx/uwsgi_params;
    }
}
```

重启nginx服务器，访问服务器的443端口即可访问calculate接口，如https://服务器域名/calculate?formula=2*3-4

如果你只有自己的域名而没有ssl证书，可以去申请免费的ssl证书或者参考此网址配置（https://certbot.eff.org/#ubuntuxenial-nginx）。
如果你没有自己的域名甚至没有自己的服务器，请出门右转阿里云或左转腾讯云自行购买。