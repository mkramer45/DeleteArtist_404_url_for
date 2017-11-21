from flask import *
from functools import wraps
import sqlite3

artists = ['Solomun', 'Dubfire']
# DJname = request.form['DJname']


DATABASE = 'Beatscrape.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'my precious'

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

# 11/14 ... updated scrapelist2 in attempts to get the user input to be saved in ArtistMonitor table
@app.route('/scrapelist2', methods=['GET', 'POST'])
def scrapelist2():
	if request.method == 'POST':
		global feed
		conn = sqlite3.connect('Beatscrape.db')
		cursor = conn.cursor()
		posts = [dict(DJname=row[0]) for row in cursor.fetchall()]
		DJname = request.form['Producername']
		cursor.execute("INSERT INTO ArtistMonitor VALUES (NULL,?)", (DJname,))
		conn.commit()
		cursor.close()
		conn.close()
		artists.append(request.form['Producername'])
	g.db = connect_db()
	cur = g.db.execute('select DJName from ArtistMonitor')
	pull = [dict(DJname=row[0]) for row in cur.fetchall()]
	g.db.close()
	return render_template('scrapelist2.html', selected='submit', pull=pull)

	
@app.route('/delete_artist/<string:id>', methods=['POST'])
def delete_artist(id):
	g.db = connect_db()
	cur = g.db.execute("DELETE FROM ArtistMonitor WHERE id = ?", [id])
	g.db.commit
	return redirect(url_for('scrapelist2'))
	
	
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('log'))
	return wrap


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect (url_for('log'))

@app.route('/hello')
@login_required
def hello():
	g.db = connect_db()
	cur = g.db.execute('select Artist, Song, Label, Price from BeatPortTechHouse')
	info = [dict(Artist=row[0], Song=row[1], Label=row[2], Price=row[3]) for row in cur.fetchall()]
	g.db.close()
	return render_template('hello.html', info=info)

@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True

			return redirect(url_for('hello'))
	return render_template('log.html', error=error)



if __name__ == '__main__':
	app.run(debug=True)