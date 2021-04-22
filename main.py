import json

from flask import Flask, render_template, redirect, request, make_response, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, login_manager
from sqlalchemy import func

from forms.user import RegisterForm, LoginForm
from data.users import User
from data.compositions import Composition
from data import db_session, composition_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
sort_by_class = False
sort_by_author = False

def main():
    db_session.global_init("db/library.db")
    app.register_blueprint(composition_api.blueprint)
    login_manager.login_view = 'login'
    app.run(port=8080, host='127.0.0.1')


# просто коментарий


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    params = {}
    if current_user.is_authenticated:
        params['molodec'] = True
    else:
        params['molodec'] = False
    params['title'] = 'Дневник читателя'
    compositions = db_sess.query(Composition).all()[:-1:]
    params["compositions"] = compositions
    return render_template('index.html', **params)


@app.route("/search", methods=['post', 'get'])
def search():
    if request.method == 'POST':
        print("1")
        search_value = request.form['search_value']  # запрос к данным формы
        db_sess = db_session.create_session()
        params = {}
        compositions = []
        if current_user.is_authenticated:
            params['molodec'] = True
        else:
            params['molodec'] = False
        params['title'] = 'Дневник читателя'
        if search_value.isdigit():
            search1 = int(search_value)
            if search1 in range(5, 9):
                compositions = db_sess.query(Composition).filter(Composition.Class == search1).all()
            else:
                compositions = db_sess.query(Composition).filter(Composition.Year.contains(search_value)).all()
        elif not search_value:
            compositions = db_sess.query(Composition).all()[:-1:]
        else:
            search1 = "%{}%".format(search_value)
            compositions = db_sess.query(Composition).filter(func.upper(Composition.Name).
                                                             contains(func.upper(search1))
                                                             | func.upper(Composition.Author).
                                                             contains(func.upper(search1))).all()

        print(Composition)
        params["compositions"] = compositions
        return render_template('index.html', **params)


@app.route("/change_sort_by_class")
def shange_sort_by_class():
    print(4)
    global sort_by_class
    print(sort_by_class)
    if sort_by_class:
        sort_by_class = False
    else:
        sort_by_class = True

    if sort_by_class:
        db_sess = db_session.create_session()
        params = {}
        if current_user.is_authenticated:
            params['molodec'] = True
        else:
            params['molodec'] = False
        params['title'] = 'Дневник читателя'
        compositions = db_sess.query(Composition).order_by(Composition.Class.desc()).all()[1::]
        params["compositions"] = compositions
        print("1")
        return render_template('index.html', **params)
    else:
        return redirect("/index")


@app.route("/change_sort_by_author")
def change_sort_by_author():
    print(3)
    global sort_by_author
    if sort_by_author:
        sort_by_author = False
    else:
        sort_by_author = True

    if sort_by_author:
        db_sess = db_session.create_session()
        params = {}
        if current_user.is_authenticated:
            params['molodec'] = True
        else:
            params['molodec'] = False
        params['title'] = 'Дневник читателя'
        compositions = db_sess.query(Composition).order_by(Composition.Author.asc()).all()[1::]
        params["compositions"] = compositions
        print(2)
        return render_template('index.html', **params)
    else:
        return redirect("/index")


@app.route('/<name>')
def about_composition(name):
    params = {}
    db_sess = db_session.create_session()
    composition = db_sess.query(Composition).filter(Composition.Name == name).all()
    try:
        params["composition"] = composition[0]
        return render_template("composition.html", **params)
    except IndexError:
        params["composition"] = composition
        return render_template("composition.html", **params)


@app.route("/about")
def about_app():
    return render_template("about_app.html")


@app.route('/download')
def download_file():
    path = "static/Форма для дневника читателя.docx"
    return send_file(path, as_attachment=True)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
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
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
