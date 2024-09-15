# preprocessing.py
import cv2
import os

input_folder = 'images/'
output_folder = 'preprocessed_images/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def preprocess_image(image_path, output_path):
    img = cv2.imread(image_path)

    # Step 1: Resize the image
    img = cv2.resize(img, (800, 800))  # Resizing to a standard size (800x800)

    # Step 2: Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 4: Apply adaptive thresholding
    binary_img = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Step 5: Save the preprocessed image
    cv2.imwrite(output_path, binary_img)

# Preprocess all images in the images folder
def preprocess_all_images():
    for image_file in os.listdir(input_folder):
        if image_file.endswith('.jpg') or image_file.endswith('.png'):
            input_path = os.path.join(input_folder, image_file)
            output_path = os.path.join(output_folder, image_file)
            preprocess_image(input_path, output_path)

if __name__ == '__main__':
    preprocess_all_images()
    print("Preprocessing complete. Preprocessed images saved in 'preprocessed_images/'")
