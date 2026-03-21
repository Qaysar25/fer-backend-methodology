EMOTION_CATEGORIES = [
    'Happy', 
    'Sad', 
    'Angry', 
    'Surprise', 
    'Fear', 
    'Disgust', 
    'Neutral'
]

# Mapping to index if needed for model
EMOTION_MAP = {emotion: i for i, emotion in enumerate(EMOTION_CATEGORIES)}
