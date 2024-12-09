import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class PreProcessImage():
    def __init__(self, image_path):
        self.path = image_path

    def CannyProcess(self):
        # Load the image
        image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

        # Apply GaussianBlur to reduce noise
        smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)

        # Apply Canny edge detector
        edges = cv2.Canny(smoothed_image, threshold1=30, threshold2=150)

        # Ensure the processed directory exists
        processed_dir = './static/processed/'
        os.makedirs(processed_dir, exist_ok=True)

        # Filename
        namename = os.path.basename(self.path)
        filename = os.path.join(processed_dir, namename)

        # Save the processed image
        cv2.imwrite(filename, edges)

        return filename
    
class ModelApply():
    def __init__(self, processed_path):
        self.path = processed_path

    def NumberDetect(self):
        pass
