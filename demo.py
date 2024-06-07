#not finall code

import torch
import cv2
import numpy as np
import time
import os
from ultralytics import YOLO  # Make sure you have the ultralytics package installed

pTime = 0

# Set the home directory and model path
home_directory = os.path.expanduser('/media/nops/disk2/Download/perkuliahan/yolo/HarvestVision')
model_path = os.path.join(home_directory, 'data', 'yolov8n.pt')

# Load the YOLOv8 model
model = YOLO(model_path)
model.to('cuda' if torch.cuda.is_available() else 'cpu')  # Move model to GPU if available

# Define a dictionary to map class indices to class names
class_names = {
    0: 'Healthy 1 Month',
    1: 'Unhealthy 1 Month',
    2: 'Healthy 2 Months',
    3: 'Unhealthy 2 Months',
    4: 'Healthy 3 Months',
    5: 'Unhealthy 3 Months',
}

# Define the function to detect rice fields
def detect_rice_fields(frame, current_age):
    # Prepare the image for the model
    input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_image = torch.from_numpy(input_image).permute(2, 0, 1).float().unsqueeze(0) / 255.0  # Normalize to [0, 1]
    input_image = input_image.to('cuda' if torch.cuda.is_available() else 'cpu')

    # Run the model
    results = model(input_image)

    # Extract the results
    boxes = results[0].boxes  # Assuming results[0] is a detection result with a 'boxes' attribute
    unhealthy_count = 0

    # Iterate over the boxes
    for i in range(boxes.xyxy.shape[0]):
        x1, y1, x2, y2 = boxes.xyxy[i]
        conf = boxes.conf[i]
        cls = boxes.cls[i]

        cls = int(cls)
        if conf > 0.5:  # Confidence threshold
            # Determine if the detection matches the current age
            class_name = class_names.get(cls, 'Unknown')
            if str(current_age) in class_name:
                color = (0, 255, 0) if 'Healthy' in class_name else (0, 0, 255)
                label = f"{class_name}: {conf:.2f}"
                if 'Unhealthy' in class_name:
                    unhealthy_count += 1
            else:
                color = (0, 0, 255)
                label = f"Unusual: {class_name} ({conf:.2f})"
                unhealthy_count += 1  # Count as unhealthy if unusual for the age
            
            # Draw the bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return frame, unhealthy_count

# Capture video from the webcam or load an image
use_webcam = True  # Set to False to use a local image

if use_webcam:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # Define the current age of the crop in months
    current_age = 1  # Change this based on the crop's age

    pTime = 0

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        # Detect rice fields in the frame
        frame, unhealthy_count = detect_rice_fields(frame, current_age)
        
        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the count of unhealthy areas
        cv2.putText(frame, f'Unhealthy areas: {unhealthy_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show the frame
        cv2.imshow('Rice Field Detection', frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
else:
    # Load the local image
    image_path = os.path.join(home_directory, 'data', 'source', 'rice_field.jpg')
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Error: Unable to load image from {image_path}")
        exit()

    # Define the current age of the crop in months
    current_age = 1  # Change this based on the crop's age

    # Detect rice fields in the image
    frame, unhealthy_count = detect_rice_fields(frame, current_age)

    # Display the image with the count of unhealthy areas
    cv2.putText(frame, f'Unhealthy areas: {unhealthy_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Rice Field Detection', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


