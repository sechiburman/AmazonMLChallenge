# ocr_extraction.py
import pytesseract
from PIL import Image
import os
import csv

# Extract text from a single image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Extract text from all images in the folder and save to a CSV file
def extract_text_from_images(image_folder, output_file='ocr_output.csv'):
    text_data = {}

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['image_file', 'extracted_text'])  # CSV header

        for image_file in os.listdir(image_folder):
            if image_file.endswith('.jpg') or image_file.endswith('.png'):
                image_path = os.path.join(image_folder, image_file)
                text = extract_text_from_image(image_path)
                text_data[image_file] = text
                writer.writerow([image_file, text])  # Save image file and its OCR text
                print(f"Text extracted from {image_file}: {text}")
    
    return text_data

if __name__ == '__main__':
    text_data = extract_text_from_images('preprocessed_images')
    print("OCR complete. Results saved in 'ocr_output.csv'.")
