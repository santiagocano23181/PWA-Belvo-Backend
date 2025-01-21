from main import app
from utils.db import db
from models.User import User
from models.UserHistory import UserHistory

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()