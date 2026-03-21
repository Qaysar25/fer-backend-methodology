import os
import cv2
from config import ALLOWED_EXTENSIONS


def validate_image(file):
    """
    Validate the uploaded image file.

    Returns:
        (True, None)            if the file is valid.
        (False, error_message)  if validation fails.
    """
    if file is None or file.filename == '':
        return False, 'No image file provided.'

    # Check file extension
    extension = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if extension not in ALLOWED_EXTENSIONS:
        return False, f'Invalid file format. Allowed formats: {", ".join(ALLOWED_EXTENSIONS)}'

    return True, None


def read_image(path):
    """
    Read an image from disk using OpenCV.

    Args:
        path: Absolute path to the image file.

    Returns:
        numpy.ndarray  –  the image in BGR format, or None on failure.
    """
    if not os.path.exists(path):
        return None

    image = cv2.imread(path)
    return image
