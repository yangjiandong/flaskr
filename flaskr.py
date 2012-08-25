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

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql' ) as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    app.run()
