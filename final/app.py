import os
from collections import defaultdict
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, send_from_directory, abort, send_file, Response
import json
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from helpers import login_required, logout_required, generate_address, generate_image


app = Flask(__name__)
app.secret_key = 'aa0e62f3a9fe7935e90248f484755e2d4c7a917935090e42a67551dda2d1010f'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=90)


MAX_LEVELS = 7

db = SQL("sqlite:///z.db")
@app.after_request
def add_cache_control(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, must-revalidate'
    elif request.path.startswith('/makeEnv/'):
        response.headers['Cache-Control'] = 'private, max-age=31536000'
    else:
        response.headers['Cache-Control'] = 'public, must-revalidate, max-age=360000'
    return response


@app.route("/")
@login_required
def index():
    return redirect('/home')



@app.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            flash('Must provide a username')
            return redirect('/login')
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Must provide a password')
            return redirect('/login')
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash('Invalid username and/or password')
            return redirect('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    if (request.method == "POST"):
        if not (username := request.form.get("username")):
            flash('Must provide a username')
            return redirect('/register')
        if not (password := request.form.get("password")):
            flash('Must provide password')
            return redirect('/register')
        if not (password == request.form.get("confirm")):
            flash('Passwords do not match')
            return redirect('/register')
        if (len(password) < 5):
            flash('Passwords is too short.')
            return redirect('/register')
        if (len(password) > 20):
            flash('Passwords is too long')
            return redirect('/register')
        if (len(username) < 2):
            flash('Username is too short.')
            return redirect('/register')
        if (len(username) > 15):
            flash('Username is too long')
            return redirect('/register')


        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?);", username,
                       generate_password_hash(password, method='pbkdf2', salt_length=16))
            id = db.execute("SELECT id FROM users WHERE username = ?;", username)[0]['id']
            address = generate_address()
            db.execute("INSERT INTO addresses (user_id, street, city, zip, country) VALUES(?, ?, ?, ?, ?);", id ,address["street"], address["city"], address["zip"], address["country"])
            for i in range(1, MAX_LEVELS + 1, 1):
                db.execute("INSERT INTO notes (user_id, level) VALUES (?, ?);", id, i)
                db.execute("INSERT INTO envelopes_modify (user_id, route) VALUES (?, ?);", id, "env" + str(i))

        except ValueError:
            flash('Username already exists')
            return redirect('/register')
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == 'POST':
        data = request.get_json()
        if message := data.get('message'):
            c = datetime.now()
            date = c.strftime('%y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO messages (user_id, message, date) VALUES(?, ?, ?);", session['user_id'], message, date)
        if last_id := data.get('last_id'):
            messages = db.execute("SELECT * FROM (SELECT users.username, messages.message, messages.id FROM users JOIN messages ON users.id = messages.user_id WHERE messages.id > ? ORDER BY messages.id DESC) ORDER BY id ASC;", last_id)
            return jsonify(messages), 203
        return '', 203

    messages = db.execute("SELECT * FROM (SELECT users.username, messages.message, messages.id FROM users JOIN messages ON users.id = messages.user_id ORDER BY messages.id DESC LIMIT 50) ORDER BY id ASC;")
    if not messages:
        return render_template("chat.html", messages = None, last_id = 0)

    return render_template("chat.html", messages = messages, last_id = messages[-1]['id'])


@app.route("/document", methods=["GET", "POST"])
@login_required
def document():
    if request.method == "POST":
        try:
            data = request.get_json()
            note = data.get('note')[0:400]
            level = data.get('level')
            if note and level:
                db.execute("UPDATE notes SET note = ? WHERE user_id = ? AND level = ?;", note, session['user_id'], level)
                return "Saved", 200
        except Exception:
            return "Couldn't save", 300
    else:
        level = db.execute("SELECT level FROM users WHERE id = ?;", session["user_id"])[0]['level']
        texts = json.dumps(db.execute("SELECT * FROM (SELECT note, letters.level, letter FROM (SELECT note, level FROM notes WHERE user_id = ?) AS notes JOIN letters ON notes.level = letters.level) WHERE level <= ? ORDER BY level ASC;", session["user_id"], level))
        return render_template("document.html", texts = texts, level = level)

@app.route('/static/<path:filename>')
def custom_static(filename):
    file_path = os.path.join('static', filename)
    last_modified_time = os.path.getmtime(file_path)
    last_modified = datetime.datetime.utcfromtimestamp(last_modified_time).strftime('%a, %d %b %Y %H:%M:%S GMT')

    if 'If-Modified-Since' in request.headers:
        if_modified_since = request.headers['If-Modified-Since']
        if if_modified_since == last_modified:
            return Response(status=304)

    response = send_from_directory('static', filename)
    response.headers['Last-Modified'] = last_modified
    if (filename[0:3 == "zxy"]):
        try:
            if (int(filename[4 : filename.index('.')]) <= db.execute("SELECT level FROM users WHERE id = ?;", session["user_id"])[0]['level']):
                return response
            abort(403)
        except Exception:
            return response
    return response


@app.route('/makeEnv/<user_id>/<route>')
@login_required
def fetch_media(user_id, route):
    if not (str(user_id) == str(session['user_id'])):
        return "u aint no slick", 403
    level = db.execute("SELECT level FROM users WHERE id = ?;", session['user_id'])[0]['level']
    address = db.execute("SELECT street, city, zip, country FROM addresses WHERE user_id = ?;", session['user_id'])[0]
    username = db.execute("SELECT username FROM users WHERE id = ?;", session['user_id'])[0]['username']
    if route == 'envOwn':
        if recipient := db.execute("SELECT * FROM recipient_addresses WHERE user_id = ? AND level = ?;", session['user_id'], level):
            recipient = recipient[0]
    else:
        recipient = None
    try:
        print(f"generated {route} for {username}")
        image = generate_image(route, address, username, recipient)
        print("done serverside")
        db.execute("UPDATE envelopes_modify SET modified = 0 WHERE user_id = ? AND route = ?;", user_id, route)
        return send_file(image, as_attachment=True, download_name=route+'png', mimetype='image/png')
    except Exception as e:
        print(e)
        return abort(500)


@app.route('/q/<user_id>/<route>')
@login_required
def query_for_modify(user_id, route):
    if not (str(user_id) == str(session['user_id'])):
        return "u aint no slick", 403

    if not (state := db.execute("SELECT modified FROM envelopes_modify WHERE user_id = ? AND route = ?;", user_id, route)):
        db.execute("INSERT INTO envelopes_modify (user_id, route) VALUES(?, ?);", user_id, route)
        return '', 200
    if  state[0]['modified']:
        return '', 200

    return '', 304


@app.route("/poffice", methods=["GET", "POST"])
@login_required
def poffice():
    level = db.execute("SELECT level FROM users WHERE id = ?;", session["user_id"])[0]['level']
    if request.method == "POST":
        db.execute("UPDATE user_letters SET message = ?, attachments = ? WHERE user_id = ? AND level = ?;", request.json['letter'][0:400], ','.join(map(str, request.json['attachments'])), session["user_id"], level)
        return '', 200

    if not (letter:= db.execute("SELECT message FROM user_letters WHERE user_id = ? AND level = ?;", session["user_id"], level)):
        db.execute("INSERT INTO user_letters (user_id, level) VALUES (?, ?);", session["user_id"], level)
        letter = db.execute("SELECT message FROM user_letters WHERE user_id = ? AND level = ?;", session["user_id"], level)
    letter = letter[0]['message']
    attachments = db.execute("SELECT attachments FROM user_letters WHERE user_id = ? AND level = ?;", session["user_id"], level)[0]['attachments']
    if attachments == '':
        attachments = []
    else:
        attachments = attachments.split(',')

    address = db.execute("SELECT * FROM addresses WHERE user_id = ?;", session["user_id"])[0]
    username = db.execute("SELECT username FROM users WHERE id = ?;", session["user_id"])[0]['username']
    inbox = json.dumps(db.execute("SELECT name, address, city, zipcode, country, time, message FROM inbox ORDER BY indx ASC;"))
    address_book = json.dumps(db.execute("SELECT * FROM address_book;"))
    items = {}
    rows = db.execute("SELECT * FROM items WHERE level <= ? ORDER BY level, item_index;", level)
    for row in rows:
        lvl = row['level']
        item_type = row['item_type']
        item_content = row['item_content']
        item_name = row['name']
        item_id = str(row['id'])
        if item_type != "document":
            if lvl not in items:
                items[lvl] = []
            items[lvl].append({"type": item_type, "content": item_content, "name": item_name, "id": item_id})

    attachments = json.dumps(attachments)
    items = json.dumps(items)

    return render_template("poffice.html", address_book = address_book, inbox = inbox, address=address, username=username, letter=letter, items=items, level = level, attachments = attachments)


@app.route("/submit_address", methods=["POST"])
@login_required
def submit_address():

    if not (name := request.form.get("NOTname")):
        flash('You aint no slick, dont bypass! no name provided.')
        return redirect('/poffice')
    if not (street := request.form.get("NOTstreet")):
        flash('You aint no slick, dont bypass! no street provided.')
        return redirect('/poffice')
    if not (city := request.form.get("NOTcity")):
        flash('You aint no slick, dont bypass! no city provided.')
        return redirect('/poffice')
    if not (zip := request.form.get("NOTzip")):
        flash('You aint no slick, dont bypass! no zip provided.')
        return redirect('/poffice')
    if not (country := request.form.get("NOTcountry")):
        flash('You aint no slick, dont bypass! no country provided.')
        return redirect('/poffice')
    level = db.execute("SELECT level FROM users WHERE id = ?;", session['user_id'])[0]['level']
    if db.execute("SELECT * FROM recipient_addresses WHERE user_id = ? AND level = ?;", session['user_id'], level):
        db.execute("DELETE FROM recipient_addresses WHERE user_id = ? AND level = ?;", session['user_id'], level)
    db.execute("INSERT INTO recipient_addresses (user_id, name, street, city, zip, country, level) VALUES(?, ?, ?, ?, ?, ?, ?);", session['user_id'], name, street, city, zip, country, level)
    db.execute("UPDATE envelopes_modify SET modified = 1 WHERE user_id = ? AND route = 'envOwn';", session['user_id'])

    return redirect("/poffice")



@app.route("/home")
@login_required
def mix():
    messages = db.execute("SELECT * FROM (SELECT users.username, messages.message, messages.id FROM users JOIN messages ON users.id = messages.user_id ORDER BY messages.id DESC LIMIT 50) ORDER BY id ASC;")
    if not messages:
        return render_template("mix.html", messages = None, last_id = 0)

    lvl = db.execute("SELECT level FROM users WHERE id = ?;", session["user_id"])[0]['level']
    texts = json.dumps(db.execute("SELECT * FROM (SELECT note, letters.level, letter FROM (SELECT note, level FROM notes WHERE user_id = ?) AS notes JOIN letters ON notes.level = letters.level) WHERE level <= ? ORDER BY level ASC;", session["user_id"], lvl))
    address_book = json.dumps(db.execute("SELECT name, address, city, zipcode, country FROM address_book ORDER BY indx ASC;"))
    items = defaultdict(lambda: {"document": None, "others": []})

    rows = db.execute("SELECT item_index, level, item_type, item_content FROM items WHERE level <= ? ORDER BY level, item_index;", lvl)
    for row in rows:
        level = row['level']
        item_type = row['item_type']
        item_content = row['item_content']

        if item_type == "document":
            # Assign document content
            items[level]["document"] = item_content
        else:
            # Append other item to the 'others' list
            items[level]["others"].append({"type": item_type, "content": item_content})

    # Convert defaultdict to regular dictionary
    items = dict(items)

    # Pass levels to Jinja
    items_json = json.dumps(items)

    return render_template("mix.html", items = items_json, address_book = address_book, texts = texts, level = lvl, messages = messages, last_id = messages[-1]['id'])

