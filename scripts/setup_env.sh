# Activate the virtual environment
source venv/bin/activate

# Load necessary modules only if not already loaded
if ! module list 2>&1 | grep -q gcc; then
  module load gcc/12.3
fi

if ! module list 2>&1 | grep -q arrow; then
  module load gcc arrow/19.0.1 python/3.11
fi

if ! module list 2>&1 | grep -q cuda; then
  module load cuda
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3.11 -m venv venv
else
  echo "Virtual environment already exists, skipping creation."
fi

# Verify if virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
  echo "❗ Error: Virtual environment is not active after activation attempt."
  echo "Exiting to avoid broken installations."
  exit 1
fi

# Upgrade pip
pip install --upgrade pip

# Install PyTorch manually first (important for compatibility)
pip install --no-index torch torchvision torchaudio
pip install streamlit tornado pytest lxml pyyaml lightning

module load scipy-stack

# Check if torch and torchvision are installed correctly
TORCH_VERSION=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "")
VISION_VERSION=$(python -c "import torchvision; print(torchvision.__version__)" 2>/dev/null || echo "")

if [ -z "$TORCH_VERSION" ] || [ -z "$VISION_VERSION" ]; then
  echo "❗ Error: torch or torchvision not installed correctly."
  exit 1
fi

echo "✅ torch version: $TORCH_VERSION"
echo "✅ torchvision version: $VISION_VERSION"

# Install remaining project dependencies unless in dev mode
if [ "$dev" != "1" ]; then
  source venv/bin/activate
  echo "Installing project requirements..."
  pip install -r requirements.txt
  pip install tornado scipy pillow pandas six packaging==24.0 decorator
else
  echo "⚡ Dev mode active: Skipping pip install -r requirements.txt"
fi

# Final success message
echo "🎉 Environment setup complete! Ready to go."
