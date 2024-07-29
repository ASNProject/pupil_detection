import csv
import os

import cv2
from PIL import Image
import math
import numpy as np
from datetime import datetime


# Buka gambar
# image_path = 'assets/images/1.png'

def check_resolution(image_path):
    with Image.open(image_path) as img:
        # Dapatkan sesolusi gambar
        width, height = img.size
        print(f"Resolusi gambar: {width}x{height}")


def calculate_pixel_to_mm(image_width, image_height, diagonal_size):
    ppi = math.sqrt(image_width ** 2 + image_height ** 2) / diagonal_size
    ppm = ppi / 25.4
    return ppm


def detect_pupil(frame, hsv_ranges):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definisikan rentang warna untuk pupil
    lower_black = np.array([hsv_ranges["pupil"]["LH"], hsv_ranges["pupil"]["LS"], hsv_ranges["pupil"]["LV"]])
    upper_black = np.array([hsv_ranges["pupil"]["UH"], hsv_ranges["pupil"]["US"], hsv_ranges["pupil"]["UV"]])

    # Masking warna pupil
    mask = cv2.inRange(hsv, lower_black, upper_black)
    masked = cv2.bitwise_and(frame, frame, mask=mask)

    # Temukan kontur
    gray_mask = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    diameter_mm = None

    if contours:
        max_contours = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(max_contours)
        center = (int(x), int(y))
        radius = int(radius)

        # Hitung diameter (assuming calculate_pixel_to_mm is defined elsewhere)
        diameter_px = 2 * radius
        diameter_mm = diameter_px / calculate_pixel_to_mm(1280, 720, 14)
        print(f'Diameter Pupil: {diameter_mm} mm')

        # Gambar lingkaran pada gambar
        cv2.circle(frame, center, radius, (255, 0, 0), 4)
        cv2.rectangle(frame, (center[0] - 5, center[1] - 5), (center[0] + 5, center[1] + 5), (0, 128, 255), -1)

    return frame, diameter_mm


def save_image(frame):
    # Define the directory to save images
    save_dir = "assets/images"

    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define the filename with a timestamp
    filename = os.path.join(save_dir, f"captured_image_{timestamp}.png")
    cv2.imwrite(filename, frame)
    print(f"Image saved as {filename}")
    return  filename


def save_to_csv(filename, diameter):
    csv_file = 'pupil_data.csv'
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Filename', 'Diameter (mm)'])
        writer.writerow([filename, diameter])
