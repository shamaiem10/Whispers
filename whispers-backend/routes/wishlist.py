from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db, Wishlist

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist/add', methods=['POST'])
@login_required
def add_wishlist():
    whisper_id = request.json.get('whisper_id')
    if Wishlist.query.filter_by(user_id=current_user.id, whisper_id=whisper_id).first():
        return jsonify({"error": "Already in wishlist"}), 400
    new_item = Wishlist(user_id=current_user.id, whisper_id=whisper_id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Added to wishlist"})

@wishlist_bp.route('/wishlist/remove', methods=['POST'])
@login_required
def remove_wishlist():
    whisper_id = request.json.get('whisper_id')
    item = Wishlist.query.filter_by(user_id=current_user.id, whisper_id=whisper_id).first()
    if not item:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Removed from wishlist"})
