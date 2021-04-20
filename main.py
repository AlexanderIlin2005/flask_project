
from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import json

from flask import Flask, render_template, redirect, request, make_response, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, login_manager

from forms.user import RegisterForm, LoginForm
from data.users import User
# from data.compositions import Composition
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/library.db")
    app.run(port=8080, host='127.0.0.1')
# просто коментарий


@app.route('/download')
def download_file():
    path = "static/Форма для дневника читателя.docx"
    return send_file(path, as_attachment=True)


@app.route("/")
@app.route("/index")
def index():
    params = {}
    params['title'] = 'Дневник читателя'
    return render_template('index.html', **params)

"""
@app.route('/compositions/<name>')
@login_manager.user_loader
def list_prof(name):
    param = {}
    param['title'] = name
    db_sess = db_session.create_session()
    return render_template('composition.html', **param)
"""

@app.route('/login', methods=['GET', 'POST'])
@login_manager.user_loader
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