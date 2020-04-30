from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.Users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RRB3'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def start():
    return redirect('/main_page')


@app.route('/main_page')
def load_main_page():
    return render_template('main_page.html', page_title='Главная страница')


@app.route('/tutorials/<int:tutorial_id>')
def load_content_page(tutorial_id):
    if not current_user.is_authenticated and 4 < tutorial_id < 9:
        abort(404)

    videos = {1: ['https://www.youtube.com/embed/srsRU7qN22s', 'https://www.youtube.com/embed/4E8sr4QS7OI',
                  'https://www.youtube.com/embed/Kmkx3SfJwuc'],
              2: ['https://www.youtube.com/embed/BOeqW-p52Dw', 'https://www.youtube.com/embed/JsfgDn273fI',
                  'https://www.youtube.com/embed/WLcaQkiJiq8'],
              3: ['https://www.youtube.com/embed/skFoGLIOkRY', 'https://www.youtube.com/embed/qUZ9EP6R_wA',
                  'https://www.youtube.com/embed/lSN_CPZ86Ng'],
              4: ['https://www.youtube.com/embed/FbgZ_3qErv0', 'https://www.youtube.com/embed/WhGom_wWK1I',
                  'https://www.youtube.com/embed/3jA6i8l3DQE'],
              5: ['https://www.youtube.com/embed/l6NTdAe_vu8', 'https://www.youtube.com/embed/C4vRM2RpYBU',
                  'https://www.youtube.com/embed/3Q5vYpfrV9A'],
              6: ['https://www.youtube.com/embed/_y2YcGqptLo', 'https://www.youtube.com/embed/OLh6t7wLyxY',
                  'https://www.youtube.com/embed/sFkwI0WVukM'],
              7: ['https://www.youtube.com/embed/Ir-iHGAWwMg', 'https://www.youtube.com/embed/Q6qOaPro_YM',
                  'https://www.youtube.com/embed/nJxAyDnfeM8'],
              8: ['https://www.youtube.com/embed/Rv26ek-OeZ4', 'https://www.youtube.com/embed/g8qR_AmNhOY',
                  'https://www.youtube.com/embed/lmT2X2qwN5Q']}

    titles = {1: 'Основы работы в Adobe Photoshop',
              2: 'Выделение объекта',
              3: 'Цветокоррекция фотографий',
              4: 'Работа с тенями',
              5: 'Работа со светом',
              6: 'Наложение текстуры на объект',
              7: 'Различные эффекты',
              8: 'Интересные фишки в Adobe Photoshop'}

    return render_template('content_page.html', page_title='Туториалы', title=titles[tutorial_id], link=videos[tutorial_id])


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration_form.html', page_title='Регистрация')

    elif request.method == 'POST':
        if request.form.get('name') == '' or request.form.get('password') == '' or \
                request.form.get('password_again') == '' or request.form.get('email') == '':
            return render_template('registration_form.html', page_title='Регистрация',
                                   error_message='Вы заполнили не все поля')
        if request.form.get('password') != request.form.get('password_again'):
            return render_template('registration_form.html', page_title='Регистрация',
                                   error_message='Пароли не совпадают')
        session = db_session.create_session()
        if session.query(User).filter(User.email == request.form.get('email')).first():
            return render_template('registration_form.html', page_title='Регистрация',
                                   error_message='Пользователь с таким адресом почты уже зарегистрирован')
        user = User(
            name=request.form.get('nickname'),
            email=request.form.get('email'),
        )
        user.set_password(request.form['password'])
        session.add(user)
        session.commit()

        login_user(user, remember=False)
        return redirect('/main_page')


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    global user_authorized
    if request.method == 'GET':
        return render_template('login_form.html', page_title='Авторизация')

    elif request.method == 'POST':
        session = db_session.create_session()
        user = session.query(User).filter(User.email == request.form.get('email')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user, remember=request.form.get('remember_me'))
            return redirect("/main_page")
        return render_template('login_form.html', page_title='Авторизация',
                               error_message="Неправильный логин или пароль")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/main_page")


if __name__ == '__main__':
    db_session.global_init("db/users.sqlite")
    app.run(host='127.0.0.1', port=8080)