import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACe14a5f8002c846a41f8f27f2f6170595'
    TWILIO_SYNC_SERVICE_SID = 'ISd698abf4544ee0d488749e7feb750a8a'
    TWILIO_API_KEY = 'SK37d7ed70c7d5c850b6e0eb12ea9117bb'
    TWILIO_API_SECRET = 'lEoFA3DXFGYSaH4h4WxEaq73wdN1hwFb'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('downloaded_text.txt', 'w') as f:
        f.write(text_from_notepad)

    path_to_store_text = 'downloaded_text.txt'
    return send_file(path_to_store_text, as_attachment = True)    

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
