from app import app
from  flask import render_template,flash,redirect,url_for
from app.forms import LoginForm
from flask_login import current_user,login_user
from app.models import User
import os
import gzip
from app.checkurl import *
from app.ipcheck import getIP
import socket
@app.route('/')
@app.route('/index')
def index():
    user={'username':'duke'}
    posts=[
        {
            'author':{'username':'刘'},
            'body':'这是模版模块中的循环例子~1'
    
        },
    {
            'author': {'username': '忠强'},
            'body': '这是模版模块中的循环例子~2'
    }
    
    ]
    return render_template('index.html',title='我的',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        flash('用户登录的用户名是：{},是否记住我:{}'.format(form.username.data,form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('login.html',title='登录',form=form)

@app.route('/log',methods=['GET','POST'])
def log():
    import sys
    import os 
    import time
    import datetime
    logpath='/root/GetDayLog/tmp/'
    date=time.strftime("%Y%m%d",time.localtime())
    # print(date)
    path=os.path.join(logpath,date)
    domain=os.listdir(path)
    domain.sort()
    dic={}
    dicCDN={}
    #检测文件夹下所有的日志
    # for do in domain:
    #     dir=os.path.join(path,do)
    #     with gzip.open(dir,'r') as pf:
    #         for line in pf:
    #             if b'NULL' not in line.split()[8]:
    #                 url=str(line.split()[8])
    #                 code=str(line.split()[7])
    #                 # print(type(line))
    #                 # print(line)
    #                 if code != "b'403'":
    #                     dic[url.split("/")[2]]=code
    #             # print(dic)
    #检测文件夹下最新的日志
    log=domain[-1]
    dir=os.path.join(path,log)
    with gzip.open(dir,'r') as pf:
        for line in pf:
            if b'NULL' not in line.split()[8]:
                url=str(line.split()[8])
                code=str(line.split()[7])
                domain=url.split("/")[2]
                # print(type(line))
                # print(line)
                if code != "b'403'":
                    dic[url.split("/")[2]]=code
                    cdn=CdnCheck(url).check()
                    dicCDN[domain]=[cdn,getIP(domain)]

    
    return render_template('log.html',dic=dic,dicCDN=dicCDN,dir=dir)

#     def read_gz_file(path):
#     if os.path.exists(path):
#         with gzip.open(path,'r') as pf:
#             for line in pf:
#                 yield line
    
#     else:
#         print('the path [{}] is not exist!'.format(path))

# con=read_gz_file('2018080123-sn.163ar.cn.gz')
# if getattr(con,'__iter__',None):
#     for line in con:
#         print(line)

