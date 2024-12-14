from flask import Flask, request, jsonify
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

# Load settings from settings.py
app.config.from_pyfile('settings.py')
SECRET_KEY = app.config['SECRET_KEY']  # Access the SECRET_KEY from the config

class PreProcessImage():
    def __init__(self, image_path):
        self.path = image_path

    def resize_with_aspect_ratio(self, width=None, height=None):
        # Get the original image dimensions
        image_before_resize = cv2.imread(self.path)
        h, w = image_before_resize.shape[:2]
        # Calculate the aspect ratio
        aspect_ratio = w / h
        if width is None:
            # Calculate height based on the specified width
            new_height = int(height / aspect_ratio)
            resized_image = cv2.resize(image_before_resize, (height, new_height))
        else:
            # Calculate width based on the specified height
            new_width = int(width * aspect_ratio)
            resized_image = cv2.resize(image_before_resize, (new_width, width))
        cv2.imwrite(self.path, resized_image)
        return 

    def CannyProcess(self):
        image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        smoothed_image = cv2.GaussianBlur(image, (7, 7), 0)
        edges = cv2.Canny(smoothed_image, threshold1=0, threshold2=255)
        kernel = np.ones((3, 3), np.uint8)
        thicker_edges = cv2.dilate(edges, kernel, iterations=1)
        inverted_edges = cv2.bitwise_not(thicker_edges)
        processed_dir = './static/images/processed/'
        os.makedirs(processed_dir, exist_ok=True)
        namename = os.path.basename(self.path)
        filename = os.path.join(processed_dir, namename)
        cv2.imwrite(filename, inverted_edges)

        return self.path, filename  # org_path, processed_path


class ModelApply():
    def __init__(self, org_path, processed_path):
        self.orgpath = org_path
        self.processedpath = processed_path

    def NumberDetect(self):
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=SECRET_KEY
        )
        result = CLIENT.infer(self.processedpath, model_id="number-euwn1/5")

        image = cv2.imread(self.processedpath)
        org_image = cv2.imread(self.orgpath)

        max_confidence = 0
        best_prediction = None

        # Check if detection results contain any predictions
        if "predictions" in result:
            for prediction in result["predictions"]:
                confidence = prediction["confidence"]
                if confidence > max_confidence:
                    max_confidence = confidence
                    best_prediction = prediction

        if best_prediction:
            x_min = int(best_prediction["x"] - best_prediction["width"] / 2)
            y_min = int(best_prediction["y"] - best_prediction["height"] / 2)
            x_max = int(best_prediction["x"] + best_prediction["width"] / 2)
            y_max = int(best_prediction["y"] + best_prediction["height"] / 2)
            label = best_prediction["class"]

            # Draw the bounding box for the best prediction
            cv2.rectangle(org_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Crop the region within the bounding box
            cropped_image = cv2.bitwise_not(image[y_min:y_max, x_min:x_max])
            # Resize the crop to match the bounding box size
            crop_resized = cv2.resize(cropped_image, (x_max - x_min, y_max - y_min))
            # Replace the bounding box area with the resized crop
            org_image[y_min:y_max, x_min:x_max] = crop_resized

            # Put the label with confidence score above the bounding box
            cv2.putText(
                org_image,
                f"{label} ({max_confidence:.2f})",
                (x_min, y_min - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )

        detected_dir = './static/images/detected/'
        os.makedirs(detected_dir, exist_ok=True)
        namename = os.path.basename(self.orgpath)
        filename = os.path.join(detected_dir, namename)
        cv2.imwrite(filename, org_image)

        # Return the filename and label of the highest-confidence prediction
        return filename, label if best_prediction else None

if __name__ == '__main__':
    app.run(debug=True)
