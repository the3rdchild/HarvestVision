import os
import time
from ultralytics import YOLO

home_directory = os.path.expanduser('D:/Download/perkuliahan/yolo/HarvestVision/github/HarvestVision/')
# home_directory = os.path.expanduser('~/HarvestVision/')
# image_path = os.path.join(home_directory, "Source")
image_path = "D:/Download/perkuliahan/yolo/HarvestVision/github/validation"
image_out = os.path.join(home_directory, "Result")
# model_path = os.path.join(home_directory, 'Model', 'HarvestVision.pt')
model_path = "D:/Download/perkuliahan/yolo/HarvestVision/HarvestVision-m.pt"

model = YOLO(model_path)
processed_images = set()

while True:
    images = [f for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    for image in images:
        if image not in processed_images:
            image_file = os.path.join(image_path, image)

            model(image_file, 
                  save=True, 
                  save_crop=False, 
                  project=image_out, 
                  name="images", 
                  exist_ok=True)

            processed_images.add(image)
            print(f"Processed {image}")

    time.sleep(10) #wait for the next image updated
