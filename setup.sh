#!/usr/bin/env bash
# setup.sh – Create a virtualenv and install project dependencies.
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh

set -euo pipefail

VENV_DIR=".venv"

echo "=== fluent-critic setup ==="

# Ensure python3 is available
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 not found. Please install Python 3." >&2
  exit 1
fi

# Install virtualenv if not already available
if ! python3 -m virtualenv --version &>/dev/null 2>&1; then
  echo "Installing virtualenv…"
  pip3 install --quiet virtualenv
fi

# Create the virtual environment
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in ${VENV_DIR}…"
  python3 -m virtualenv "$VENV_DIR"
else
  echo "Virtual environment already exists at ${VENV_DIR}, skipping creation."
fi

# Activate and install dependencies
echo "Installing dependencies from requirements.txt…"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
pip install --quiet -r requirements.txt

echo ""
echo "Setup complete. To run the bot:"
echo "  source ${VENV_DIR}/bin/activate"
echo "  cp .env.example .env   # then add your OPENAI_API_KEY"
echo "  python src/main.py"
