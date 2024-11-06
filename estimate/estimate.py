import numpy as np
import os
import sys
import importlib.util
import matplotlib.pyplot as plt
import csv

estimate_dir = os.path.dirname(os.path.abspath(__file__))
HarvestVision = os.path.join(estimate_dir, '..')
sys.path.append(HarvestVision)

from path import csv_path, estimate_path, kformula, kmonth

spec = importlib.util.spec_from_file_location("k", kformula)
k_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k_module)

a = k_module.a
b = k_module.b

def get_all_k_values():
    k_values = {}
    with open(kmonth, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            month = row["Months"].strip().capitalize()
            k_values[month] = float(row["K"])
    return k_values

def adjusted_yield(disease_counts, a, b, K):
    total_diseases = sum(disease_counts.values())
    average_diseases = total_diseases / len(disease_counts)
    
    yield_estimate = a * K + b
    
    if average_diseases > 1100:
        adjustment_factor = np.clip((1100 / average_diseases), 0.67, 0.83)
        yield_estimate *= adjustment_factor
    
    return max(yield_estimate, 4)

try:
    disease_counts = {}
    with open(csv_path, 'r') as file:
        for line in file:
            if ':' in line:
                disease, count = line.strip().split(':')
                disease_counts[disease.strip()] = int(count.strip())
    
    k_values = get_all_k_values()

    monthly_yields = {}
    for month, K in k_values.items():
        monthly_yields[month] = adjusted_yield(disease_counts, a, b, K)

    with open(estimate_path, 'w') as file:
        for month, yield_value in monthly_yields.items():
            file.write(f"{month} (tons/ha): {yield_value:.2f}\n")
    
    print(f"Estimasi untuk 12 bulan direkam ke {estimate_path}")

except Exception as e:
    print(f"An error occurred: {e}")

months = list(monthly_yields.keys())
yield_values = list(monthly_yields.values())

# # border color
# plt.figure(figsize=(10, 6), facecolor="white")
# # plot color
# plt.gca().set_facecolor("lightgreen")

stylesheets = ['dark_background'] #Solarize_Light2 also good. 
for style in stylesheets:
    plt.style.use(style)
    plt.plot(months, yield_values, marker='o', markerfacecolor='lightgreen', color='lightyellow', linestyle='-')
    plt.title("Crop yield predictions (tons/ha) per month")
    plt.xlabel("Month")
    plt.ylabel("tons/ha")
    plt.xticks(rotation=45)
    plt.grid(color = 'gray', linestyle = 'dotted', linewidth = 1)
    plt.tight_layout()
    plt.show()