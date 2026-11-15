# This file is being archived on 15.11.2026 and is not part of the new version.
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

# Code can be importet or added to current backend
app = Flask(__name__)
database = 'database.db'
app.secret_key = 'Test'

# init_db, get_db and table_exists ist needed for easier handling
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


# Data has to be extracted by (e.g. login page) with the help of a POST request and a session to then be
# redirected to add_userdata / add_articledata with the needed values
@app.route('/add_userdata', methods=['GET'])
def add_userdata():

    userdata = session['userdata']

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
@app.route('/add_articledata', methods=['GET'])
def add_articledata():
    articledata = session['articledata']

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

# Redirect has to be adjusted to give the needed values to rmv_userdata / rmv_articledata. Works by PRIMARY_KEY ID
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

# Redirect has to be adjusted to give the needed values to update_userdata / update_articledata
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)