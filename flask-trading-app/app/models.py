from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, username, email, password=None, password_hash=None):
        self.username = username
        self.email = email
        self.set_password(password)
    
            # Use the hash directly if provided
    def set_password(self, password):
 
        self.password_hash = password

    def check_password(self, password):
       
        return self.password_hash == password

    def get_id(self):
        return self.username  # Assuming username is unique and used as the user ID
