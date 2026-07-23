# Smart Surveillance System

A deep learning-based smart surveillance system that automatically detects unauthorized intrusions and analyzes suspicious human behavior in real time.

## Overview
This project provides a simple, easy-to-implement foundation for a smart surveillance system. 
- **Object Detection:** Uses YOLOv8 (You Only Look Once) to identify humans in a video stream.
- **Behavior Analysis:** Analyzes movement patterns (currently mocked with placeholder logic, ready for an LSTM/CNN model integration).
- **Alert System:** Automatically logs alerts and saves screenshots when suspicious activity is detected.

## Directory Structure
- `backend/`: Core application scripts (`app.py`, `detector.py`, etc.)
- `models/`: Location to store model weights (e.g., YOLO `.pt` files, Keras `.h5` files)
- `dataset/`: Folder for training datasets.
- `screenshots/`: Where the system saves images of suspicious activity.
- `videos/`: Place sample video files here.

## Setup Instructions

1. **Create and activate a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Navigate into the `backend` folder and run `app.py`:
   ```bash
   cd backend
   python app.py
   ```
   By default this uses your computer's webcam (`source 0`). To use a video file stored in the workspace `videos/` folder, pass the file name or path with `--source`:
   ```bash
   python app.py --source "sample.mp4"
   ```
   or from the workspace root:
   ```bash
   python backend/app.py --source "videos/sample.mp4"
   ```
   The app will detect people in the video and flag suspicious behavior based on movement patterns.
