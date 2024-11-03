import numpy as np
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from path import csv_path, estimate_path

print(csv_path) 
print(estimate_path) 

def adjusted_yield(disease_counts):
    standard_yield = 6.89  # tons per hectare baseline
    total_diseases = sum(disease_counts.values())
    average_diseases = total_diseases / len(disease_counts)
    
    if average_diseases > 1100:
        adjustment_factor = np.clip((1100 / average_diseases), 0.67, 0.83)
        adjusted_yield = standard_yield * adjustment_factor
        return max(adjusted_yield, 4)
    return standard_yield

try:
    disease_counts = {}
    with open(csv_path, 'r') as file:
        for line in file:
            if ':' in line:
                disease, count = line.strip().split(':')
                disease_counts[disease.strip()] = int(count.strip())
    
    final_yield = adjusted_yield(disease_counts)
    
    with open(estimate_path, 'w') as file:
        file.write(f"Prediksi Hasil Panen (tons/ha): {final_yield:.2f}")
    
    print(f"Estimasi direkam ke {estimate_path}")

except FileNotFoundError:
    print("Tresult.txt not found. Please ensure the file exists in the specified path.")
except ValueError as ve:
    print(f"Data parsing error: {ve}")
except Exception as e:
    print(f"An error occurred: {e}")
