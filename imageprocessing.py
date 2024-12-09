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

    def CannyProcess(self):
        # Load the image
        image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        # Apply GaussianBlur to reduce noise
        smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)
        # Apply Canny edge detector
        edges = cv2.Canny(smoothed_image, threshold1=100, threshold2=110)
        # Create a kernel for dilation
        kernel = np.ones((1, 1), np.uint8)
        # Apply dilation to thicken edges
        thicker_edges = cv2.dilate(edges, kernel, iterations=1)
        # Ensure the processed directory exists
        processed_dir = './static/images/processed/'
        os.makedirs(processed_dir, exist_ok=True)
        # Filename
        namename = os.path.basename(self.path)
        filename = os.path.join(processed_dir, namename)
        # Save the processed image
        cv2.imwrite(filename, thicker_edges)

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

        # Check if detection results contain any predictions
        if "predictions" in result:
            for prediction in result["predictions"]:
                x_min = int(prediction["x"] - prediction["width"] / 2)
                y_min = int(prediction["y"] - prediction["height"] / 2)
                x_max = int(prediction["x"] + prediction["width"] / 2)
                y_max = int(prediction["y"] + prediction["height"] / 2)
                label = prediction["class"]
                confidence = prediction["confidence"]

                # Draw the bounding box
                cv2.rectangle(org_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # Crop the region within the bounding box
                cropped_image = image[y_min:y_max, x_min:x_max]
                # Resize the crop to match the bounding box size
                crop_resized = cv2.resize(cropped_image, (x_max - x_min, y_max - y_min))
                # Replace the bounding box area with the resized crop
                org_image[y_min:y_max, x_min:x_max] = crop_resized

                # Put the label with confidence score above the bounding box
                cv2.putText(
                    org_image,
                    f"{label} ({confidence:.2f})",
                    (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                )

        # Ensure the detected directory exists
        detected_dir = './static/images/detected/'
        os.makedirs(detected_dir, exist_ok=True)

        # Filename
        namename = os.path.basename(self.orgpath)
        filename = os.path.join(detected_dir, namename)

        # Save the processed image
        cv2.imwrite(filename, org_image)

        return filename

if __name__ == '__main__':
    app.run(debug=True)
