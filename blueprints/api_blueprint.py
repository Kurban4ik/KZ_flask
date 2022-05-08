import datetime
import os

from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse

from data import db_session
from data.photos import News
from data.users import User

api_blueprint = Blueprint('api_blueprint', __name__, )
api = Api(api_blueprint)

parser = reqparse.RequestParser()


def get_news(new_id):
    db_sessi = db_session.create_session()
    news = db_sessi.query(News).filter(News.id == int(new_id)).first()
    print(db_sessi.query(News).all()[-1].filter)
    if news:
        print('ya')
        return news.user.name, news.photo, news.filter, news.user_id
    return 0


class NewsApi(Resource):
    def get(self):
        args = request.args
        new_id = args['news_id']
        newa = args['name']
        date = args['date']

        new = get_news(new_id)
        if new:
            return {'creator': new[0], 'photo': new[1], 'filter': new[2], 'user_id': new[3],
                    'image_url': f'http://127.0.0.1:5000/img/{date}?name={newa}'}
        return {'error': 'i shitted in my pants'}

    def post(self):
        db_sessi = db_session.create_session()
        args = request.form
        login = args['login']
        password = args['password']
        for i in db_sessi.query(User).all():
            if i.check_password(password) and i.email == login:
                file = request.files['file']
                # проверка на формат
                if request.files["file"].content_type.split('/')[-1] not in ['png', 'jpg', 'jpeg']:
                    return {'response': 'wrong format: png, jpg, jpeg allowed only'}, 503
                filters = args['filter']
                now = datetime.datetime.now()
                now = str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
                print(i.email)
                file.save('./blueprints/' + file.filename)
                return {'response': 'ok'}


api.add_resource(NewsApi, '/api/news')
