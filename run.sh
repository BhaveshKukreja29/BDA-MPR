#!/bin/bash
# Run the full BDA MPR pipeline
# Usage: bash run.sh

set -e
cd "$(dirname "$0")"

echo "=========================================="
echo " BDA MPR - Twitter Hashtags Analysis"
echo "=========================================="

# Step 1: Preprocess
echo ""
echo ">>> Step 1: Preprocessing tweets.csv..."
python3 scripts/preprocess.py

# Step 2: Analysis + Visualizations
echo ""
echo ">>> Step 2: FM Algorithm + Visualizations..."
python3 scripts/analysis.py

# Step 3: Generate Report
echo ""
echo ">>> Step 3: Generating output.md..."
python3 scripts/generate_report.py

echo ""
echo "=========================================="
echo " ALL DONE! Open output.md for the report."
echo "=========================================="
