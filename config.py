import sys
import traceback

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_cors import CORS
from flask_qrcode import QRcode
import os
import qrcode
from werkzeug.exceptions import HTTPException

flask_app = Flask(__name__)
qrcode = QRcode(flask_app)

CORS(flask_app, resources=r"/api/*")

#workaround for heroku and sqlalchemy 1.4 https://stackoverflow.com/a/66794960
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
     uri = uri.replace("postgres://", "postgresql://", 1)

flask_app.config["SQLALCHEMY_DATABASE_URI"] = uri

flask_app.config["FRONTEND_URI"] = os.environ["FRONTEND_URI"]
flask_app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
#squelch warning, per https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(flask_app)

from init_db import init_app

@flask_app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    print("Message:",str(e))
    print(traceback.print_exc())
    return jsonify(error=str(e)), code

init_app(flask_app)

migrate = Migrate(flask_app, db)
