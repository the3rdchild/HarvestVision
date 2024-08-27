#!/bin/bash

path="~/HarvestVision/"
cd $path || exit

python3 main.py &
python3 box.py &
python3 estimate.py &

wait
