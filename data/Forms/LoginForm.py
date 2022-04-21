from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

from Classes.Lang import Lang

lang = Lang("ru")


class LoginForm(FlaskForm):
    email = EmailField(
        "Почта",
        validators=[
            DataRequired(message=lang.get("data_required", ["Почта"])),
            Email(message=lang.get("field_invalid", ["Почта"]))
        ]
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message=lang.get("data_required", ["Пароль"])),
            Length(min=6, max=100, message=lang.get("field_min_len", ["Пароль", "6", "100"]))
        ]
    )
    remember_me = BooleanField(lang.get("field_remember_me"))
