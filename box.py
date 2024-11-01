import os
import time
from ultralytics import YOLO
from path import model_path, model_path, image_path, image_out

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
