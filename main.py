from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm, LoginForm
from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# просто коментарий

@app.route("/")
@app.route("/index")
def index():
    params = {}
    params['title'] = 'Домашняя страница'
    return render_template('index.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)



def main():
    db_session.global_init("db/library.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()