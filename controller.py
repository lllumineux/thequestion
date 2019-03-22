from flask import Flask, session, render_template, request
from werkzeug.utils import redirect

app = Flask(__name__)

all_surveys = {
    'survey1': {
        'name': 'Гапон красавчик?',
        'category': 'Люди',
        'id': '1'
    },
    'survey2': {
        'name': 'Права палочка твикс круче левой?',
        'category': 'Другое',
        'id': '2'
    },
    'survey3': {
        'name': 'Левая палочка твикс хуже правой?',
        'category': 'Другое',
        'id': '3'
    },
    'survey4': {
        'name': 'Сергей козёл?',
        'category': 'Люди',
        'id': '4'
    }
}
all_users = {
    'login': 'password',
    'admin': 'admin'
}
session = {
    'username': 'admin'
}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='question?', survey_list=all_surveys, session=session)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        if 'username' in session:
            return redirect('/')
        return render_template('signup.html', title='Зарегистрироваться')

    elif request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        all_users[name] = password
        session['username'] = name
        return redirect('/')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect('/')
        return render_template('login.html', title='Войти')

    elif request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        if name in all_users and all_users[name] == password:
            session['username'] = name
            return redirect('/')
        return render_template('login.html', title='Войти')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
