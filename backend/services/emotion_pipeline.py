import os
import time
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, PROCESSING_TIMEOUT
from database.db import db
from database.models import Image, Face, EmotionResult
from services.face_detection import FaceDetectionService
from services.stats_service import StatsService
from models.cnn_model import cnn_model

face_detector = FaceDetectionService()

def save_image(file):
    """Save uploaded image to the uploads folder."""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    unique_filename = f"{int(time.time())}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)
    return unique_filename, file_path

def process_image(file, user_id=None):
    """
    Main pipeline for processing an uploaded image (FER Methodology Compliant).
    Detects faces, predicts emotions, and updates dashboard stats.
    """
    start_time = time.time()

    # 1. Save image
    filename, file_path = save_image(file)

    # 2. Add image record to DB
    new_image = Image(user_id=user_id, filename=filename, file_path=file_path)
    db.session.add(new_image)
    db.session.flush()

    # 3. Detect faces (Methodology step 3.1)
    faces, error = face_detector.detect_faces(file_path)
    if error and not faces:
        return {'status': 'error', 'message': error}

    results = []
    for face_data in faces:
        # 4. Create Face record
        new_face = Face(
            image_id=new_image.image_id,
            x_coordinate=face_data['x'],
            y_coordinate=face_data['y'],
            width=face_data['width'],
            height=face_data['height'],
            detection_confidence=face_data['confidence']
        )
        db.session.add(new_face)
        db.session.flush()

        # 5. Extract and Preprocess (Methodology standard: 48x48)
        face_region = face_detector.extract_face_region(file_path, face_data)
        
        # 6. Predict emotion (Methodology step 3.2 - CNN Model)
        prediction = cnn_model.predict(face_region)
        
        # Calculate individual processing time
        face_processing_time = round((time.time() - start_time) * 1000, 2)

        # 7. Create EmotionResult record
        result_record = EmotionResult(
            face_id=new_face.face_id,
            emotion=prediction['emotion'],
            confidence_score=prediction['confidence'],
            processing_time=face_processing_time
        )
        db.session.add(result_record)
        
        results.append({
            'emotion': result_record.emotion,
            'confidence': result_record.confidence_score,
            'bbox': face_data
        })

    db.session.commit()

    # 8. Update Dashboard Statistics
    StatsService.update_dashboard_stats()

    total_processing_time = round((time.time() - start_time), 2)
    
    # NFR1 Validation: must be < 3 seconds
    status = 'success' if total_processing_time < PROCESSING_TIMEOUT else 'warning'

    return {
        'status': status,
        'results': results,
        'processing_time': total_processing_time,
        'total_faces': len(faces)
    }
