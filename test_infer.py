from inference.pipeline import run_inference
from pathlib import Path

ds_path = Path("webapp/tmp_ds/CantusSVSTest.ds")
output_dir = Path("webapp/output")
title = "CantusSVSTest"

wav_path = run_inference(ds_path, output_dir, title)
print(wav_path)
