#Client- ID = 15290909298-a7t7e7e0hngfmcr6lug01qruf3r3b1eh.apps.googleusercontent.com
#Client- KEY= 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
#URL -      = http://localhost:5000/authorize


# requirements 

#pip install Flask oauthlib requests-oauthlib

from flask import Flask, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)

# Secret Key zur Sicherung der Sitzungen.
app.secret_key = 'macro'

# Google OAuth 2.0 Client ID und Client Secret.
app.config['GOOGLE_CLIENT_ID'] = '15290909298-a7t7e7e0hngfmcr6lug01qruf3r3b1eh.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    client_kwargs={'scope': 'openid profile email'},
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo'
)

@app.route('/')
def index():
    email = dict(session).get('email', None)
    return f'Hello, {email}!'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/authorize')
def authorize():
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        session['email'] = user_info['email']
        return redirect('/')
    except Exception as e:
        # Fehler Loggen
        print(f'Authorization failed: {str(e)}')
        return jsonify(error=f'Authorization failed: {str(e)}'), 400

if __name__ == '__main__':
    app.run(debug=True)


