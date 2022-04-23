from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Length

from Classes.Lang import Lang

lang = Lang("ru")


class SearchForm(FlaskForm):
    search = StringField(
        "Поиск",
        validators=[DataRequired()]
    )
    submit = SubmitField("Поиск")
