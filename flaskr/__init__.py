# -*- coding: utf-8 -*-
from flask import Flask
import sqlite3

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

import flaskr.views

