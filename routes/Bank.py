import base64

from flask import session, Blueprint, jsonify, request
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, UserHistory
from utils.db import db
import jwt
from datetime import datetime, timedelta
from typing import Dict
from decouple import config

bank = Blueprint('bank', __name__)


@bank.route("/")
def list_banks():
    page: int = request.args.get('page', default=1, type=int)

    secret: str = config("SECRET_ID")
    password: str = config("SECRET_PASSWORD")
    headers: Dict = {
        "accept": "application/json",
        "authorization": f'Basic {base64.b64encode(f"{secret}:{password}".encode()).decode("utf-8")}'
    }
    response = requests.get(f'{config("BELVO_URL")}/api/institutions/?page_size=100&page={page}&type=bank', headers=headers)

    return response.json(), 200

