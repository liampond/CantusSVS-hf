# inference/pipeline.py

import os
import json
import sys
from pathlib import Path
from typing import Optional

from utils.hparams import set_hparams, hparams
from inference.ds_variance import DiffSingerVarianceInfer
from inference.ds_acoustic import DiffSingerAcousticInfer
from utils.infer_utils import parse_commandline_spk_mix, trans_key
from webapp.services.parsing.ds_validator import validate_ds

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HF_CHECKPOINTS_DIR = "/tmp/cantussvs_v1/checkpoints"


def run_inference(
    ds_path: Path,
    output_dir: Path,
    title: str,
    *,
    variance_exp: str = "regular_variance_v1",
    acoustic_exp: str = "debug_test",
    seed: int = 42,
    num_runs: int = 1,
    key_shift: int = 0,
    gender: Optional[float] = None
) -> Path:
    """
    Runs the full pipeline: variance model => acoustic model;
    returns the path to the generated WAV.
    """

    sys.argv = [
        "", 
        "--config", str(PROJECT_ROOT / "checkpoints" / variance_exp / "config.yaml"), 
        "--exp_name", variance_exp, 
        "--infer"
    ]
    set_hparams(print_hparams=False)

    # 1) Check input DS exists
    if not ds_path.exists():
        raise FileNotFoundError(f"Input DS file not found: {ds_path}")

    # 2) Load DS params
    with open(ds_path, "r", encoding="utf-8") as f:
        params = json.load(f)
    if not isinstance(params, list):
        params = [params]

    # Validate loaded DS files
    for p in params:
        try:
            validate_ds(p)
        except Exception as e:
            raise ValueError(f"Invalid input DS file: {e}")

    # Ensure ph_seq present
    for p in params:
        if "ph_seq" not in p:
            text = p.get("text", "")
            p["ph_seq"] = " ".join(list(text.replace(" ", "")))

    # Transpose
    if key_shift != 0:
        params = trans_key(params, key_shift)

    # Speaker mix
    spk_mix = parse_commandline_spk_mix(None) if hparams.get("use_spk_id") else None
    for p in params:
        if gender is not None and hparams.get("use_key_shift_embed"):
            p["gender"] = gender
        if spk_mix is not None:
            p["spk_mix"] = spk_mix

    # ==== Variance Inference ==== #
    print(f"[pipeline] Loading variance exp: {variance_exp}")
    variance_config_path = os.path.join(HF_CHECKPOINTS_DIR, variance_exp, "config.yaml")

    sys.argv = [
        "", 
        "--config", variance_config_path,
        "--exp_name", variance_exp,
        "--infer"
    ]
    set_hparams(print_hparams=False)

    print("[pipeline] Variance hparams keys:", sorted(hparams.keys()))

    var_infer = DiffSingerVarianceInfer(ckpt_steps=None, predictions={"dur", "pitch"})
    ds_out = output_dir / f"{title}.ds"
    var_infer.run_inference(params, out_dir=output_dir, title=title, num_runs=1, seed=seed)
    if not ds_out.exists():
        raise RuntimeError(f"Variance inference failed; missing {ds_out}")

    # Reload params from variance output
    with open(ds_out, "r", encoding="utf-8") as f:
        params = json.load(f)
    if not isinstance(params, list):
        params = [params]

    # Validate variance output DS
    for p in params:
        try:
            validate_ds(p)
        except Exception as e:
            raise ValueError(f"Invalid DS after variance inference: {e}")

    # ==== Acoustic Inference ==== #
    print(f"[pipeline] Loading acoustic exp: {acoustic_exp}")
    acoustic_config_path = os.path.join(HF_CHECKPOINTS_DIR, acoustic_exp, "config.yaml")

    sys.argv = [
        "", 
        "--config", acoustic_config_path,
        "--exp_name", acoustic_exp,
        "--infer"
    ]
    set_hparams(print_hparams=False)
    print("[pipeline] Acoustic hparams keys:", sorted(hparams.keys()))

    ac_infer = DiffSingerAcousticInfer(load_vocoder=True, ckpt_steps=None)
    ac_infer.run_inference(params, out_dir=output_dir, title=title, num_runs=num_runs, seed=seed)

    wav_out = output_dir / f"{title}.wav"
    if not wav_out.exists():
        raise RuntimeError(f"Acoustic inference failed; missing {wav_out}")

    return wav_out

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run full DiffSinger inference pipeline")
    parser.add_argument("ds_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--title", type=str, default=None)
    parser.add_argument("--variance_exp", type=str, default="regular_variance_v1")
    parser.add_argument("--acoustic_exp", type=str, default="debug_test")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_runs", type=int, default=1)
    parser.add_argument("--key_shift", type=int, default=0)
    parser.add_argument("--gender", type=float, default=None)

    args = parser.parse_args()
    title = args.title or args.ds_path.stem

    run_inference(
        ds_path=args.ds_path,
        output_dir=args.output_dir,
        title=title,
        variance_exp=args.variance_exp,
        acoustic_exp=args.acoustic_exp,
        seed=args.seed,
        num_runs=args.num_runs,
        key_shift=args.key_shift,
        gender=args.gender,
    )
