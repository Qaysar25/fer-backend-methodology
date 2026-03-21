from database.db import db
from datetime import datetime

class EmotionResult(db.Model):
    __tablename__ = 'emotion_results'
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    face_id = db.Column(db.Integer, db.ForeignKey('faces.face_id'), unique=True, nullable=False)
    emotion = db.Column(db.String(20), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    processing_time = db.Column(db.Float, nullable=False)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
