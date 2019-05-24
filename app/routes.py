from app import app
from flask import render_template, flash,url_for, redirect
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from .models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.exts import db
from app.forms import RegistrationForm


#**********************************************************
@app.route("/")
@app.route("/index")
# @login_required
def index():
    user = {"username": "duke"}
    posts = [
        {
            'author': {'username': '刘欢'},
            'body': "这是第一个模板 --1"

        },
        {
            'author': {"username": '山景'},
            'body': "这是第二个模板 --2"
        }
    ]
    return render_template('index.html', user=user, posts=posts)

@app.route('/login', methods=["POST","GET"])
def login():

    """"登陆"""
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))


    # 创建一个表单实力
    form = LoginForm()
    #对表格数据进行验证
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回Nono
        user = User.query.filter_by(username=form.username.data).first()
        # 判断用户不存在或者密码错误
        if user is None or not user.check_password(form.password.data):
            # 如果用户名不正确就会闪现这条信息
            flash("无效的用户名")
        # flash('用户登录的登录名是:{},是否记住我:{}'.format(form.username.data,form.remember_me.data))
            # 然后重定向到登陆页面
            return redirect(url_for('index'))
        # 这是一个非常方便的方法，但用户名和密码都正确的时候，来解决用户是否记住登录状态的问题
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录的时跳转至登陆页面的地址
        next_page = request.args.get('next')
        # 如股next_page记录的地址不存在那么久返回首页
        if not next_page or url_parse(next_page).netloc() != "":
            next_page = url_for('index')

        # 综上，登录后那么重定向跳转的页面，要么跳转到首页
        return redirect(next_page)

    return render_template('login.html', title = "登录", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)
