from database.db import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'Images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    faces = db.relationship('Face', backref='image', cascade='all, delete-orphan', lazy=True)
