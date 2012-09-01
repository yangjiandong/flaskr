# -*- coding: utf-8 -*-
#from __future__ import with_statemnt
from contextlib import closing
import sqlite3
from flask import Flask, request, session,g,redirect,url_for,\
        abort, render_template, flash

#configuation
DATABASE = 'tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'DEVELOPMENT KEY'
USERNAME='admin'
PASSWORD='123'

app = Flask(__name__)
app.config.from_object(__name__)

ADMINS = ['yourname@example.com']
def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)

    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@example.com',
                               ADMINS, 'YourApplication Failed')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    else:
        import logging
        from logging import FileHandler
        file_handler = FileHandler('app.log');
        from logging import Formatter
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)


    return app

# To allow aptana to receive errors, set use_debugger=False
# 还有问题
# appp = create_app(config="config.ini")

if app.debug:
    use_debugger = True
try:
    use_debugger = not(app.config.get('DEBUG_WITH_APTANA'))
except:
    pass

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql' ) as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    cur =g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    app.logger.debug(entries)
    return render_template('show_entries.html', entries = entries)

# add new entry
@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    g.db.execute('insert into entries(title, text) values(?,?)',
            [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'

        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()

    # app.run(use_debugger=use_debugger, debug = app.debug,
            # user_reloader =use_debugger, host='0.0.0.0')
