import datetime
from flask import Flask, render_template, request, make_response, abort
from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase, SqlAlchemyBase
from data.Forms.CommentForm import CommentForm
from data.Forms.LoginForm import LoginForm
from data.Forms.RegisterForm import RegisterForm
from data.Models.Comment import Comment
from data.Models.Object import Object
from data.Models.User import User
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config["DEBUG"] = True

# Добавить ресурсы
api = Api(app)
# api.add_resource(GetPos, '/api/getpos')

login_manager = LoginManager()
login_manager.init_app(app)

db = SqlAlchemyDatabase()
session = db.create_session()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@login_required
def index():
    objects = session.query(Object).all()
    if objects:
        return render_template("index.html", objects=objects)
    else:
        abort(403)


@app.route("/objects/<int:object_id>", methods=["GET", "POST"])
def describe_object(object_id):
    obj = session.query(Object).filter(Object.id == object_id).first()
    comments = session.query(Comment).filter(Comment.belongs_to_object == object_id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.comment.data,
            belongs_to_object=object_id,
            created_by=f"{current_user.name} {current_user.surname}"
        )
        session.add(comment)
        session.commit()
        print("SUCCESS")
        return redirect("/")

    if obj:
        return render_template("object.html", form=form, obj=obj, comments=comments)
    else:
        abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            password=form.password.data,
            age=int(form.age.data),
            email=form.email.data
        )
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(host="localhost", port=8080)
