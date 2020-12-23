from flask import Flask, request
import flaskr.config

from flask_cors import *

# app = Flask(__name__)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['UPLOADED_PHOTOS_DEST'] = 'flaskr/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
import flaskr.views
