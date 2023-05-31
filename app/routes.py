# 从app模块中即从__init__.py中导入创建的app应用
from app import app, db
from flask import render_template, flash, redirect, url_for, request, g
from app.form import LoginForm, RegistrationForm, SearchForm
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from app.vediocrawl import BiliCrawler
from datetime import datetime
import pymysql

# 建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchForm()
    if form.validate_on_submit():
        crawl = BiliCrawler()
        detail_url, title = crawl.getAudioLink(form.content.data)
        commit_time = datetime.utcnow()
        post = Post(body=title, timestamp=commit_time, user_id=current_user.get_id())
        db.session.add(post)
        db.session.commit()
        return redirect(detail_url)

    return render_template('index1.html', title='我的', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # 对表格数据进行验证
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        # 判断用户不存在或者密码不正确
        if user is None or not user.check_password(form.password.data):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user, remember=form.remember_me.data)

        # 此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 综上，登录后要么重定向至跳转前的页面，要么跳转至首页

        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)


@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/history', methods=['GET', 'POST'])
def history():
    res_1 = []
    res_2 = []
    user_id = current_user.get_id()

    db_1 = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='bilibili')
    cursor = db_1.cursor()
    sql = 'select * from post where user_id={}'.format(user_id)
    res_1 = cursor.execute(sql)
    res_2 = cursor.fetchall()

    return render_template('history.html', posts=res_2)

@app.before_request
def my_before_request():
    user_id = current_user.get_id()
    if user_id:
        user = User.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

@app.context_processor
def my_context_processor():
    return {'user': g.user}

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
