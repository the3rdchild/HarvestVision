import os

HarvestVision = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(HarvestVision, 'Result', 'Tresult.txt')
estimate_path = os.path.join(HarvestVision, 'Estimate', 'Estimate.txt')
model_path = os.path.join(HarvestVision, 'Model', 'HarvestVision.pt')
image_dir = os.path.join(HarvestVision, 'Source')
result_path = os.path.join(HarvestVision, 'Result', 'Result.txt')
final_result_path = os.path.join(HarvestVision, 'Result', 'Tresult.txt')
image_path = os.path.join(HarvestVision, 'Source')
image_out = os.path.join(HarvestVision, 'Result')
