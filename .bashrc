# Warn if Arrow is not loaded
if ! module list 2>&1 | grep -q arrow; then
  echo -e "\n\033[1;33m[WARNING]\033[0m Arrow module is not loaded! Run: module load arrow/19.0.1"
fi

# Warn if GCC is not loaded
if ! module list 2>&1 | grep -q gcc; then
  echo -e "\n\033[1;33m[WARNING]\033[0m GCC module is not loaded! Run: module load gcc/12.3"
fi
