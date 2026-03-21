from database.db import db
from database.models import Image, Face, EmotionResult, DashboardStats
from sqlalchemy import func
from utils.constants import EMOTION_CATEGORIES
import json

class StatsService:
    @staticmethod
    def update_dashboard_stats():
        """
        Recalculate all aggregates and save to DashboardStats table.
        """
        total_images = Image.query.count()
        total_faces = Face.query.count()
        
        # Average Confidence
        avg_confidence = db.session.query(func.avg(EmotionResult.confidence_score)).scalar() or 0.0
        
        # Average Processing Time
        avg_processing_time = db.session.query(func.avg(EmotionResult.processing_time)).scalar() or 0.0
        
        # Emotion Counts
        emotion_counts = {}
        for emotion in EMOTION_CATEGORIES:
            count = EmotionResult.query.filter_by(emotion=emotion).count()
            emotion_counts[emotion] = count
            
        # Update or Create Stats Record
        stats = DashboardStats.query.first()
        if not stats:
            stats = DashboardStats()
            db.session.add(stats)
            
        stats.total_images = total_images
        stats.total_faces = total_faces
        stats.avg_confidence = avg_confidence
        stats.emotion_counts = emotion_counts
        stats.avg_processing_time = avg_processing_time
        
        db.session.commit()
        return stats

    @staticmethod
    def get_dashboard_stats():
        """
        Return current dashboard stats including most_common_emotion.
        """
        stats = DashboardStats.query.first()
        if not stats:
            # If no stats yet, trigger an update
            stats = StatsService.update_dashboard_stats()
            
        data = stats.to_dict()
        
        # Determine most common emotion
        counts = stats.emotion_counts or {}
        if counts:
            most_common = max(counts, key=counts.get) if any(counts.values()) else "None"
            data["most_common_emotion"] = most_common
        else:
            data["most_common_emotion"] = "None"
            
        return data

    @staticmethod
    def get_user_stats(user_id):
        """
        Return statistics for a specific user.
        """
        total_uploads = Image.query.filter_by(user_id=user_id).count()
        
        # User's faces and emotion results
        user_data = db.session.query(EmotionResult).join(Face).join(Image).filter(Image.user_id == user_id).all()
        
        total_faces = len(user_data)
        
        # Confidence distribution
        avg_conf = sum(r.confidence_score for r in user_data) / total_faces if total_faces > 0 else 0
        
        # Emotion distribution
        dist = {emotion: 0 for emotion in EMOTION_CATEGORIES}
        for r in user_data:
            dist[r.emotion] += 1
            
        return {
            "total_uploads": total_uploads,
            "total_faces": total_faces,
            "avg_confidence": round(avg_conf, 2),
            "emotion_distribution": dist
        }
