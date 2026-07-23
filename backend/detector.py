import cv2
from ultralytics import YOLO

class IntrusionDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # Load the YOLO model (will download automatically if not present in the current dir)
        self.model = YOLO(model_path)
    
    def detect(self, frame):
        # Run inference on the frame
        # classes=[0] filters to only detect 'person'
        results = self.model(frame, classes=[0], verbose=False) 
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # get coordinates and confidence
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                conf = float(box.conf[0])
                detections.append({'box': (x1, y1, x2, y2), 'confidence': conf})
                
        # Return raw detections and the frame with bounding boxes drawn
        return detections, results[0].plot()
