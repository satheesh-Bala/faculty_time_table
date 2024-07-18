# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    designation=db.Column(db.String(70),nullable=True)
    id_number = db.Column(db.String(64), nullable=True, unique=True)
    mail = db.Column(db.String(120), nullable=True, unique=True)
    created_by = db.Column(db.String(64), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.String(64), nullable=True)
    modified_on = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Integer,nullable=False)

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    period_1 = db.Column(db.Integer,nullable=True,default=0)
    period_2 = db.Column(db.Integer,nullable=True,default=0)
    period_3 = db.Column(db.Integer,nullable=True,default=0)
    period_4 = db.Column(db.Integer,nullable=True,default=0)
    period_5 = db.Column(db.Integer,nullable=True,default=0)
    period_6 = db.Column(db.Integer,nullable=True,default=0)
    period_7 = db.Column(db.Integer,nullable=True,default=0)
    period_8 = db.Column(db.Integer,nullable=True,default=0)

    faculty = db.relationship('Faculty', backref=db.backref('time_slots', lazy=True))

    def __repr__(self):
        return f'<TimeSlot date={self.date} faculty_id={self.faculty_id}>'