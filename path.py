import os

home_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(home_dir, 'result', 'Tresult.txt')
estimate_path = os.path.join(home_dir, 'estimate', 'estimate.txt')
model_path = os.path.join(home_dir, 'Model', 'HarvestVision.pt')
image_dir = os.path.join(home_dir, 'Source')
result_path = os.path.join(home_dir, 'result', 'Result.txt')
final_result_path = os.path.join(home_dir, 'result', 'Tresult.txt')
image_path = os.path.join(home_dir, 'Source')
image_out = os.path.join(home_dir, 'result')
