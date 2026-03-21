from database.db import db
from datetime import datetime

class Face(db.Model):
    __tablename__ = 'faces'
    face_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_id = db.Column(db.Integer, db.ForeignKey('Images.image_id'), nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False)
    y_coordinate = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    detection_confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    emotion_result = db.relationship('EmotionResult', backref='face', uselist=False, cascade='all, delete-orphan', lazy=True)
