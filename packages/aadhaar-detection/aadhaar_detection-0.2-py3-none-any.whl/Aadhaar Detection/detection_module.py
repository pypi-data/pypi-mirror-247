# aadhaar_detection/detection_module.py

import cv2
import numpy as np
from tensorflow import keras
import os

# Define the default model path
DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'aadhaar.h5')

def predict_aadhaar(image_path, model_path=None):
    # If model path is not provided, use the default model path
    if model_path is None:
        model_path = DEFAULT_MODEL_PATH

    # Load the trained model
    model = keras.models.load_model(model_path)

    # Load and preprocess the input image
    input_image = cv2.imread(image_path)
    input_image_resized = cv2.resize(input_image, (128, 128))
    input_image_scaled = input_image_resized / 255
    input_image_reshaped = np.reshape(input_image_scaled, [1, 128, 128, 3])

    # Make a prediction using the loaded model
    input_prediction = model.predict(input_image_reshaped)

    # Determine the predicted label
    input_pred_label = np.argmax(input_prediction)

    # Return the result based on the predicted label
    if input_pred_label == 1:
        return 'This is an Aadhaar card'
    else:
        return 'This is not an Aadhaar card'
