from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from Classes.Lang import Lang

lang = Lang("ru")


class CommentForm(FlaskForm):
    comment = TextAreaField(
        "Комментарий",
        validators=[
            DataRequired(message=lang.get("data_required", ["Комментарий"])),
        ]
    )
