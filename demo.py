#not finall code

import torch
import cv2
import numpy as np
import os

# Set the home directory and model path
home_directory = os.path.expanduser('~/HarvestVision')
model_path = os.path.join(home_directory, 'data', 'yolov8n.pt')

# Load the YOLOv8 model
model = torch.hub.load('ultralytics/yolov8', 'custom', path=model_path)

# Set device to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Define the function to detect rice fields
def detect_rice_fields(frame):
    # Prepare the image for the model
    input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_image = torch.from_numpy(input_image).permute(2, 0, 1).float().unsqueeze(0).to(device)

    # Run the model
    with torch.no_grad():
        results = model(input_image)
    
    # Extract the results
    boxes = results.xyxy[0].cpu().numpy()  # Get the bounding boxes
    for box in boxes:
        x1, y1, x2, y2, conf, cls = box
        if conf > 0.5:  # Confidence threshold
            # Draw the bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"Rice Field: {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

# Capture video from the webcam
cap = cv2.VideoCapture(0) #change the device nummber

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Detect rice fields in the frame
    frame = detect_rice_fields(frame)

    # Display the frame
    cv2.imshow('Rice Field Detection', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
