import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'Mongo_URI
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')  or "NewsAPIKEY"# For News API
    API_KEY = os.environ.get('API_KEY') or "FMP_API_KEY"  # For Trading API
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    
