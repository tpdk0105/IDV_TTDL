# ==============================================================================
# Pipeline Execution Script for Windows PowerShell
# Project: Global Wildfire & Natural Disasters (2005-2024)
# Sequence: 01_download -> 02_eda -> 03_clean -> 03b_ml_clean ->
#           04_split_tables -> 05_build_db -> 06_export_json -> 07_validate
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " STARTING DATA PIPELINE: IDV_TTDL (2005-2024)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$steps = @(
    @{ Name = "Step 1: Download Raw Data"; Script = "src/01_download.py" },
    @{ Name = "Step 2: Initial EDA & Quality Report"; Script = "src/02_eda.py" },
    @{ Name = "Step 3: Rule-based Data Cleaning"; Script = "src/03_clean.py" },
    @{ Name = "Step 3b: Machine Learning Cleaning"; Script = "src/03b_ml_clean.py" },
    @{ Name = "Step 4: Star Schema Table Splitting"; Script = "src/04_split_tables.py" },
    @{ Name = "Step 5: Database Build & Integrity Checks"; Script = "src/05_build_db.py" },
    @{ Name = "Step 6: Export Dashboard JSON Data"; Script = "src/06_export_json.py" },
    @{ Name = "Step 7: Automated Validation & Assertions"; Script = "src/07_validate.py" }
)

foreach ($step in $steps) {
    Write-Host "`n>>> Running $($step.Name)..." -ForegroundColor Yellow
    python $step.Script
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n[ERROR] $($step.Name) failed with exit code $LASTEXITCODE. Pipeline halted!" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "[OK] $($step.Name) completed successfully." -ForegroundColor Green
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " PIPELINE EXECUTED SUCCESSFULLY!" -ForegroundColor Cyan
Write-Host " Run 'npm run start' to preview the interactive dashboard." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
