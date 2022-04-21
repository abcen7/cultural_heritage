from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField, SelectField, \
    FileField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from Classes.Lang import Lang

SEX_LIST = ["Мужской", "Женский"]

lang = Lang("ru")


class RegisterForm(FlaskForm):
    name = StringField(
        "Имя",
        validators=[
            DataRequired(message=lang.get("data_required", ["Имя"])),
            Length(min=2, max=100, message=lang.get("field_min_len", ["Имя", "2", "100"]))
        ]
    )
    surname = StringField(
        "Фамилия",
        validators=[
            DataRequired(message=lang.get("data_required", ["Фамилия"])),
            Length(min=2, max=100, message=lang.get("field_min_len", ["Фамилия", "2", "100"]))
        ]
    )
    age = IntegerField(
        "Возраст",
        validators=[
            DataRequired(message=lang.get("data_required", ["Возраст"])),
            NumberRange(12, 100, message=lang.get("field_range", ["Возраст", "12", "100"]))
        ]
    )
    email = EmailField(
        "Почта",
        validators=[
            DataRequired(message=lang.get("data_required", ["Почта"])),
            Email(message=lang.get("field_invalid", ["Почта"]))
        ]
    )
    # TODO: Пароль должен включать в себя спец. символы и буквы заглавного и нижнего регистра
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message=lang.get("data_required", ["Пароль"])),
            Length(min=6, max=100, message=lang.get("field_min_len", ["Пароль", "6", "100"]))
        ]
    )
    submit = SubmitField("Зарегистрироваться")
