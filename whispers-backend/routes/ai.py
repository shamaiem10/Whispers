from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db, ChatLog

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai/echo', methods=['POST'])
@login_required
def echo():
    message = request.json.get('message')
    response = f"Echo AI says: You said '{message}'"
    chat = ChatLog(user_id=current_user.id, message=message, response=response)
    db.session.add(chat)
    db.session.commit()
    return jsonify({"response": response})

@ai_bp.route('/ai/ambient-sound', methods=['POST'])
@login_required
def ambient_sound():
    whisper_id = request.json.get('whisper_id')
    # Placeholder: return static sound URL
    return jsonify({"url": "https://example.com/ambient.mp3"})

@ai_bp.route('/ai/travel-tips', methods=['POST'])
@login_required
def travel_tips():
    whisper_id = request.json.get('whisper_id')
    # Placeholder tips
    tips = [
        "Visit the local market early in the morning.",
        "Try local cuisine at a hidden gem restaurant."
    ]
    return jsonify({"tips": tips})

@ai_bp.route('/stats/<int:user_id>', methods=['GET'])
def travel_graph(user_id):
    # Placeholder stats
    return jsonify({
        "places_visited": ["Paris","Tokyo","Bali"],
        "emotions": ["happy","relaxed","excited"],
        "insights": ["You enjoy calm nature spots", "Your happiest trips were near the ocean"]
    })
