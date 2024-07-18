# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123@localhost/faculty_time_table'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
