#!/usr/bin/env bash
# ==============================================================================
# Pipeline Execution Script for Linux / macOS Bash
# Project: Global Wildfire & Natural Disasters (2006-2025)
# Sequence: 01_download -> 02_eda -> 03_clean -> 08_predictive_model ->
#           04_split_tables -> 05_build_db -> 06_export_json -> 07_validate
# ==============================================================================

set -e

echo "=========================================================="
echo " STARTING DATA PIPELINE: IDV_TTDL (2006-2025)"
echo "=========================================================="

echo -e "\n>>> Running Step 1: Download Raw Data..."
python src/01_download.py

echo -e "\n>>> Running Step 2: Initial EDA & Quality Report..."
python src/02_eda.py

echo -e "\n>>> Running Step 3: Rule-based Data Cleaning..."
python src/03_clean.py


echo -e "\n>>> Running Step 8: Linear Regression Forecast 2026-2035..."
python src/08_predictive_model.py

echo -e "\n>>> Running Step 4: Star Schema Table Splitting..."
python src/04_split_tables.py

echo -e "\n>>> Running Step 5: Automated Validation & Assertions..."
python src/07_validate.py

echo "=========================================================="
echo " PIPELINE EXECUTED SUCCESSFULLY!"
echo " Run 'npm run start' to preview the interactive dashboard."
echo "=========================================================="
