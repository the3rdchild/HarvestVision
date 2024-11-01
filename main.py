import cv2
import os
from ultralytics import YOLO
from path import model_path, image_dir, result_path, final_result_path, image_path

model = YOLO(model_path)
conf_thres = 0.5
total_counts = {}
for filename in os.listdir(image_dir):
    image_path = os.path.join(image_dir, filename)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not open image {image_path}. Skipping...")
        continue
    results = model(image, conf=conf_thres) #detect
    class_counts = {}
    for result in results:
        for cls in result.boxes.cls:
            cls_name = model.names[int(cls)]
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
    with open(result_path, "a") as deteksi_txt:
        deteksi_txt.write(f"{filename}: ")
        for cls_name, count in class_counts.items():
            deteksi_txt.write(f"{cls_name}: {count} ")
            total_counts[cls_name] = total_counts.get(cls_name, 0) + count
        deteksi_txt.write("\n")
with open(final_result_path, "w") as final_result_txt:
    for cls_name, total in total_counts.items():
        final_result_txt.write(f"{cls_name}: {total}\n")

print("Detection finished. Results are in Result.txt and Tresult.txt")
