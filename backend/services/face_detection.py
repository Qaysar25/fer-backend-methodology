import cv2
import numpy as np
import os

class FaceDetectionService:
    def __init__(self):
        # Load the pre-trained Haar Cascade classifier for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            print(f"[ERROR] Failed to load Haar Cascade from {cascade_path}")

    def detect_faces(self, image_path):
        """
        Detect faces in an image using Haar Cascade.
        Returns a list of dicts with x, y, width, height, confidence.
        """
        image = cv2.imread(image_path)
        if image is None:
            return None, "Failed to read image file."

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        # scaleFactor: how much the image size is reduced at each image scale
        # minNeighbors: how many neighbors each candidate rectangle should have
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return [], "No faces detected."

        detected_faces = []
        for (x, y, w, h) in faces:
            # Haar Cascade doesn't provide a direct confidence score, so we'll 
            # provide a mock confidence for the methodology chapter.
            detected_faces.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h),
                'confidence': 0.95  # Mock detection confidence
            })

        return detected_faces, None

    def extract_face_region(self, image_path, face_coords):
        """
        Extract and preprocess face region: grayscale, resize to 48x48, normalize.
        """
        image = cv2.imread(image_path)
        if image is None:
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        x, y, w, h = face_coords['x'], face_coords['y'], face_coords['width'], face_coords['height']
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize to 48x48 for model input (FER methodology standard)
        face_resized = cv2.resize(face_roi, (48, 48))
        
        # Normalize (0 to 1)
        face_normalized = face_resized.astype('float32') / 255.0
        
        return face_normalized
