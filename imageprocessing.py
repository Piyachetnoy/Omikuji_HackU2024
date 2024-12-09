import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class ModelApply():
    def __init__(self, image_path):
        self.path = image_path

    def getPath(self):
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

# # Display the results
# plt.figure(figsize=(8, 4))
# plt.subplot(121), plt.imshow(image, cmap='gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(edges, cmap='gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()