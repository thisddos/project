__author__ = 'XeanYu'

"""
this modle is main.views

"""

from flask import render_template,session,url_for,request,jsonify,redirect
from flask_login import login_required,login_user,logout_user
from . import main
from random import randint # make random_code
from exts import db
from models import Users,Login_logs
from func.password import * # use bcrypt make password
from func.date import now
from func.agent import *


# index view route
@main.route('/')
def index():
    return 'index'

# sgin_up view route
@main.route('/registered/',methods=['GET','POST']) # allow GET and POST request
def sgin_up():
    """
    此路由用来注册用户
    :return:
    """
    if request.method == 'GET': # GET
        global up_random_code
        up_random_code = randint(10000, 99999)  # 生成5位纯数字验证码
        return render_template('sgin_up.html',num_code=up_random_code)

    else: # POST
        username = request.form.get('username').strip() # 获取用户名
        email = request.form.get('email').strip() # 获取邮箱
        password = request.form.get('password').strip() # 获取密码
        code = request.form.get('code').strip() # 获取私密代码
        random_code_form = request.form.get('random_code').strip() # 获取随机码

        if all([username,email,password,code,random_code_form]):

            # 判断验证码是否正确
            if str(random_code_form) == str(up_random_code):

                add_db = Users.query.filter_by(username=username).first()
                if not add_db: # 判断数据是否存在当前用户，如果不存在，则添加到数据库

                    password = passwd_bcrypt(password)
                    add_db = Users(username=username,mail=email,password=password,code=code,sgin_up_date = now())
                    db.session.add(add_db)
                    db.session.commit() # 提交值数据库(Fluash())
                    return jsonify(msg='redirect')

                else:
                    return jsonify(msg='用户已存在')

            else:
                return jsonify(msg='输入的随机码不正确')

        else:
            return jsonify(msg='输入的信息不完整')

# sgin_in  view route
@main.route('/login/',methods=['GET','POST'])
def sgin_in():
    """
    此路由用来用户登录
    :return:
    """
    # if user not login ==> GO TO login
    if request.method == 'GET':
        global lg_random_code
        lg_random_code = randint(10000,99999)
        return render_template('sgin_in.html',num_code=lg_random_code) # return template and export make_random_code

    if request.method == 'POST':

        """
        strip() => cut space
        """
        username = request.form.get('username').strip() # get user's username
        password = request.form.get('password').strip() # get user's password
        random_code_form = request.form.get('random_code').strip() # get user's input random code

        # get user's msg
        user_ip = str(request.remote_addr) # get user's IP
        user_agent = str(request.user_agent) # get user's User-Agent
        browser = str(request.user_agent.browser) # get user's browser
        os = str(request.user_agent.platform)  # get user's os

        if all([username,password,random_code_form]): # judgmeng user's input not is None
            if str(lg_random_code) == str(random_code_form): # judgment random_code == user input random_code

                # search user for Users'Table
                login = Users.query.filter_by(username=username).first()
                if login: # find user

                    if check_passwd(password,login.password.encode()): # judgment password equal

                        # add user login log
                        logadd = Login_logs(
                            username=username,
                            browser=browser,
                            device=is_device(user_agent),
                            os=os,
                            ip=user_ip,
                            platform=user_msg(user_agent)
                        ) #


                        db.session.add(logadd) # add 'logadd' object to 'db.session'
                        db.session.commit() # commit session to DB's Login_logs
                        login_user(login)
                        return jsonify(msg='login') # return views to Ajax ==> Login success

                    else: # password error
                        return jsonify(msg='密码错误!')

                else:   # don's search username
                    return jsonify(msg='没有此用户,请注册')

            else:   # random error
                return jsonify(msg='随机码输入错误')

        else:  # fill message have None
            return jsonify(msg='请输入完整信息')

    # if user login

# password lost page  view route
@main.route('/getpass/',methods=['GET','POST'])
def getpass():

    """
    change password page
    :return:
    """
    if request.method == 'GET':
        return render_template('getpass.html')

    else:
        username = request.form.get('user').strip()
        code = request.form.get('user').strip()
        newpass = request.form.get('newpass').strip()

            # use all() function => True
        if all([username,code,newpass]):

            # find username for DB
            user = Users.query.filter_by(username=username).first()
            if user:
                if str(code) == str(user.code):
                    user.password = str(passwd_bcrypt(newpass))
                    db.session.add(user)
                    db.session.commit()
                    return jsonify(msg='change')

                else:
                    return jsonify(msg='私密代码不正确!')

            else:
                return jsonify(msg='没有此用户')

        else:
            return jsonify(msg='请填写好信息')

@main.route('/user/',methods=['GET','POST'])
@login_required
def console():
    return render_template('user.html')

@main.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.sgin_in'))
