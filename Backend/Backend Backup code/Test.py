from flask import Flask, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

GOOGLE_CLIENT_ID = "15290909298-a7t7e7e0hngfmcr6lug01qruf3r3b1eh.apps.googleusercontent.com"

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    token = db.Column(db.String(255), nullable=False)

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

@app.route("/protected_area")
def protected_area():
    # Access protected area logic
    return jsonify({"message": "Welcome to the protected area"}), 200

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


#Senden einer POST-Anfrage an https://example.com/login (ersetze example.com durch die tatsächliche Domain oder URL deines Backends)
