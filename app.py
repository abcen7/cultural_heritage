import datetime
import requests
from flask import Flask, render_template, request, make_response, abort, url_for
from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase, SqlAlchemyBase
from data.Forms.CommentForm import CommentForm
from data.Forms.LoginForm import LoginForm
from data.Forms.RegisterForm import RegisterForm
from data.Forms.AddObjectForm import AddObjectForm
from data.Forms.SearchForm import SearchForm
from data.Models.Category import Category
from data.Models.Comment import Comment
from data.Models.Object import Object
from data.Models.Type import Type
from data.Models.User import User
from flask import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = r"static/upload_folder/"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["png", "jpg", "jpeg", "gif", "mp4", "avi", "mov"]

# Добавить ресурсы
api = Api(app)
# api.add_resource(GetPos, '/api/getpos')

login_manager = LoginManager()
login_manager.init_app(app)

db = SqlAlchemyDatabase(create=True)
session = db.create_session()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.errorhandler(401)
def login_error(error):
    return render_template('error.html', error="Недоступно для незарегистрированных пользователей")


@app.errorhandler(404)
def login_error(error):
    return render_template('error.html', error="Такой страницы не существует")


@app.route("/", methods=["GET", "POST"])
def index():
    objects = session.query(Object).all()
    form = SearchForm()
    if form.validate_on_submit():
        query = session.query(Object).filter(Object.title.like(f"%{form.search.data}%")).all()
        if query:
            return render_template("index.html", objects=query, form=form)
        else:
            return render_template("index.html", objects=objects, form=form, message="Ничего не было найдено")
    return render_template("index.html", objects=objects, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/map")
@login_required
def map():
    pixels_d = 2.858532
    pixels_sh = 5.78852867
    ll = [99.012606, 64.186239]  # координаты России
    data, data_marks = [], []
    for object in session.query(Object).all():
        try:
            data_marks.append(f"{object.on_map.split(',')[0]},{object.on_map.split(',')[1]}" + ',comma')
            coords = [object.id, [float(el) for el in object.on_map.split(',')]]
            data.append([coords[0], [225 + (ll[1] - coords[1][1]) * pixels_sh, 325 - (ll[0] - coords[1][0]) * pixels_d]])
        except Exception:
            pass
    map_request = "http://static-maps.yandex.ru/1.x"
    response = requests.get(map_request, params={"size": "650,450",
                                                 'll': f'{ll[0]},{ll[1]}',
                                                 'spn': '35,35',
                                                 'l': 'map',
                                                 'pt': '~'.join(data_marks),
                                                 'scale':'1'}
                            )
    print(response.request.url)
    map_file = "static/map/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return render_template("map.html", data=data)


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
        return redirect(f"/objects/{object_id}")

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


@app.route('/add_object', methods=['GET', 'POST'])
@login_required
def add_object():
    form = AddObjectForm()
    if current_user.is_admin():
        if form.validate_on_submit():
            if session.query(Object).filter(Object.register_number == form.register_number.data).first():
                return render_template('add_object.html', title='Добавить объект',
                                       form=form,
                                       message="Такой объект уже существует!")
            type = session.query(Type).filter(Type.title == form.type.data).first()
            category = session.query(Category).filter(Category.title == form.category.data).first()

            file_names = []

            for file in form.files.data:
                if file:
                    if file.filename.split(".")[-1] not in app.config["ALLOWED_FILE_EXTENSIONS"]:
                        return render_template(
                            "add_object.html",
                            message=f'Разрешенные форматы: {" ".join(app.config["ALLOWED_FILE_EXTENSIONS"])}',
                            form=form
                        )
                    file_name = f'{app.config["UPLOAD_FOLDER"]}{datetime.datetime.now().strftime("%s")}.' \
                                f'{file.filename.split(".")[-1]}'
                    file_names.append('/' + file_name)
                    file.save(file_name)

            object = Object(title=form.title.data,
                            register_number=form.register_number.data,
                            region=form.region.data,
                            full_address=form.address.data,
                            category_id=category.id,
                            type_id=type.id,
                            belonging_to_unesco=form.belonging_to_unesco.data,
                            especially_valuable=form.especially_valuable.data,
                            on_map=form.on_map.data,
                            files="<>".join(file_names))
            session.add(object)
            session.commit()
            return render_template('add_object.html', message='Объект добавлен', form=form)
        else:
            return render_template('add_object.html', title='Добавление объекта', form=form)
    else:
        return render_template('error.html', error='У вас нет прав администратора')


@app.route('/edit_object/<int:object_id>', methods=['GET', 'POST'])
@login_required
def edit_object(object_id):
    form = AddObjectForm()
    if not session.query(Object).filter(Object.id == object_id).first():
        abort(404)
    if current_user.is_admin():
        if form.validate_on_submit():
#             if session.query(Object).filter(Object.register_number == form.register_number.data).first():
#                 return render_template('edit_object.html',
#                                        title='Редактировать объект',
#                                        form=form,
#                                        message="Такой объект уже существует!",
#                                        obj=session.query(Object).filter(Object.id == object_id).first()
#                                        )
            type = session.query(Type).filter(Type.title == form.type.data).first()
            category = session.query(Category).filter(Category.title == form.category.data).first()

            obj = session.query(Object).filter(Object.id == object_id).first()
            obj.title = form.title.data
            obj.register_number = form.register_number.data
            obj.region = form.region.data
            obj.full_address = form.address.data
            obj.category_id = category.id
            obj.type_id = type.id
            obj.belonging_to_unesco = form.belonging_to_unesco.data
            obj.especially_valuable = form.especially_valuable.data
            obj.on_map = form.on_map.data
            if form.files.data:
                file_names = []
                for file in form.files.data:
                    if file:
                        if file.filename.split(".")[-1] not in app.config["ALLOWED_FILE_EXTENSIONS"]:
                            return render_template(
                                "edit_object.html",
                                error=f'Разрешенные форматы: {" ".join(app.config["ALLOWED_FILE_EXTENSIONS"])}',
                                form=form,
                                obj=session.query(Object).filter(Object.id == object_id).first()
                            )
                        file_name = f'{app.config["UPLOAD_FOLDER"]}{datetime.datetime.now().strftime("%s")}.' \
                                    f'{file.filename.split(".")[-1]}'
                        file_names.append('/' + file_name)
                        file.save(file_name)
                obj.files = "<>".join(file_names)
            else:
                obj.files = obj.files
            session.merge(obj)
            session.commit()
            return render_template(
                "edit_object.html",
                title='Изменение объекта',
                message="Объект был успешно отредактирован",
                form=form,
                obj=session.query(Object).filter(Object.id == object_id).first()
            )
        else:
            return render_template(
                "edit_object.html",
                title='Изменение объекта',
                form=form,
                obj=session.query(Object).filter(Object.id == object_id).first()
            )
    else:
        return render_template('error.html', error='У вас нет прав администратора')


@app.route("/delete_object/<int:object_id>", methods=["GET", "POST"])
def delete_object(object_id):
    obj = session.query(Object).filter(Object.id == object_id).first()
    if not obj:
        return render_template('error.html', error="Такой записи не существует")
    else:
        session.delete(obj)
        session.commit()
        return redirect(url_for("/", message="Запись была удалена!"))


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
            email=form.email.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
