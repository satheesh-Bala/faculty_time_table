# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Moulikd345@'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:Moulikd345@localhost/faculty'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
