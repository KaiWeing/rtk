import sqlite3
import os
from flask import Flask, redirect, g, request, render_template, abort, flash, url_for

SECRET_KEY = 'development key'
DEBUG = False
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATABASE_ROOT = os.path.join(APP_ROOT, 'data')
DATABASE = os.path.join(DATABASE_ROOT, 'rtk.db')

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
	g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/heisig')
def lookup():
	kanji_nr = request.args['kanji_nr']
	cur = g.db.execute('select kanji from rtk where nr_4 = ?', [kanji_nr])
	found = cur.fetchone()
	if not found:
		flash("No kanji nr " + kanji_nr)
		return redirect(url_for('index'))
	else:
		kanji = str(found[0])
		return redirect("http://jisho.org/search/" + kanji + " %23kanji")


if __name__ == '__main__':
	app.run()
