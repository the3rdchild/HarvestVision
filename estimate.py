import pandas as pd
import numpy as np
import time
import os

home_directory = os.path.expanduser("~/HarvestVision")
csv_path = os.path.join(home_directory, "result", "Tresult.txt")

data_path = csv_path

def adjusted_yield(disease_counts):
    standard_yield = 6.0
    total_diseases = sum(disease_counts.values())
    average_diseases = total_diseases / len(disease_counts)
    
    if average_diseases > 1100:
        adjustment_factor = np.clip((1100 / average_diseases), 0.67, 0.83)
        adjusted_yield = standard_yield * adjustment_factor
        return max(adjusted_yield, 4)
    return standard_yield

last_mod_time = os.path.getmtime(data_path)

while True:
    current_mod_time = os.path.getmtime(data_path)
    
    if current_mod_time > last_mod_time: #check updated data
        last_mod_time = current_mod_time
        print("Data updated, processing...")

        new_data_df = pd.read_csv(data_path)
        disease_counts = new_data_df.iloc[0].to_dict()

        final_yield = adjusted_yield(disease_counts)
        print(f"Predicted Adjusted Yield (tons/ha): {final_yield:.2f}")
    else:
        time_elapsed = time.time() - last_mod_time
        if time_elapsed > 300:  #terminate 300 seconds 
            print("No updates detected in the last 5 minutes. Exiting.")
            break

    time.sleep(60)
