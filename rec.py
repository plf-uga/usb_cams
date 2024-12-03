import os
import cv2
import time
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from threading import Thread

class FrameCaptureApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Frame Capture App")
        self.master.geometry("400x200")

        # Variables
        self.camera_name = StringVar()
        self.is_running = False
        self.interval = 0.1  # Interval between frames in seconds
        self.duration = 60 * 2  # Default duration in seconds
        self.output_folder = "/home/alveslab/RGB_Imgs"

        # Widgets
        Label(master, text="Enter Camera Name:").pack(pady=10)
        self.camera_name_entry = Entry(master, textvariable=self.camera_name)
        self.camera_name_entry.pack(pady=5, fill="x", padx=20)

        Button(master, text="Start Capture", command=self.start_capture).pack(pady=10)
        Button(master, text="Stop Capture", command=self.stop_capture).pack(pady=10)

    def start_capture(self):
        if not self.camera_name.get().strip():
            messagebox.showwarning("Input Error", "Please provide a camera name!")
            return

        self.is_running = True

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Start a separate thread for capturing frames
        Thread(target=self.capture_frames).start()

    def capture_frames(self):
        camera_name = self.camera_name.get().strip()
        cap = cv2.VideoCapture(0)  # Open the USB camera

        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Could not open the camera!")
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        start_time = time.time()
        last_capture_time = start_time

        output_folder = os.path.join(self.output_folder, f"{camera_name}_{datetime.now().strftime('%Y_%m_%d')}")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        print("Starting frame capture...")
        while self.is_running:
            current_time = time.time()
            if current_time - start_time > self.duration:
                print("INFO: Snapshot duration completed.")
                break

            # Capture frame only if the interval has passed
            if current_time - last_capture_time >= self.interval:
                ret, frame = cap.read()
                if ret:
                    frame = cv2.resize(frame, (width, height))
                    timestamp = datetime.now().strftime('%H%M%S_%f')[:-3]  # Include milliseconds
                    frame_path = os.path.join(output_folder, f"{camera_name}_{timestamp}.jpg")
                    success = cv2.imwrite(frame_path, frame)
                    if success:
                        print("Saved frame to:", frame_path)
                    else:
                        print("Error: Frame could not be saved at", frame_path)
                else:
                    print("Error: Could not read frame.")
                last_capture_time = current_time

        cap.release()
        print("Frame capture stopped.")
        messagebox.showinfo("Capture Stopped", "Frame capture has been stopped.")

    def stop_capture(self):
        if self.is_running:
            self.is_running = False
        else:
            messagebox.showwarning("Stop Error", "Capture is not running!")


if __name__ == "__main__":
    root = Tk()
    app = FrameCaptureApp(root)
    root.mainloop()

