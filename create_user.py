from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from models import db, User, Faculty

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_initial_user():    
    admin = User(username='admin2')
    admin.set_password('123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created")

create_initial_user()