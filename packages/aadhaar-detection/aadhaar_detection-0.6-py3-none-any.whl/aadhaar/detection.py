import cv2
import numpy as np
from tensorflow.keras.models import load_model

def predict_aadhaar(input_image_path):
    try:
        # Assuming 'path_to_your_model.h5' is the path to your trained model file
        model = load_model(r'C:\Users\Unknown\Downloads\aadhaar.h5')
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None

    try:
        input_image = cv2.imread(input_image_path)

        if input_image is None:
            raise FileNotFoundError("Image not found or could not be loaded.")
    except Exception as e:
        print(f"Error: {e}")
        # Handle the error appropriately, e.g., exit or ask for a valid path.
        return None

    input_image_resized = cv2.resize(input_image, (128, 128))
    input_image_scaled = input_image_resized / 255
    input_image_reshaped = np.reshape(input_image_scaled, [1, 128, 128, 3])

    input_prediction = model.predict(input_image_reshaped)
    print(input_prediction)

    input_pred_label = np.argmax(input_prediction)

    if input_pred_label == 1:
        return 'This is an Aadhaar card'
    else:
        return 'This is not an Aadhaar card'

if __name__ == "__main__":
    input_image_path = input('Path of the image to be predicted: ')
    result = predict_aadhaar(input_image_path)
    if result:
        print(result)
