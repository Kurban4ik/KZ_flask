# -*- coding: utf-8 -*-
import datetime
import os

from waitress import serve
from flask import Flask, render_template, redirect, request, abort, send_from_directory, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from blueprints.api_blueprint import api_blueprint
from changer import ImageChange
from forms.photos import NewsForm
from forms.user import RegisterForm, LoginForm
from data.photos import News
from data.users import User
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# внесение изменений в конфигурацию
app.config['UPLOAD_FOLDER'] = '''static/inner'''
app.config['SECRET_KEY'] = 'AvdsvSPDolfSD123pls90sg908SDFuj009sfd90'
# регистрация блюпринтов
app.register_blueprint(api_blueprint)



@app.route('/register', methods=['GET', 'POST'])
def reqister():  # регистрация пользователя
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
def login():  # авторизация
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
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    print(cur_dir)
    db_session.global_init("db/blogs.db")
    app.run()
    #serve(app, port=5000)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():  # добавление новостей
    form = NewsForm()
    if form.validate_on_submit():  # проверка валидности
        db_sess = db_session.create_session()
        news = News()
        if request.files["photo"].content_type.split('/')[-1] not in ['png', 'jpg', 'jpeg']:  # проверка формата
            return 'bad request'
        file = request.files["photo"]
        # now это переменная определяющая момент времени в который занесли изображение,
        # оно нужно для дифференциации одинаковых изображений
        now = datetime.datetime.now()
        now = str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
        # создание директории в которой будет хранится необработанное изображение
        os.mkdir(f'./static/inner/{now}')
        # сохранение фото в эту директорию
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + f'/{now}', file.filename))
        # обработка фотографии
        photod = ImageChange(now, file.filename)
        if form.f.data == '1':
            photod.pixelator()
        elif form.f.data == '2':
            photod.liner()
        elif form.f.data == '4':
            photod.edges()
        else:
            photod.nihil()
        photod.save()
        # занесение в базу данных информации о фотографии
        news.photo = f'{now}/{file.filename}'
        news.filter = form.f.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news_delete/<int:new_id>', methods=['GET', 'POST'])
@login_required
def news_delete(new_id):  # удаление фотографии
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == new_id, News.user == current_user).first()
    if news:
        os.remove(f'static/inner/{news.photo}')
        os.remove(f'static/images/{news.photo}')
        os.rmdir(f'static/inner/{news.photo.split("/")[0]}')
        os.rmdir(f'static/images/{news.photo.split("/")[0]}')
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/")
def index():  # главная страница
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news[::-1])


@app.route('/img/<int:date>/<string:name>')
def get_img(date, name):  # страница отображения отдельного изображения (сделано так как собираюсь дорабатывать)
    strs = str(date) + '/' + name
    return render_template('img.html', photo=strs)


@login_required
@app.route('/my_photos')
def my_photos_page():  # просмотр только своих изображений
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(News.user_id == current_user.id)
        if not news:
            txt = 'Вы ещё ничего не загрузили'
        else:
            txt = ''
        return render_template("index.html", news=news[::-1], txt=txt)
    else:
        abort(404)


@app.route('/download/<path:filename>/')
def download(filename):
    return send_file('static/images', filename)


if __name__ == '__main__':
    main()
