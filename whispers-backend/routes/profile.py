from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db, User, Whisper

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    whispers_count = Whisper.query.filter_by(user_id=user.id).count()
    countries_visited = Whisper.query.filter_by(user_id=user.id).distinct(Whisper.location_name).count()
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "bio": user.bio,
        "profile_image": user.profile_image,
        "whispers_count": whispers_count,
        "countries_visited": countries_visited,
        "traveler_type": user.traveler_type
    })

@profile_bp.route('/profile/<int:user_id>', methods=['PUT'])
@login_required
def update_profile(user_id):
    if current_user.id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    user = User.query.get(user_id)
    user.name = data.get('name', user.name)
    user.bio = data.get('bio', user.bio)
    user.profile_image = data.get('profile_image', user.profile_image)
    db.session.commit()
    return jsonify({"message": "Profile updated"})
