from flask_restful import abort
from flask import Flask, redirect, session, request
from flask import render_template as flask_render_template
import extra.auth as auth
from api.v1 import init as init_api_v1
from models import User, Surveys
from categories import categories


def init_route(app, db):
    def render_template(*args, **kwargs):
        kwargs['auth_user'] = auth.get_user()
        return flask_render_template(*args, **kwargs)

    init_api_v1(app, auth)

    @app.route('/')
    @app.route('/index')
    def index():
        db.create_all()

        surveys_list = Surveys.query.filter_by(publicity_check=True, on_admin_check=False)
        return render_template('index.html', title='question?', survey_list=surveys_list, category_list=categories, session=session)

    @app.route('/signup', methods=['GET', 'POST'])
    def registration():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user:
                return redirect('/signup')
            else:
                User.add(username=username, password=password)
                auth.login(username, password)
                session['username'] = username
                return redirect('/')

        return render_template(
            'signup.html',
            title='Регистрация'
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            if auth.login(username, request.form['password']):
                session['username'] = username
                return redirect('/')
            else:
                return redirect('/login')

        return render_template(
            'login.html',
            title='Вход'
        )

    @app.route('/surveys/create', methods=['GET', 'POST'])
    def add_survey():
        if not auth.is_authorized():
            return redirect('/login')

        if request.method == 'POST':
            title = request.form['survey-title']
            category = request.form['survey-category']
            publicity_check = eval(request.form['publicity_check'])
            on_admin_check = eval(request.form['publicity_check'])
            if not publicity_check:
                publicity_check = False
                on_admin_check = False

            Surveys.add(title=title, category=category, publicity_check=publicity_check, on_admin_check=on_admin_check, user=auth.get_user())
            return redirect('/')

        return render_template(
            'survey_create.html',
            title='Создание опроса',
            category_list=categories
        )

    @app.route('/logout')
    def logout():
        session.pop('user_id', 0)
        session.pop('username', 0)
        return redirect('/')
