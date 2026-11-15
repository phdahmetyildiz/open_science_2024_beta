# This file is being archived on 15.11.2026 and is not part of the new version.
import os
import pathlib
import requests
from flask import Flask, render_template, request, redirect, url_for, session
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import sqlite3
import jsonify

# variables needed inside the flask app / methods
app = Flask("Google Login App")
app.secret_key = "Test"
database = 'database.db'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "15290909298-a7t7e7e0hngfmcr6lug01qruf3r3b1eh.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# methods needed inside the flask app
def init_db():
    if not os.path.exists(database):
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS userdata (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        date_of_birth DATE NOT NULL,
                        phone_number TEXT,
                        address TEXT,
                        city TEXT,
                        country TEXT,
                        postal_code TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS articledata (
                        article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        article_name TEXT NOT NULL,
                        description TEXT,
                        author_id INTEGER NOT NULL,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        file_path TEXT NOT NULL,
                        file_size TEXT NOT NULL,
                        file_type TEXT NOT NULL,
                        is_approved BOOLEAN DEFAULT 0
                    )
                ''')

            conn.commit()
    else:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            if not table_exists(cursor, 'userdata'):
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS userdata (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            date_of_birth DATE NOT NULL,
                            phone_number TEXT,
                            address TEXT,
                            city TEXT,
                            country TEXT,
                            postal_code TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
            if not table_exists(cursor, 'articledata'):
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS articledata (
                            article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            article_name TEXT NOT NULL,
                            description TEXT,
                            author_id INTEGER NOT NULL,
                            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            file_path TEXT NOT NULL,
                            file_size TEXT NOT NULL,
                            file_type TEXT NOT NULL,
                            is_approved BOOLEAN DEFAULT 0
                        )
                    ''')

            conn.commit()
def get_db():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn
def table_exists(cursor, table_name):
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
    ''', (table_name,))
    return cursor.fetchone() is not None
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

# app routes

# Database
@app.route('/get_articledata', methods=['GET'])
def get_articledata():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM articledata')
    articledata = cursor.fetchall()
    db.close()
    return jsonify(articledata)
@app.route('/add_userdata', methods=['POST'])
def add_userdata():

    userdata = request.json

    username = userdata['username']
    email = userdata['email']
    password = userdata['password']
    first_name = userdata['first_name']
    last_name = userdata['last_name']
    date_of_birth = userdata['date_of_birth']
    phone_number = userdata.get('phone_number', None)
    address = userdata.get('address', None)
    city = userdata.get('city', None)
    country = userdata.get('country', None)
    postal_code = userdata.get('postal_code', None)

    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
            INSERT INTO userdata (
                username, email, password, first_name, last_name, date_of_birth,
                phone_number, address, city, country, postal_code
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password, first_name, last_name, date_of_birth,
              phone_number, address, city, country, postal_code))

    db.commit()
    db.close()
    return jsonify({"message": "User data added successfully"}), 201
@app.route('/add_articledata', methods=['POST'])
def add_articledata():
    articledata = request.json

    article_name = articledata['article_name']
    description = articledata.get('description', None)
    author_id = articledata['author_id']
    file_path = articledata['file_path']
    file_size = articledata['file_size']
    file_type = articledata['file_type']
    is_approved = articledata.get('is_approved', 0)

    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
            INSERT INTO articledata (
                article_name, description, author_id, file_path, file_size, file_type, is_approved
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (article_name, description, author_id, file_path, file_size, file_type, is_approved))

    db.commit()
    db.close()
    return jsonify({"message": "Article data added successfully"}), 201
@app.route('/rmv_userdata/<int:user_id>', methods=['DELETE'])
def rmv_userdata(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        DELETE FROM userdata WHERE user_id = ?
    ''', (user_id,))
    db.commit()
    db.close()
    return jsonify({"message": f"User data with ID {user_id} removed successfully"}), 200
@app.route('/rmv_articledata/<int:article_id>', methods=['DELETE'])
def rmv_articledata(article_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        DELETE FROM articledata WHERE article_id = ?
    ''', (article_id,))
    db.commit()
    db.close()
    return jsonify({"message": f"Article data with ID {article_id} removed successfully"}), 200
@app.route('/update_userdata/<int:user_id>/<string:row>/<string:new_value>', methods=['GET'])
def update_userdata():
    if row not in userdata:
        return jsonify({"error": f"Field '{row}' not found in user data"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'''
            UPDATE userdata SET {row} = ? WHERE user_id = ?
        ''', (new_value, user_id))
    db.commit()
    db.close()

    return jsonify({"message": f"User data with ID {user_id}, field '{row}' updated successfully"}), 200
@app.route('/update_articledata/<int:article_id>/<string:row>/<string:new_value>', methods=['GET'])

#Social Login
def update_articledata():
    if row not in userdata:
        return jsonify({"error": f"Field '{row}' not found in user data"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'''
            UPDATE articledata SET {row} = ? WHERE article_id = ?
        ''', (new_value, user_id))
    db.commit()
    db.close()

    return jsonify({"message": f"User data with ID {user_id}, field '{row}' updated successfully"}), 200
@app.route("/login", methods=["POST"])
def login():
    token = request.json.get("token")
    if not token:
        return jsonify({"error": "Token missing"}), 400

    try:
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        google_id = id_info.get("sub")
        email = id_info.get("email")
        name = id_info.get("name")

        # Check if user already exists in the database
        user = UserProfile.query.filter_by(google_id=google_id).first()
        if user:
            # Update the user's token
            user.token = token
        else:
            # Create a new user profile
            user = UserProfile(google_id=google_id, email=email, token=token)
            db.session.add(user)

        db.session.commit()

        return jsonify({"google_id": google_id, "email": email, "name": name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"
@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

#Articlemanagement
@app.route('/return_article/<string:keyword>', methods=['GET', 'POST'])
def return_article():
        conn = get_db_connection()
        if conn is not None:
            try:
                cursor = conn.execute('''
                    SELECT * FROM articles WHERE title LIKE ? OR content LIKE ?
                ''', ('%' + keyword + '%', '%' + keyword + '%'))
                results = cursor.fetchall()
                conn.close()
                if results:
                    for i, article in enumerate(results, start=1):
                        jsonify(f"{i}. Titel: {article['title']}, Autor: {article['author']}")
                else:
                    jsonify(f"Keine Artikel gefunden mit dem Stichwort '{keyword}'.")
            except sqlite3.Error as e:
                jsonify(f"Fehler bei der Artikelsuche: {e}")
        else:
            jsonify("Verbindung zur Datenbank konnte nicht hergestellt werden.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


# TODO
# /register app route? (Manual register, without the need of a social account)
# Social login modules (e.g. from google.oauth2 import id_token) have to be added to the venv
# Replace the JSON Part in Articlemanagement and Social login with the SQLite Database
# (Database code might has to be adjusted, based on how the data is provided by the other app routes / frontend)
# (Add Data currently works with Sessions, rmv and update data work with URLs)
