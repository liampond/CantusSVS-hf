#!/bin/bash

# ========== CONFIGURATION ==========

INPUT_DS=$1
OUTPUT_DIR=$2
TITLE=$(basename "$INPUT_DS" .ds)

# Inference configuration
VARIANCE_EXP="regular_variance_v1"
ACOUSTIC_EXP="debug_test"
ACOUSTIC_CKPT=""       # Set this to e.g., 50000 to specify a checkpoint
DIFFUSION_STEPS=100    # Set to desired number of diffusion steps
SEED=42
NUM_RUNS=1
MEL_ONLY=false         # Set to true to save only mel spectrograms, not waveform

# ========== CHECK INPUTS ==========

if [ -z "$INPUT_DS" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "Usage: ./inference.sh path/to/input.ds path/to/output_dir"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ========== LOGGING SETUP ==========

LOG="$OUTPUT_DIR/${TITLE}_inference.log"
exec > >(tee -a "$LOG") 2>&1

echo ">>> Starting inference for: $INPUT_DS"
echo ">>> Logging to: $LOG"

# ========== STEP 0: VOCODER CHECK (dynamic) ==========

if [ "$MEL_ONLY" = false ]; then
  # Find the highest-step vocoder checkpoint in the acoustic experiment folder
  EXTRACT_ROOT="/tmp/cantussvs_v1"
  VOCODER_PATH=$(find "$EXTRACT_ROOT/checkpoints/$ACOUSTIC_EXP" -maxdepth 1 -type f -name 'model_ckpt_steps_*.ckpt' | sort -V | tail -n 1)

  if [ -z "$VOCODER_PATH" ]; then
    echo "❌ No vocoder checkpoint found in $EXTRACT_ROOT/checkpoints/$ACOUSTIC_EXP/"
    echo "   You can disable waveform synthesis by setting MEL_ONLY=true in the script."
    exit 1
  else
    echo ">>> Using vocoder checkpoint: $VOCODER_PATH"
  fi
fi

# ========== STEP 1: VARIANCE INFERENCE ==========

echo ">>> Step 1: Running variance model inference..."
python scripts/infer.py variance "$INPUT_DS" \
  --exp "$VARIANCE_EXP" \
  --predict dur --predict pitch \
  --out "$OUTPUT_DIR" \
  --title "$TITLE" \
  --seed "$SEED"

VARIANCE_EXIT_CODE=$?
COMPLETED_DS="$OUTPUT_DIR/${TITLE}.ds"

if [ $VARIANCE_EXIT_CODE -ne 0 ] || [ ! -f "$COMPLETED_DS" ]; then
  echo "❌ Variance inference failed or output DS file was not created."
  exit 1
fi

# ========== STEP 2: ACOUSTIC INFERENCE ==========

echo ">>> Step 2: Running acoustic model inference..."

ACOUSTIC_ARGS=(
  python scripts/infer.py acoustic "$COMPLETED_DS"
  --exp "$ACOUSTIC_EXP"
  --out "$OUTPUT_DIR"
  --title "$TITLE"
  --seed "$SEED"
  --num "$NUM_RUNS"
  --steps "$DIFFUSION_STEPS"
)

if [ -n "$ACOUSTIC_CKPT" ]; then
  ACOUSTIC_ARGS+=(--ckpt "$ACOUSTIC_CKPT")
fi

if [ "$MEL_ONLY" = true ]; then
  ACOUSTIC_ARGS+=(--mel)
fi

"${ACOUSTIC_ARGS[@]}"
ACOUSTIC_EXIT_CODE=$?

# Check output WAV file (only if not mel-only)
if [ "$MEL_ONLY" = false ]; then
  OUTPUT_WAV="$OUTPUT_DIR/${TITLE}.wav"
  if [ $ACOUSTIC_EXIT_CODE -ne 0 ] || [ ! -f "$OUTPUT_WAV" ]; then
    echo "❌ Acoustic inference failed or output WAV file not created."
    exit 1
  fi
  echo "✅ Done! Output saved to: $OUTPUT_WAV"
else
  echo "✅ Done! Mel-spectrogram(s) saved to: $OUTPUT_DIR"
fi
