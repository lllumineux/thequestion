from flask import Flask, session, render_template
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='question?')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
