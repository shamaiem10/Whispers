from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from database import db, Whisper
from datetime import datetime
import os

whisper_bp = Blueprint('whispers', __name__)

# ----------------- Helper -----------------
def save_image(image_file):
    if image_file:
        filename = f"{datetime.utcnow().timestamp()}_{image_file.filename}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(path)
        return path
    return ""

# ----------------- Create Whisper -----------------
@whisper_bp.route('/whispers/create', methods=['POST'])
@login_required
def create_whisper():
    title = request.form.get('title')
    content = request.form.get('content')
    location_name = request.form.get('location_name')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    visit_date_str = request.form.get('visit_date')  # string from form
    privacy = request.form.get('privacy', 'Public')
    image = request.files.get('image')
    image_path = save_image(image)

    # Convert visit_date string to a date object
    visit_date = None
    if visit_date_str:
        try:
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Placeholder AI tagging
    emotion = "happy"
    mood_tags = "['adventure','beach']"
    vibe_tags = "['relax','fun']"
    ai_summary = "This was a wonderful travel memory."

    whisper = Whisper(
        user_id=current_user.id,
        title=title,
        content=content,
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        visit_date=visit_date,
        image_path=image_path,
        privacy=privacy,
        emotion=emotion,
        mood_tags=mood_tags,
        vibe_tags=vibe_tags,
        ai_summary=ai_summary
    )
    db.session.add(whisper)
    db.session.commit()
    return jsonify({"message": "Whisper created", "whisper_id": whisper.id})

# ----------------- Get Whisper -----------------
@whisper_bp.route('/whispers/<int:id>', methods=['GET'])
def get_whisper(id):
    w = Whisper.query.get_or_404(id)
    return jsonify({
        "id": w.id,
        "title": w.title,
        "content": w.content,
        "location_name": w.location_name,
        "latitude": w.latitude,
        "longitude": w.longitude,
        "visit_date": w.visit_date.strftime('%Y-%m-%d') if w.visit_date else None,
        "image_path": w.image_path,
        "emotion": w.emotion,
        "mood_tags": w.mood_tags,
        "vibe_tags": w.vibe_tags,
        "ai_summary": w.ai_summary,
        "privacy": w.privacy
    })

# ----------------- Edit Whisper -----------------
@whisper_bp.route('/whispers/<int:id>', methods=['PUT'])
@login_required
def edit_whisper(id):
    w = Whisper.query.get_or_404(id)
    if w.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json

    w.title = data.get('title', w.title)
    w.content = data.get('content', w.content)
    w.privacy = data.get('privacy', w.privacy)

    # Update visit_date if provided
    visit_date_str = data.get('visit_date')
    if visit_date_str:
        try:
            w.visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    db.session.commit()
    return jsonify({"message": "Whisper updated"})

# ----------------- Delete Whisper -----------------
@whisper_bp.route('/whispers/<int:id>', methods=['DELETE'])
@login_required
def delete_whisper(id):
    w = Whisper.query.get_or_404(id)
    if w.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(w)
    db.session.commit()
    return jsonify({"message": "Whisper deleted"})

# ----------------- Get Public Whispers -----------------
@whisper_bp.route('/whispers/public', methods=['GET'])
def public_whispers():
    whispers = Whisper.query.filter_by(privacy="Public").all()
    return jsonify([{
        "id": w.id,
        "title": w.title,
        "latitude": w.latitude,
        "longitude": w.longitude,
        "image_path": w.image_path,
        "emotion": w.emotion
    } for w in whispers])

# ----------------- Explore Filter -----------------
@whisper_bp.route('/explore/filter', methods=['POST'])
def explore_filter():
    filters = request.json
    query = Whisper.query.filter_by(privacy="Public")

    if "emotion" in filters:
        query = query.filter(Whisper.emotion.in_(filters["emotion"]))
    if "mood_tags" in filters:
        query = query.filter(Whisper.mood_tags.contains(filters["mood_tags"]))
    if "vibe_tags" in filters:
        query = query.filter(Whisper.vibe_tags.contains(filters["vibe_tags"]))

    whispers = query.all()
    return jsonify([{
        "id": w.id,
        "title": w.title,
        "latitude": w.latitude,
        "longitude": w.longitude,
        "image_path": w.image_path,
        "emotion": w.emotion
    } for w in whispers])
