from flask_restful import abort
from flask import Flask, redirect, session, request
from flask import render_template as flask_render_template
import extra.auth as auth
from api.v1 import init as init_api_v1
from dbase import db
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
        session['last_page'] = '/index'
        db.create_all()
        surveys_list = Surveys.query.filter_by(publicity_check=True, on_admin_check=False)

        return render_template('index.html', title='question?', survey_list=surveys_list, category_list=categories, session=session)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
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
                return redirect(session['last_page'])

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
                return redirect(session['last_page'])
            else:
                return redirect('/login')

        return render_template(
            'login.html',
            title='Вход'
        )

    @app.route('/surveys/create', methods=['GET', 'POST'])
    def add_survey():
        session['last_page'] = '/surveys/create'

        if not auth.is_authorized():
            return redirect('/login')

        if request.method == 'POST':
            title = request.form['survey-title']
            category = request.form['survey-category']
            publicity_check = eval(request.form['publicity_check'])
            on_admin_check = publicity_check
            if not publicity_check:
                publicity_check = False
                on_admin_check = False
            Surveys.add(title=title,
                        category=category,
                        publicity_check=publicity_check,
                        on_admin_check=on_admin_check,
                        user=auth.get_user()
                        )
            return redirect(session['last_page'])

        return render_template(
            'survey_create.html',
            title='Создание опроса',
            category_list=categories
        )

    @app.route('/surveys/<int:survey_id>', methods=['GET', 'POST'])
    def surveys_view(survey_id: int):
        survey = Surveys.query.filter_by(id=survey_id).first()
        if not survey:
            abort(404)
        session['last_page'] = '/surveys/{}'.format(str(survey_id))

        if survey.voted_users_id and str(session['user_id']) in survey.voted_users_id.split():
            user_voted = True
        else:
            user_voted = False
            if request.method == 'POST':
                if not auth.is_authorized():
                    return redirect('/login')

                chosen_ans = request.form['chosen-ans']
                if chosen_ans == 'да':
                    Surveys.plus_yes(survey)
                else:
                    Surveys.plus_no(survey)

                Surveys.vote_add(survey, session['user_id'])

                return redirect(session['last_page'])

        return render_template(
            'survey.html',
            title='Опрос',
            survey=survey,
            user_voted=user_voted
        )

    @app.route('/surveys/delete/<int:survey_id>')
    def survey_delete(survey_id: int):
        if not auth.is_authorized():
            return redirect('/login')
        if session['username'] != 'admin':
            abort(403)

        survey = Surveys.query.filter_by(id=survey_id).first()
        Surveys.delete(survey)

        return redirect(session['last_page'])

    @app.route('/surveys/show/<int:survey_id>')
    def survey_show(survey_id: int):
        if not auth.is_authorized():
            return redirect('/login')
        if session['username'] != 'admin':
            abort(403)

        survey = Surveys.query.filter_by(id=survey_id).first()
        Surveys.show(survey)

        return redirect(session['last_page'])

    @app.route('/surveys/hide/<int:survey_id>')
    def survey_hide(survey_id: int):
        if not auth.is_authorized():
            return redirect('/login')
        if session['username'] != 'admin':
            abort(403)

        survey = Surveys.query.filter_by(id=survey_id).first()
        Surveys.hide(survey)

        return redirect(session['last_page'])

    @app.route('/surveys/mark_as_checked/<int:survey_id>')
    def survey_checked(survey_id: int):
        if not auth.is_authorized():
            return redirect('/login')
        if session['username'] != 'admin':
            abort(403)

        survey = Surveys.query.filter_by(id=survey_id).first()
        Surveys.mark_as_checked(survey)

        return redirect(session['last_page'])

    @app.route('/surveys')
    def user_surveys():
        session['last_page'] = '/surveys'

        if not auth.is_authorized():
            return redirect('/login')

        on_check_surveys = Surveys.query.filter_by(
            user_id=session['user_id'],
            on_admin_check=True
        )
        hidden_surveys = Surveys.query.filter_by(
            user_id=session['user_id'],
            on_admin_check=False,
            publicity_check=False,
        )
        shown_surveys = Surveys.query.filter_by(
            user_id=session['user_id'],
            on_admin_check=False,
            publicity_check=True
        )
        surveys_on_check = Surveys.query.filter_by(
            on_admin_check=True
        )

        return render_template('my_surveys.html',
                               on_check_surveys=on_check_surveys,
                               hidden_surveys=hidden_surveys,
                               shown_surveys=shown_surveys,
                               surveys_on_check=surveys_on_check
                               )

    @app.route('/logout')
    def logout():
        session.pop('user_id', 0)
        session.pop('username', 0)
        session.pop('last_page', 0)
        return redirect('/')
