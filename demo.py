#not final code

import torch
import cv2
import numpy as np
import time
import os
from torchvision import transforms
from ultralytics import YOLO
from collections import deque

from class_names import class_names

pTime = 0

# Set the home directory and model path
home_directory = os.path.expanduser('~/HarvestVision')
model_path = os.path.join(home_directory, 'best.pt') # path your model
result_path = os.path.join(home_directory, 'result', 'out.txt')
image_path = os.path.join(home_directory, 'data', 'source', '1.jpg')
result_images_path = os.path.join(home_directory, 'result', 'images')

# Create result images directory if it doesn't exist
os.makedirs(result_images_path, exist_ok=True)

# Load the YOLOv8 model
model = YOLO(model_path)
model.to('cuda' if torch.cuda.is_available() else 'cpu')  # Move model to GPU if available

# Use torchvision transforms only
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize(size=(640, 640))  # Resize to model's expected input size
])

img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
img_tensor = transform(img).unsqueeze(0)  # Add batch dimension
img_tensor = img_tensor.to('cuda' if torch.cuda.is_available() else 'cpu')  # Move tensor to GPU if available

# Print the shape of the tensor to debug
print(f"Image tensor shape after resizing: {img_tensor.shape}")

# Ensure the input tensor has the correct shape
if img_tensor.shape[-2] % 32 != 0 or img_tensor.shape[-1] % 32 != 0:
    raise ValueError(f"Input shape {img_tensor.shape} is not divisible by 32.")

model(img_tensor)

# Function to estimate rice field age based on color
def estimate_rice_field_age(frame):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    avg_hue = np.mean(hsv_image[:, :, 0])
    # Convert hue to week (this is a simple heuristic, adjust accordingly)
    estimated_week = int((avg_hue / 180) * 16)  # 180 is the max hue value in HSV color space
    estimated_week = min(max(estimated_week, 1), 16)  # Clamp the value between 1 and 16
    return estimated_week

# Function to detect rice fields
def detect_rice_fields(frame):
    input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_image = torch.from_numpy(input_image).permute(2, 0, 1).float().unsqueeze(0) / 255.0  # Normalize to [0, 1]
    input_image = input_image.to('cuda' if torch.cuda.is_available() else 'cpu')

    results = model(input_image)
    print("Model Results: ", results)

    detected_boxes = []

    for result in results:
        if not hasattr(result, 'boxes'):
            print("No 'boxes' attribute in result")
            continue

        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]
            cls = int(box.cls[0])
            print(f"Box: (
            {x1}, 
            {y1}, 
            {x2}, 
            {y2}), 
            Conf: {conf}, 
            Class: {cls}")

            if conf > 0.5:  # Confidence threshold
                class_name = class_names.get(cls, 'Unknown')
                detected_boxes.append
                (
                    (
                    x1.item(), 
                    y1.item(), 
                    x2.item(), 
                    y2.item(), 
                    conf.item(), 
                    cls, 
                    class_name
                    )
                )

    return frame, detected_boxes

# Function to draw boxes
def draw_boxes(frame, detected_boxes):
    for (x1, y1, x2, y2, conf, cls, class_name) in detected_boxes:
        if class_name == 'Brown Spot Disease':
            color = (0, 0, 255)  # Red for unhealthy area
        elif 'early stage' in class_name:
            color = (0, 255, 0)  # Green for early stage
        elif 'mid stage' in class_name:
            color = (255, 255, 0)  # Cyan for mid stage
        elif 'harvesting stage' in class_name:
            color = (0, 255, 255)  # Yellow for harvesting stage
        else:
            color = (255, 0, 0)  # Blue for other stages

        cv2.rectangle(frame, 
                      (int(x1), 
                       int(y1)), 
                      (int(x2), 
                       int(y2)), 
                      color, 2)
        
        cv2.putText(frame, f"{class_name}: Age {int(conf*100)}", (int(x1), int(y1) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
                   )
    return frame

# Function to log results to out.txt
def log_results(week, unhealthy_count, disease_counts):
    with open(result_path, 'w') as f:
        f.write(f"Week {week}: {unhealthy_count} unhealthy areas\n")
        for disease, count in disease_counts.items():
            f.write(f"{disease}: {count}\n")

# Function to assign unique identifiers to detected areas
def assign_unique_ids(detected_boxes, tracked_boxes):
    next_id = max(tracked_boxes.keys(), default=0) + 1
    updated_tracked_boxes = {}
    for box in detected_boxes:
        match_found = False
        for tid, (tbox, age) in tracked_boxes.items():
            if iou(box[:4], tbox) > 0.5:  # Using IoU to check for match
                updated_tracked_boxes[tid] = (box[:4], age + 1)
                match_found = True
                break
        if not match_found:
            updated_tracked_boxes[next_id] = (box[:4], 1)
            next_id += 1
    return updated_tracked_boxes

# Function to calculate Intersection over Union (IoU)
def iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_p, y1_p, x2_p, y2_p = box2

    xi1 = max(x1, x1_p)
    yi1 = max(y1, y1_p)
    xi2 = min(x2, x2_p)
    yi2 = min(y2, y2_p)

    inter_area = max(0, xi2 - xi1 + 1) * max(0, yi2 - yi1 + 1)

    box1_area = (x2 - x1 + 1) * (y1 - y1 + 1)
    
    box2_area = (x2_p - x1_p + 1) * (y2_p - y1_p + 1)

    union_area = box1_area + box2_area - inter_area

    iou = inter_area / union_area

    return iou

# Capture video from the webcam or load an image
use_webcam = False  # Set to False to use a local image

# Use webcam
if use_webcam:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    pTime = 0
    tracked_boxes = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        # Estimate the age of the rice field
        current_week = estimate_rice_field_age(frame)

        # Detect rice fields in the frame
        frame, detected_boxes = detect_rice_fields(frame)

        # Draw the detected boxes on the frame
        frame = draw_boxes(frame, detected_boxes)

        # Assign unique IDs to detected areas
        tracked_boxes = assign_unique_ids(detected_boxes, tracked_boxes)

        # Draw tracked boxes and display unique IDs
        unhealthy_count = 0
        disease_counts = {name: 0 for name in class_names.values()}
        for tid, (box, age) in tracked_boxes.items():
            x1, y1, x2, y2 = map(int, box)
            class_name = class_names.get(tid, f"Unhealthy area {tid}")
            if class_name in disease_counts:
                disease_counts[class_name] += 1
            if 'Brown Spot Area' in class_name:
                unhealthy_count += 1

            label = f"{class_name}: Age {age}"
            color = (0, 0, 255) if 'Brown Spot Area' in class_name else (0, 255, 0)
            cv2.rectangle(frame, 
                          (x1, y1), 
                          (x2, y2), 
                          color, 2)
            
            cv2.putText(frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Log results
        log_results(current_week, unhealthy_count, disease_counts)

        # Display the frame with additional information
        cv2.putText(frame, f"Unhealthy areas: {unhealthy_count}", 
                    (10, 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                    (0, 0, 255), 2
                   )
        
        cv2.putText(frame, f"Estimated Age: Week {current_week}", 
                    (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                    (0, 255, 0), 2
                   )
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f"FPS: {fps:.2f}", 
                    (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                    (255, 0, 0), 2)

        cv2.imshow("Rice Field Detection", frame)

        # Save image if an unhealthy area is detected
        if unhealthy_count > 0:
            timestamp = int(time.time())
            result_image_path = os.path.join(result_images_path, 
                                             f"detected_unhealthy_{timestamp}.png")
            
            cv2.imwrite(result_image_path, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Use local image
else:
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: Could not read image.")
        exit()

    current_week = estimate_rice_field_age(frame)
    frame, detected_boxes = detect_rice_fields(frame)
    frame = draw_boxes(frame, detected_boxes)

    unhealthy_count = len([box for box in detected_boxes if 'Brown Spot Area' in box[-1]])
    disease_counts = {name: 0 for name in class_names.values()}
    for _, _, _, _, _, _, class_name in detected_boxes:
        if class_name in disease_counts:
            disease_counts[class_name] += 1

    log_results(current_week, unhealthy_count, disease_counts)

    if unhealthy_count > 0:
        result_image_path = os.path.join(result_images_path, "detected_unhealthy.png")
        cv2.imwrite(result_image_path, frame)

    cv2.putText(frame, 
                f"Unhealthy areas: {unhealthy_count}", 
                (10, 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                (0, 0, 255), 2
               )
    
    cv2.putText(frame, 
                f"Estimated Age: Week {current_week}", 
                (10, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                (0, 255, 0), 2
               )
    
    cv2.imshow("Rice Field Detection", 
               frame
              )
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
