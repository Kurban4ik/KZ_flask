from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
    photo = FileField('Фото')
    f = SelectField(choices=[(1, 'pixelator'),
           (2, 'liner'),
           (3, 'nihil')])