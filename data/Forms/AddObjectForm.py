from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField, SelectField, \
    FileField, FieldList, RadioField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from Classes.Lang import Lang
from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
from data.Models.Type import Type
from data.Models.Category import Category
SEX_LIST = ["Мужской", "Женский"]

lang = Lang("ru")


class AddObjectForm(FlaskForm):
    db = SqlAlchemyDatabase()
    session = db.create_session()
    title = StringField(
        "Название",
        validators=[
            DataRequired(message=lang.get("data_required", ["Название"]))
        ]
    )
    register_number = IntegerField(
        "Регистрационный номер",
        validators=[
            DataRequired(message=lang.get("data_required", ["Регистрационный номер"])),
        ]
    )

    region = StringField(
        "Регион",
        validators=[
            DataRequired(message=lang.get("data_required", ["Регион"])),
        ]
    )

    address = StringField(
        "Полный адрес",
        validators=[
            DataRequired(message=lang.get("data_required", ["Полный адрес"])),
        ]
    )
    choices = [category.title for category in session.query(Category).all()]
    category = RadioField(
        "Категория", choices=[],
        validators=[
            DataRequired(message=lang.get("data_required", ["Категория"])),
        ]
    )

    choices = [type.title for type in session.query(Type).all()]
    type = RadioField(
        "Тип", choices=[],
        validators=[
            DataRequired(message=lang.get("data_required", ["Тип"])),
        ]
    )

    belonging_to_unesco = BooleanField("Относится к Юнеско")

    especially_valuable = BooleanField("Особенно ценный")
    on_map = StringField('Координаты объекта')
    submit = SubmitField("Добавить объект")

