#!/bin/bash
#SBATCH --account=def-ichiro
#SBATCH --gpus-per-node=1
#SBATCH --mem=125G
#SBATCH --cpus-per-task=8
#SBATCH --time=20:00:00
#SBATCH --output=variance_training_%j.out

module load cuda/12.2 python/3.11
source ~/env-py311/bin/activate
export PYTHONPATH=$(pwd):$(pwd)/basics:$(pwd)/training:$PYTHONPATH

echo "GPU Check:"
nvidia-smi

python scripts/train.py \
  --config=configs/CantusSVS_variance.yaml \
  --exp_name=regular_variance_v1 \
  --pl_trainer.accelerator=gpu \
  --pl_trainer.devices=1 \
  --pl_trainer.precision=16-mixed
