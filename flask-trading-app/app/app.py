from flask import Flask
from config import Config
from flask_login import LoginManager
from pymongo import MongoClient
from models import User
login_manager = LoginManager()


@login_manager.user_loader
def load_user(username):
    client = MongoClient('Mongo DB Keys')
    user_db = client['Users']
    user_data = user_db.users.find_one({'username': username})
    if user_data:
        return User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=user_data['password_hash']
        )
    return None
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret Key'
    app.config.from_object(Config)
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session lifetime in seconds
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.session_protection = "strong"
    # Initialize MongoDB client
    client = MongoClient('Mongo DB Keys')
    app.config['MONGO_CLIENT'] = client
    app.config['USER_DB'] = client['Users']
    app.config['TRADE_DB'] = client['Trades']

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
