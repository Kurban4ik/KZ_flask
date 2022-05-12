# -*- coding: utf-8 -*-
import datetime
import os

from waitress import serve
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort, Api

from blueprints.api_blueprint import api_blueprint
from changer import pixelator, liner, nihil, edges
from forms.photos import NewsForm
from forms.user import RegisterForm, LoginForm
from data.photos import News
from data.users import User
from data import db_session

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '''static/inner'''
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.register_blueprint(api_blueprint)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    serve(app, host='0.0.0.0', port=5000)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    # создается запись, фотография сохраняется в папке static/inner/деньчасминутасекунда создания/
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        if request.files["photo"].content_type.split('/')[-1] not in ['png', 'jpg', 'jpeg', 'gif']:
            return 'bad request'
        file = request.files["photo"]
        now = datetime.datetime.now()
        now = str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
        os.mkdir(f'./static/inner/{now}')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + f'/{now}', file.filename))
        news.photo = f'{now}/{file.filename}'
        if form.f.data == '1':
            pixelator(now, file.filename)
        elif form.f.data == '2':
            liner(now, file.filename)
        elif form.f.data == '4':
            edges(now, file.filename)
        else:
            nihil(now, file.filename)
        news.filter = form.f.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()

        return redirect('/')
    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    for i in news:
        print(i.photo)
    return render_template("index.html", news=news)


@app.route('/img/<int:date>')
def get_img(date):
    username = request.args.get('name')
    strs = str(date) + '/' + username
    return render_template('img.html', photo=strs)


if __name__ == '__main__':
    main()
