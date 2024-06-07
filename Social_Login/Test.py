from flask import Flask, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

app = Flask(__name__)

GOOGLE_CLIENT_ID = "your_google_client_id"

@app.route("/login", methods=["POST"])
def login():
    token = request.json.get("token")
    if not token:
        return jsonify({"error": "Token missing"}), 400

    try:
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        google_id = id_info.get("sub")
        name = id_info.get("name")
        # Additional logic to handle user data
        return jsonify({"google_id": google_id, "name": name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route("/protected_area")
def protected_area():
    # Access protected area logic
    return jsonify({"message": "Welcome to the protected area"}), 200

if __name__ == "__main__":
    app.run(debug=True)
