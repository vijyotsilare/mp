# Setup environment with Python 3.10
# Note: Ensure Python 3.10 is installed on your system.

# Upgrade pip to latest version
python -m pip install --upgrade pip

# 1. Force binary install of tokenizers to prevent Rust / MSVC build failure
#    This happens because precompiled wheels for tokenizers don't exist for
#    newer/unsupported Python versions like 3.13. Using Python 3.10 and
#    forcing --only-binary prevents from compiling from source.
python -m pip install tokenizers==0.15.0 --only-binary tokenizers

# 2. Install Stable PyTorch (2.1.2)
python -m pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu121

# 3. Enforce the exact dependency stack requested
python -m pip install transformers==4.36.2 datasets==2.16.1 accelerate==0.26.1 peft==0.7.1 trl==0.7.10 "numpy<2"
