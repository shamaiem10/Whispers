from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import os

# ----------------- Flask App Setup -----------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- Models -----------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.Text, default="")
    profile_image = db.Column(db.String(300), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    traveler_type = db.Column(db.String(50), default="Adventurer")

    whispers = db.relationship('Whisper', backref='author', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)
    chat_logs = db.relationship('ChatLog', backref='user', lazy=True)


class Whisper(db.Model):
    __tablename__ = 'whispers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    location_name = db.Column(db.String(150))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    visit_date = db.Column(db.Date)
    image_path = db.Column(db.String(300))
    privacy = db.Column(db.String(10), default='Public')
    emotion = db.Column(db.String(50), default="")
    mood_tags = db.Column(db.String(300), default="")
    vibe_tags = db.Column(db.String(300), default="")
    ai_summary = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    whisper_id = db.Column(db.Integer, db.ForeignKey('whispers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatLog(db.Model):
    __tablename__ = 'chatlogs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------- Create Database -----------------
if __name__ == "__main__":
    if not os.path.exists('database.db'):
        print("Creating SQLite database and tables...")
    else:
        print("Database already exists. Tables will be checked/created if missing.")

    with app.app_context():
        db.create_all()
        print("All tables created successfully!")
