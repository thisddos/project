#!/usr/bin/env python
__author__ = 'XeanYu'
from exts import db
from flask_login import UserMixin
from exts import login_manager
from func.date import now
# Log Users
class Users(db.Model,UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer,primary_key=True)

    username = db.Column(db.String(64),unique=True,nullable=False,index=True)

    password = db.Column(db.String(124),nullable=False,index=True)

    mail = db.Column(db.String(124),index=True,nullable=False)

    code = db.Column(db.String(40),nullable=False)

    sgin_up_date = db.Column(db.String(64))

    vip = db.Column(db.String(64),default=0) # judgment have vip
    attract = db.Column(db.Integer,default=0) #


    # 表中没有id字段，自己定义返回uid字段
    def get_id(self):
        return self.uid

@login_manager.user_loader
def user_load(id):
    return Users.query.get(id)

# Login log
class Login_logs(db.Model):
    __tablename__ = 'login_logs'

    id = db.Column(db.Integer,primary_key=True) # id => 主键

    username = db.Column(db.String(64),index=True) # 用户的用户名

    browser = db.Column(db.String(124),index=True) # 用户使用的浏览器

    device = db.Column(db.String(124),index=True)  # 用户使用的设备

    os = db.Column(db.String(124),index=True)  # 用户的操作系统

    ip = db.Column(db.String(64),index=True) # 用户IP地址

    platform = db.Column(db.String(12),index=True) # user's platform

    login_date = db.Column(db.String(64),default=now())