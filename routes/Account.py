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

account = Blueprint('account', __name__)


@account.route("/<string:bank_name>")
def list_accounts(bank_name: str):
    secret: str = config("SECRET_ID")
    password: str = config("SECRET_PASSWORD")

    page: int = request.args.get('page', default=1, type=int)
    headers: Dict = {
        "accept": "application/json",
        "authorization": f'Basic {base64.b64encode(f"{secret}:{password}".encode()).decode("utf-8")}'
    }
    response = requests.get(f'{config("BELVO_URL")}/api/accounts/?page_size=100&page={page}&institution={bank_name}', headers=headers)

    return response.json(), 200
