from pathlib import Path

home_dir = Path('~/HarvestVision')
model_path = home_dir / 'Model' / "HarvestVision.pt"
image_dir = home_dir / 'Source'
result_path = home_dir / 'result' / 'Result.txt'
final_result_path = home_dir / 'result' / 'Tresult.txt'
csv_path = home_dir / "result" / "Tresult.txt"
estimate_path = home_dir / "result" / "estimate.txt"
image_path = home_dir / 'Source'
image_out = home_dir / "result"

# model_path, model_path, image_dir, result_path, final_result_path, csv_path, estimate_path, image_path, image_out