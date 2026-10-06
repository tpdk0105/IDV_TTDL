"""
Module: src/02_eda.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2005–2024)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Thực hiện phân tích khám phá dữ liệu ban đầu (EDA) trên các tập dữ liệu thô trong `data/raw/`.
    - Sử dụng các thư viện biểu đồ tĩnh (Matplotlib, Seaborn) vẽ tối thiểu 3 - 5 biểu đồ tĩnh theo đúng barem IDV:
        1. Phân phối biến định lượng (Histogram / KDE: burned_area_ha, damage_usd).
        2. Biểu đồ hộp phát hiện ngoại lai sơ bộ (Boxplot: deaths, affected).
        3. Bản đồ nhiệt tương quan đa biến (Correlation Heatmap: Pearson / Spearman).
        4. Ma trận dữ liệu khuyết thiếu (Missing values bar/matrix).
        5. Xu hướng tần suất thảm họa theo thời gian (Line plot / Countplot).
    - Xuất các biểu đồ tĩnh sang thư mục `reports/figures/` và lập báo cáo `docs/DATA_QUALITY_REPORT.md`.

Trạng thái: Khung mã nguồn & Đặc tả chi tiết (Giai đoạn 1) - Tích hợp thực thi trong Giai đoạn 2.
"""

import sys
from pathlib import Path

# Đảm bảo UTF-8 stream trên Windows console
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
import seaborn as sns


def plot_missing_values(df=None, output_path: Path = Path("reports/figures/eda_01_missing_values.png")) -> None:
    """Ve bieu do phan tich ty le khuyet thieu cua cac cot du lieu bang Seaborn/Matplotlib."""
    print(f"[TODO - TV1] Ve va luu bieu do khuyet thieu -> {output_path}")


def plot_distributions(df=None, output_path: Path = Path("reports/figures/eda_02_distributions.png")) -> None:
    """Ve bieu do phan phoi Histogram/KDE cho cac bien lien tuc (dien tich chay, thiet hai USD)."""
    print(f"[TODO - TV1] Ve va luu bieu do phan phoi bien dinh luong -> {output_path}")


def plot_outlier_boxplots(df=None, output_path: Path = Path("reports/figures/eda_03_outliers_boxplot.png")) -> None:
    """Ve bieu do hop (Boxplot) phat hien ngoai lai cho so nguoi chet, so nguoi anh huong."""
    print(f"[TODO - TV1] Ve va luu Boxplot phat hien ngoai lai so bo -> {output_path}")


def plot_correlation_heatmap(df=None, output_path: Path = Path("reports/figures/eda_04_correlation_heatmap.png")) -> None:
    """Ve Correlation Heatmap bang Seaborn the hien moi tuong quan giua cac bien so."""
    print(f"[TODO - TV1] Ve va luu Correlation Heatmap -> {output_path}")


def plot_temporal_trends(df=None, output_path: Path = Path("reports/figures/eda_05_temporal_trend.png")) -> None:
    """Ve xu huong tan suat tham hoa va chay rung qua cac nam (2006-2025)."""
    print(f"[TODO - TV1] Ve va luu bieu do xu huong thoi gian so bo -> {output_path}")


def run_initial_eda() -> None:
    """Ham dieu phoi toan bo luong EDA du lieu tho va xuat bao cao chat luong."""
    raw_dir = Path("data/raw")
    figures_dir = Path("reports/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"[TV1 - EDA] Bat dau kham pha du lieu tho tu: {raw_dir.resolve()}")
    print("[TV1 - EDA] Khoi tao cac bieu do tinh (Matplotlib, Seaborn) theo barem do an IDV (3-5 bieu do)...")

    # Goi cac ham ve bieu do tinh (3 - 5 bieu do theo barem do an)
    plot_missing_values(output_path=figures_dir / "eda_01_missing_values.png")
    plot_distributions(output_path=figures_dir / "eda_02_distributions.png")
    plot_outlier_boxplots(output_path=figures_dir / "eda_03_outliers_boxplot.png")
    plot_correlation_heatmap(output_path=figures_dir / "eda_04_correlation_heatmap.png")
    plot_temporal_trends(output_path=figures_dir / "eda_05_temporal_trend.png")

    print("[TV1 - EDA] Hoan thanh phan tich kham pha du lieu. Xuat bao cao sang docs/DATA_QUALITY_REPORT.md.")


if __name__ == "__main__":
    run_initial_eda()

