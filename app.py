import sqlite3
import os
from flask import Flask, redirect, g, request, render_template, abort, flash, url_for

SECRET_KEY = 'development key'
DEBUG = True
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
	search_input = request.args['kanji_search']
	kanji = search(search_input)
	if not kanji:
		flash(search_input + " not found")
		return redirect(url_for('index'))
	else:
		return redirect("http://jisho.org/search/" + kanji + " %23kanji")


def search(text):
	try:
		nr = int(text)
		cur = g.db.execute('SELECT kanji FROM rtk WHERE nr_4 = ?', [nr])
	except ValueError:
		cur = g.db.execute('SELECT kanji FROM rtk WHERE name_deu = ? COLLATE nocase OR name_eng = ? COLLATE nocase', [text, text])
	found = cur.fetchone()
	if not found:
		return None
	else:
		return found[0]


if __name__ == '__main__':
	app.run()
