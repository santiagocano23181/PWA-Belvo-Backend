from flask import session, Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, UserHistory
from utils.db import db
import jwt
from datetime import datetime, timedelta
from typing import Dict
from decouple import config

auth = Blueprint('authentication', __name__)


@auth.route('/', methods=["POST"])
def user_register():
    user = User.User.query.filter_by(
        email=request.json["email"]
    ).first()

    if user is not None:
        return jsonify(messages="El usuario ya existe", context=2), 401

    new_user = User.User(request.json["email"], generate_password_hash(request.json["password"], method="pbkdf2:sha256"))

    db.session.add(new_user)
    db.session.commit()

    user = User.User.query.filter_by(
        email=request.json["email"]
    ).first()

    new_event = UserHistory.UserHistory(user.id, f'{request.method} {request.path}')
    db.session.add(new_event)
    db.session.commit()

    return (
        jsonify(
            messages="Usuario registrado",
            context=1,
        ),
        200,
    )


@auth.route('/login', methods=["POST"])
def user_login():
    try:
        user = User.User.query.filter_by(
            email=request.json["email"]
        ).first()

        if user is None:
            return (
                jsonify(
                    messages="Email incorrecto, usuario no registrado"
                ),
                404,
            )

        if not check_password_hash(user.password, request.json["password"]):
            return (
                jsonify(
                    messages="Asegurate que los datos son correctos e intentalo de nuevo"
                ),
                404,
            )

        new_event = UserHistory.UserHistory(user.id, f'{request.method} {request.path}')
        db.session.add(new_event)
        db.session.commit()

        session["user_session"] = user.id
        actual = datetime.now()
        session["exp_time"] = user.exp_time = actual + timedelta(minutes=15)

        user_dict: Dict = {
            'id': jwt.encode(
                {'id': user.id}, config("SECRET_KEY"), algorithm='HS256'
            )
        }
        return jsonify(user_dict), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
