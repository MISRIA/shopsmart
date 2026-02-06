import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-shopsmart-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///shopsmart.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pagination
    ITEMS_PER_PAGE = 12
    
    # Uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'img', 'uploads')
    
    # AI Config
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
