#Libs
from flask import request, jsonify, session, Flask, redirect
from decouple import config as env
from config import config as con
from flask_cors import CORS
import jwt
from routes import Authentification, Bank, Account, Transaction
from utils.db import db
from models import User, UserHistory

app = Flask(__name__)

# Configurations
if env('PRODUCTION', default=False):
    app.config.from_object(con['production'])
else:
    app.config.from_object(con['development'])


cors = CORS(app, resources={
            r'/api/v1/*': {
                'origins': env('FRONT_URL'),
                'allow_headers': ['Authorization', 'Accept', 'Content-Type']
            }
})

db.init_app(app)

def page_not_found(error):
    return '<h1>Page not found<h1>', 404


#Blueprints
#Authentification blueprints
app.register_blueprint(Authentification.auth, url_prefix='/api/v1/auth')

#Bank blueprints
app.register_blueprint(Bank.bank, url_prefix='/api/v1/banks')

#Account blueprints
app.register_blueprint(Account.account, url_prefix='/api/v1/accounts')

#Transctions blueprints
app.register_blueprint(Transaction.transaction, url_prefix='/api/v1/transactions')

# Error handlers
app.register_error_handler(404, page_not_found)

@app.before_request
def session_middleware():
    method = request.method
    if method != 'OPTIONS':
        auth = request.headers.get('Authorization')

        if auth:
            token = auth.split(" ")[1]
            value = jwt.decode(token, env('SECRET_KEY'),
                               algorithms=['HS256'])
            session['Authorization'] = value['id']
        else:
            url = request.base_url
            if not 'auth' in url:
                return jsonify(message='Usuario no valido', context=3), 403


@app.before_request
def audit_middleware():
    method = request.method
    if method != 'OPTIONS':
        auth = request.headers.get('Authorization')
        if auth:
            token = auth.split(" ")[1]
            value = jwt.decode(token, env('SECRET_KEY'),
                               algorithms=['HS256'])
            new_event = UserHistory.UserHistory(value['id'], f'{method} {request.path}')
            db.session.add(new_event)
            db.session.commit()

@app.before_request
def block_redirect_for_options():
    # Evitar redirección para solicitudes OPTIONS
    print(request.headers)
    if request.method == 'OPTIONS':
        return '', 204

@app.after_request
def after_request(response):
    # Establece los encabezados CORS
    response.headers['Access-Control-Allow-Origin'] = env('FRONT_URL')
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
