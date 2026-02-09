#!/bin/bash
set -e

# ============================================
# CodeForge - One-liner bootstrap for GCP VM
# ============================================
# Usage (from a fresh GCP VM or Cloud Shell):
#   git clone https://github.com/<user>/codeforge.git && cd codeforge && bash bootstrap.sh
# ============================================

echo "============================================="
echo "  CodeForge - Bootstrap"
echo "============================================="

# Step 1: Check Python
echo ""
echo "Step 1: Checking Python..."
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo "  Python $PY_VERSION found"
else
    echo "  Installing Python 3.11..."
    sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip
fi

# Step 2: Create virtual environment
echo ""
echo "Step 2: Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
echo "  venv activated"

# Step 3: Install dependencies
echo ""
echo "Step 3: Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet google-adk google-cloud-storage pypdf pydantic python-dotenv httpx requests
echo "  Dependencies installed"

# Step 4: Setup .env
echo ""
echo "Step 4: Environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  Created .env from template"
    echo ""
    echo "  >>>  IMPORTANT: Edit .env with your GCP project ID  <<<"
    echo "  >>>  nano .env                                       <<<"
    echo ""
fi

# Step 5: Check gcloud
echo ""
echo "Step 5: Checking gcloud CLI..."
if command -v gcloud &> /dev/null; then
    PROJECT=$(gcloud config get-value project 2>/dev/null)
    echo "  gcloud found (current project: ${PROJECT:-none})"
else
    echo "  gcloud not found. Install: https://cloud.google.com/sdk/docs/install"
fi

echo ""
echo "============================================="
echo "  Bootstrap Complete!"
echo "============================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your GCP project ID:  nano .env"
echo "  2. Authenticate:  gcloud auth application-default login"
echo "  3. Setup GCP:     bash setup_environment.sh"
echo "  4. Validate:      python3 dry_run.py"
echo "  5. Launch:        adk web --port 8080"
echo ""
echo "  (Remember to activate venv: source .venv/bin/activate)"
echo ""
