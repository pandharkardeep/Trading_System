from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin

mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": user_id})
    if not user:
        return None
    return UserMixin(user)