import os
import cv2
import time
from datetime import datetime

# Open the USB camera
cap = cv2.VideoCapture(0)

# Change working directory
os.chdir("/home/alveslab/RGB_Imgs")

width = 1080
height = 800
interval = 0.1  # Time between frames in seconds
duration = 60 * 2  # Total recording duration in seconds
camera_name = "RGB1"

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

start_time = time.time()
last_capture_time = start_time

output_folder = os.path.join(os.getcwd(), f"{camera_name}_{datetime.now().strftime('%Y_%m_%d')}")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created directory: {output_folder}")

print("Starting frame capture...")

while True:
    # Check if the duration has been exceeded
    current_time = time.time()
    if current_time - start_time > duration:
        print("INFO: Snapshot duration completed.")
        break

    # Capture frame only if the interval has passed
    if current_time - last_capture_time >= interval:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            continue  # Skip the rest of the loop if no frame is captured

        frame = cv2.resize(frame, (width, height))

        # Save the frame
        timestamp = datetime.now().strftime('%H%M%S_%f')[:-3]  # Include milliseconds
        frame_path = os.path.join(output_folder, f"{camera_name}_{timestamp}.jpg")
        success = cv2.imwrite(frame_path, frame)
        if not success:
            print("Error: Frame could not be saved at", frame_path)
        else:
            print("Saved frame to:", frame_path)

        # Update the last capture time
        last_capture_time = current_time

# Release the capture
cap.release()
print("Frame capture completed.")

