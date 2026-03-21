# FER CNN Training Script Template
# This script is a template for the Boss to train the actual CNN model.

import os
import cv2
import numpy as np
from config import MODEL_PATH
# import tensorflow as tf
# from tensorflow.keras import layers, models

def load_dataset(data_dir):
    """
    Load and preprocess the emotion dataset (e.g., FER2013).
    """
    print(f"Loading data from {data_dir}...")
    # TODO: Implement dataset loading
    # x_train, y_train = ...
    return None, None

def create_model(input_shape=(48, 48, 1), num_classes=7):
    """
    Define the CNN architecture as per methodology chapter.
    """
    # model = models.Sequential([
    #     layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    #     layers.MaxPooling2D((2, 2)),
    #     layers.Conv2D(64, (3, 3), activation='relu'),
    #     layers.MaxPooling2D((2, 2)),
    #     layers.Flatten(),
    #     layers.Dense(128, activation='relu'),
    #     layers.Dense(num_classes, activation='softmax')
    # ])
    # return model
    print("Creating model architecture...")
    return None

def train():
    """
    Main training loop.
    """
    # 1. Load data: x_train, y_train = load_dataset('path/to/fer2013')
    # 2. Create model: model = create_model()
    # 3. Compile: model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # 4. Fit: model.fit(x_train, y_train, epochs=50, batch_size=64)
    
    # 5. Save: model.save(MODEL_PATH) 
    print(f"Starting training process...")
    print(f"Note: Once trained, the model will be saved to: {MODEL_PATH}")
    print("This will enable the 'is_loaded' flag in the backend.")

if __name__ == "__main__":
    train()
