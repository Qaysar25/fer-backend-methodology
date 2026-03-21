from database.db import db
from datetime import datetime

class DashboardStats(db.Model):
    __tablename__ = 'dashboard_stats'
    stat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_images = db.Column(db.Integer, default=0)
    total_faces = db.Column(db.Integer, default=0)
    avg_confidence = db.Column(db.Float, default=0.0)
    emotion_counts = db.Column(db.JSON)  # Stores dict of {emotion: count}
    avg_processing_time = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "total_images": self.total_images,
            "total_faces": self.total_faces,
            "avg_confidence": round(self.avg_confidence, 2),
            "emotion_counts": self.emotion_counts,
            "avg_processing_time": round(self.avg_processing_time, 2),
            "last_updated": self.last_updated.isoformat()
        }
