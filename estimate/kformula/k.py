import os
import sys
kformula = os.path.dirname(os.path.abspath(__file__))
HarvestVision = os.path.join(kformula, "..", '..')
sys.path.append(HarvestVision)

K_min = 0.534513309 # kelipatan minimum dari K.csv
K_max = 1.718665871 # kelipatan maximum dari K.csv
P_min = 6.7
P_max = 8.2

a = (P_max - P_min) / (K_max - K_min)
b = P_min - a * K_min

a, b
print(a, b)
# Harvest = 1.2667286700512153 × K + 6.022916666965756
# Harvest = a × K + b