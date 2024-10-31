import cv2
import os
from ultralytics import YOLO
from class_names import class_names

# Define paths
home_directory = os.path.expanduser('~/HarvestVision/')
model_path = os.path.join(home_directory, "Model", "HarvestVision.pt")
image_dir = os.path.join(home_directory, "Source")
result_path = os.path.join(home_directory, 'Result', 'Result.txt')
final_result_path = os.path.join(home_directory, 'Result', 'Tresult.txt')

# Initialize model
model = YOLO(model_path)
total_counts = {}

# Process each image in the directory
for filename in os.listdir(image_dir):
    image_path = os.path.join(image_dir, filename)
    image = cv2.imread(image_path)
    
    # Check if image is loaded properly
    if image is None:
        print(f"Error: Could not open image {image_path}. Skipping...")
        continue
    
    # Run the YOLO model on the image
    results = model(image)
    class_counts = {}
    
    # Count detected classes in the current image
    for result in results:
        for cls in result.boxes.cls:
            cls_name = model.names[int(cls)]
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
    
    # Write detection results for this image to Result.txt
    with open(result_path, "a") as deteksi_txt:
        deteksi_txt.write(f"{filename}: ")
        for cls_name, count in class_counts.items():
            deteksi_txt.write(f"{cls_name}: {count} ")
            # Update total counts across all images
            total_counts[cls_name] = total_counts.get(cls_name, 0) + count
        deteksi_txt.write("\n")

# Write overall counts to Tresult.txt
with open(final_result_path, "w") as final_result_txt:
    for cls_name, total in total_counts.items():
        final_result_txt.write(f"{cls_name}: {total}\n")

print("Detection finished. Results are in Result.txt and Tresult.txt")
