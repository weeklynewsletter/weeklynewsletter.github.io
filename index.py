from flask import Flask, request, send_file
import firebase_admin
from firebase_admin import credentials, db
import json
import os

# Build firebase.json from env vars, once, at startup
cred_dict = {
    "type": os.environ["TYPE"],
    "project_id": os.environ["PROJECT_ID"],
    "private_key_id": os.environ["PRIVATE_KEY_ID"],
    "private_key": os.environ["PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": os.environ["CLIENT_EMAIL"],
    "client_id": os.environ["CLIENT_ID"],
    "auth_uri": os.environ["AUTH_URI"],
    "token_uri": os.environ["TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": os.environ["CLIENT_X509_CERT_URL"],
    "universe_domain": os.environ.get("UNIVERSE_DOMAIN", "googleapis.com"),
}

with open("firebase.json", "w") as f:
    json.dump(cred_dict, f)

app = Flask(__name__)

cred = credentials.Certificate("firebase.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://newsletter-a2313-default-rtdb.firebaseio.com"
})


@app.route('/')
def home():
    return send_file("index.html")


@app.route('/run-task', methods=['POST'])
def run_task():
    email = request.form.get('email')
    ref = db.reference("subscribers")
    ref.push({"email": email})
    return "Successfully subscribed!"


if __name__ == '__main__':
    app.run(debug=True)