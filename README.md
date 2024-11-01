## <div align="center">HarvestVision</div>

<div align="center">
<a href="https://github.com/the3rdchild/HarvestVision/">HarvestVision</a> is an innovative project focused on leveraging computer vision and AI to analyze crop conditions, yield predictions, and plant health in real time. By utilizing machine learning algorithms and drone imagery, this project aims to empower farmers and agricultural professionals with actionable insights for optimizing harvests and managing crops more effectively.
It is part of Project of <a href="[https://github.com/the3rdchild/HarvestVision/](https://php2d.kemdikbud.go.id/)">PPK Ormawa</a>: SMART FARMING: "PENINGKATAN EFEKTIVITAS PERTANIAN DESA KUDANGWANGI DENGAN PENGAPLIKASIAN SEMI AUTONOMOUS DRONE UNTUK  ENYEMPROTAN PESTISIDA SERTA PEMANFAATAN APLIKASI INTEGRASI PADA TANAMAN PADI" (Enhancing Agricultural Effectiveness in Kudangwangi Village through the Application of Semi-Autonomous Drones for Pesticide Spraying and Utilization of Integrated Applications on Rice Crops)
</div>

Key Features
- Real-Time Crop Monitoring: Automatically detects plant health and growth patterns.
- Yield Prediction: Provides estimates on potential harvest yield based on crop condition data.
- Scalable Technology: Suitable for diverse agricultural setups, from small farms to large-scale plantations.
This repository includes all essential files, code, and documentation to help you get started or contribute to Harvest Vision. Your contributions and feedback are always welcome!

## <div align="center">Documentation</div>

This code is using pyhton with minimum requarement is [**Python>=3.8**](https://www.python.org/). Download [HarvestVision](https://github.com/the3rdchild/HarvestVision) using
```Git
git clone https://github.com/the3rdchild/HarvestVision/
```

## Linux
Use [run.sh](https://github.com/the3rdchild/rgd/blob/main/run.sh) to run the program. this bash file contain simpel program to run all the python file:
```
#!/bin/bash
path="~/HarvestVision/"
cd $path || exit
python3 main.py &
python3 box.py &
python3 estimate.py &
wait
```

## YoloV8 Model

the defaul model of yolo is yolov8 located in the [model](https://github.com/the3rdchild/HarvestVision/tree/main/Model) folder with default name:
```
HarvestVision.pt
```
you can also train your own model or change it to latest model of yolo such yolo11 also change the class to your own data class(es) in [class_names](https://github.com/the3rdchild/HarvestVision/blob/main/class_names.py):
```
class_names = {
    "Your": 0,
    "Own": 0,
    "Class": 0
}
```
