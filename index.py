from flask import Flask, request, send_file
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase
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

    # Add email to Firebase
    ref = db.reference("subscribers")
    ref.push({
        "email": email
    })

    return "Successfully subscribed!"


if __name__ == '__main__':
    app.run(debug=True)