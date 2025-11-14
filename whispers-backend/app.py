from flask import Flask
from flask_login import LoginManager
import os
from database import db
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.whispers import whisper_bp
from routes.wishlist import wishlist_bp
from routes.ai import ai_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(whisper_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(ai_bp)

from database import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
