import cv2
import time
from ultralytics import YOLO
import os
from class_names import class_names

home_directory = os.path.expanduser('~/HarvestVision/')
model_path = os.path.join(home_directory, 'Model', 'HarvestVision.pt')
image_path = os.path.join(home_directory, 'Source', '1.jpg')
result_path = os.path.join(home_directory, 'Result', 'Result.txt')
final_result_path = os.path.join(home_directory, 'Result', 'Tresult.txt')

model = YOLO(model_path)
image = cv2.imread(image_path)
if image is None:
    print(f"Error: Could not open image {image_path}.")
    exit()

results = model(image)
class_counts = {}

for result in results:
    for cls in result.boxes.cls:
        cls_name = model.names[int(cls)]
        if cls_name in class_counts:
            class_counts[cls_name] += 1
        else:
            class_counts[cls_name] = 1

#result.txt
with open(result_path, "w") as deteksi_txt:
    deteksi_txt.write("{}: ".format(os.path.basename(image_path)))
    for cls_name, count in class_counts.items():
        deteksi_txt.write("{}: {} ".format(cls_name, count))
    deteksi_txt.write("\n")

#tresult.txt
total_counts = class_counts

with open(final_result_path, "w") as final_result_txt:
    for cls_name, total in total_counts.items():
        final_result_txt.write("{}: {}\n".format(cls_name, total))

print("Detection finished. Results are in Result.txt and Tresult.txt")

