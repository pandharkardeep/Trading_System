import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://pandharkardeep35:7762Q0QmsBVhYqLF@deep.pfmz7xz.mongodb.net/Users'
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')  or "8d3b7ee5ea0a46fab86f1f0043c8e132"# For News API
    API_KEY = os.environ.get('API_KEY') or "74b10f24c9msh9fd947632f86905p187aebjsne3e91483531a"  # For Trading API
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    