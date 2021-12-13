import os
from sqlite3 import dbapi2 as sqlite3

import werkzeug
from flask import Flask, request, g, redirect, url_for, render_template, flash, session

from werkzeug.security import generate_password_hash, check_password_hash


# This application takes many parts which were created by the developers of Flask Most functions are directly used
# from the original code of this application or have been alterned to meet the need for this application.

# create our little application :)
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12).hex()

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'tournaments.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///tournaments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


'''The following 3 functions have been derived from
https://github.com/pallets/flask/blob/5beb3be536cc743962de6cd2bd95a6e036d11f52/examples/flaskr/flaskr/flaskr.py'''


@app.route('/', methods=['GET'])
def show_tournaments():
    """Shows a list of the user's ongoing tournaments"""
    db = get_db()
    cur = db.execute('SELECT * from tournament')
    tournaments = cur.fetchall()
    return render_template('main_page.html', tournaments=tournaments)


@app.route('/create')
def show_login():
    db = get_db()
    cur = db.execute('SELECT * from player')
    login = cur.fetchall()
    return render_template('login.html', login=login)


@app.route('/create-signup')
def show_signup():
    db = get_db()
    cur = db.execute('SELECT * from player')
    signup = cur.fetchall()
    return render_template('sign_up.html', signup=signup)

@app.route('/create-events')
def show_events():
    db = get_db()
    cur = db.execute('SELECT * from tournament')
    events = cur.fetchall()
    return render_template('events.html', events=events)

@app.route('/create-communities')
def show_communities():
    db = get_db()
    cur = db.execute('SELECT * from tournament')
    communities = cur.fetchall()
    return render_template('communities.html', communities=communities)


@app.route('/create-tournament')
def show_create_tournament():
    db = get_db()
    cur = db.execute('SELECT * from tournament')
    create = cur.fetchall()
    return render_template('create_tournament.html', create=create)


@app.route('/new-bracket4')
def show_bracket4():
    db = get_db()
    name = request.args.get('name')
    player_name = request.args.get('player_name')
    game_name = request.args.get('game_name')
    description = request.args.get('description')
    if name is not None \
        and player_name is not None \
        and game_name is not None \
        and description is not None:
        cur = db.execute(
            'SELECT name, player_name, game_name, description '
            'FROM tournament WHERE name=? AND player_name=? '
            'AND game_name=? AND description=? limit 1',
            [request.args.get('name', type=str),
             request.args.get('player_name', type=str),
             request.args.get('game_name', type=str),
             request.args.get('description', type=str)])
        tournament = cur.fetchone()
    else:
        cur = db.execute('SELECT name, player_name, game_name, description '
            'FROM tournament limit 1')
        tournament = cur.fetchone()
    return render_template('bracket4.html', tournament=tournament)


@app.route('/new-bracket8')
def show_bracket8():
    db = get_db()
    name = request.args.get('name')
    player_name = request.args.get('player_name')
    game_name = request.args.get('game_name')
    description = request.args.get('description')
    if name is not None \
            and player_name is not None \
            and game_name is not None \
            and description is not None:
        cur = db.execute(
            'SELECT name, player_name, game_name, description '
            'FROM tournament WHERE name=? AND player_name=? '
            'AND game_name=? AND description=? limit 1',
            [request.args.get('name', type=str),
             request.args.get('player_name', type=str),
             request.args.get('game_name', type=str),
             request.args.get('description', type=str)])
        tournament = cur.fetchone()
    else:
        cur = db.execute('SELECT name, player_name, game_name, description '
                         'FROM tournament limit 1')
        tournament = cur.fetchone()
    return render_template('bracket8.html', tournament=tournament)


@app.route('/new-bracket16')
def show_bracket16():
    db = get_db()
    name = request.args.get('name')
    player_name = request.args.get('player_name')
    game_name = request.args.get('game_name')
    description = request.args.get('description')
    if name is not None \
            and player_name is not None \
            and game_name is not None \
            and description is not None:
        cur = db.execute(
            'SELECT name, player_name, game_name, description '
            'FROM tournament WHERE name=? AND player_name=? '
            'AND game_name=? AND description=? limit 1',
            [request.args.get('name', type=str),
             request.args.get('player_name', type=str),
             request.args.get('game_name', type=str),
             request.args.get('description', type=str)])
        tournament = cur.fetchone()
    else:
        cur = db.execute('SELECT name, player_name, game_name, description '
                         'FROM tournament limit 1')
        tournament = cur.fetchone()
    return render_template('bracket16.html', tournament=tournament)


@app.route('/profile')
def show_profile():
    db = get_db()
    cur = db.execute('SELECT * from player')
    profile = cur.fetchall()
    return render_template('profile_page.html', profile=profile)


@app.route('/new-tournament', methods=['POST'])
def new_tournament():
    """Allows users to create new tournaments """
    db = get_db()
    db.execute('INSERT INTO tournament(name, size, player_name, game_name, description) VALUES (?, ?, ?, ?, ?)',
               [request.form['name'], request.form['size'], request.form['player_name'], request.form['game_name'], request.form['description']])

    db.commit()
    size = request.form.get('size', type=int)
    if size == 4:
        return redirect(url_for('show_bracket4', name=request.form['name'],
                                player_name=request.form['player_name'],
                                game_name=request.form['game_name'],
                                description=request.form['description']))
    elif size == 8:
        return redirect(url_for('show_bracket8', name=request.form['name'],
                                player_name=request.form['player_name'],
                                game_name=request.form['game_name'],
                                description=request.form['description']))
    elif size == 16:
        return redirect(url_for('show_bracket16', name=request.form['name'],
                                player_name=request.form['player_name'],
                                game_name=request.form['game_name'],
                                description=request.form['description']))
    else:
        return redirect(url_for('show_tournaments'))


@app.route('/delete-tournament', methods=['POST'])
def del_tournament():
    """Deletes a tournament, identified by the tournament id"""
    db = get_db()
    db.execute('DELETE FROM tournament WHERE id=?', [request.form['id']])
    db.commit()
    flash('Tournament deleted successfully!')
    return redirect(url_for('show_tournaments'))


# Function allows a user to sign up for the website
@app.route('/sign-up', methods=['POST'])
def sign_up():
    password = request.form['hash']
    hashed_password = generate_password_hash(password)
    db = get_db()
    db.execute('INSERT INTO account(name, hash) VALUES (?, ?)',
               [request.form['name'], hashed_password])

    db.commit()
    return redirect(url_for('show_tournaments'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Requests username and password from the login form
        username = request.form['username']
        password = request.form['password']

        # Gets the database and gets the row associated with the username
        db = get_db()
        user = db.execute('SELECT * from account where name = ?', (username,)).fetchone()
        user_id = user['ID']

        # If user doesn't exist return error
        if user is None:
            error = 'Invalid username'
        # If password does not matched stored hash return error
        elif not check_password_hash(user['hash'], password):
            error = 'Invalid password'
        # If username and password match redirect user to home page
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_profile'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_tournaments'))

