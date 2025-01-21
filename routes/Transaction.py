import base64
from array import array

from flask import session, Blueprint, jsonify, request
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, UserHistory
from utils.db import db
import jwt
from datetime import datetime, timedelta
from typing import Dict
from decouple import config
from functools import reduce

transaction = Blueprint('transaction', __name__)


@transaction.route("/<string:link>/<string:id>")
def list_banks(link: str, id: str):
    secret: str = config("SECRET_ID")
    password: str = config("SECRET_PASSWORD")

    page: int = 1
    headers: Dict = {
        "accept": "application/json",
        "authorization": f'Basic {base64.b64encode(f"{secret}:{password}".encode()).decode("utf-8")}'
    }
    transactions: list = []
    balance: float = 0
    while True:
        response = requests.get(
            f'{config("BELVO_URL")}/api/transactions/?link={link}&page_size=100&fields=name%2Cnumber%2Cdescription%2Ctype%2Camount&account={id}&page_size=100&page={page}',
            headers=headers)

        if response.status_code != 200 or len(response.json()['results']) == 0:
            break
        transactions += response.json()['results']
        print(response.json()['results'])
        balance += reduce(get_balance, response.json()['results'])
        if response.json()['next'] is None:
            break

        page += 1
    objectResponse: Dict = {
        'balance': balance,
        'transactions': transactions
    }
    return objectResponse, 200


def get_balance(a, b):
    c: int = b['amount']
    if b['type'] == 'OUTFLOW':
        c = b['amount'] * -1
    if isinstance(a, dict):
        if a['type'] == 'OUTFLOW':
            a = a['amount'] * -1
        else:
            a = a['amount']
    return round(a + c, 2)
