### HarvestVision
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
