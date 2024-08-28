## <div align="center">HarvestVision</div>

Part of Project of [PPK Ormawa](https://php2d.kemdikbud.go.id/): SMART FARMING: "PENINGKATAN EFEKTIVITAS PERTANIAN DESA KUDANGWANGI DENGAN PENGAPLIKASIAN SEMI AUTONOMOUS DRONE UNTUK  ENYEMPROTAN PESTISIDA SERTA PEMANFAATAN APLIKASI INTEGRASI PADA TANAMAN PADI" (Enhancing Agricultural Effectiveness in Kudangwangi Village through the Application of Semi-Autonomous Drones for Pesticide Spraying and Utilization of Integrated Applications on Rice Crops)

[HarvestVision](https://github.com/the3rdchild/HarvestVision) is an artificial intelligent program that can detetct paddy disease from image captured from the drone and estimate the harvest of paddy using machine learning by counting the distribution of the disease per one hectare.

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

## <div align="center">YoloV8 Model</div>

the defaul model of yolo is yolov8 located in the [model](https://github.com/the3rdchild/HarvestVision/tree/main/Model) folder with default name:
```
HarvestVision.pt
```
you can also train your own model and change the class to your data class(es) in [class_names](https://github.com/the3rdchild/HarvestVision/blob/main/class_names.py) line 27:
```
class_names = {
    "Brown Spot Disease": 0,
    "Dirty Panicle Disease": 0,
    "Groundnut_Late_leaf_spot": 0,
    "Groundnut_Rust": 0,
    "Narrow Brown Spot Disease": 0,
    "Rice Blast Disease": 0,
    "Rice-Blast-Disease": 0,
    "Rice_Bacterial_Blight": 0,
    "Rice_Brown_spot": 0,
    "Tomato_Botrytis": 0,
    "Tomato_Early_Blight": 0,
    "Wheat_Loose_mut": 0,
    "Wheat_Steam_rust": 0,
    "bercak_coklat": 0,
    "blas": 0,
    "brown_spot_disease": 0,
    "dirty_panicle_disease": 0,
    "early stage": 0,
    "harvesting stage": 0,
    "hawar_daun_bakteri": 0,
    "mid age": 0,
    "mid satge": 0,
    "mid stage": 0,
    "narrow_brown_spot_disease": 0,
    "rice": 0,
    "rice_blast_disease": 0,
    "tungro": 0,
    "Brown Spot Area": 0
}
```