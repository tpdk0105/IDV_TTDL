"""
Module: src/03b_ml_clean.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Làm sạch dữ liệu Bước 2 bằng TỐI THIỂU 2 MÔ HÌNH HỌC MÁY (Machine Learning):
        1. Isolation Forest (kết hợp Local Outlier Factor): Phát hiện ngoại lai trên các biến log1p.
           Gắn cờ is_outlier_ml và tính outlier_score.
        2. KNN Imputer hoặc Iterative Imputer (MICE): Điền dữ liệu thiếu cho các biến số,
           gắn cờ <tên_cột>_is_imputed. Đánh giá sai số MAE/RMSE so với Median Baseline.
        3. (Khuyến khích) Random Forest Classifier: Dự đoán cause_group khi P >= 0.7,
           gắn cờ cause_is_predicted.
    - YÊU CẦU CỨNG: assert len(df) >= 5000 ở cuối script.
    - Xuất tập dữ liệu đích: `data/clean/master_clean.csv`.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 2.
"""

import sys
from pathlib import Path


def clean_by_machine_learning() -> None:
    """Áp dụng mô hình ML làm sạch và điền thiếu, xuất master_clean.csv."""
    clean_dir = Path("data/clean")
    clean_dir.mkdir(parents=True, exist_ok=True)
    out_path = clean_dir / "master_clean.csv"

    print("[TODO - TV1] Bắt đầu quy trình làm sạch dữ liệu bằng Học máy (ML Cleaning)...")
    print("[TODO - TV1] 1. Khởi tạo mô hình Isolation Forest & LOF phát hiện ngoại lai.")
    print("[TODO - TV1] 2. Khởi tạo mô hình IterativeImputer (MICE) / KNNImputer điền khuyết thiếu.")
    print("[TODO - TV1] 3. Đánh giá mô hình bằng kỹ thuật che ngẫu nhiên (Masking 15%).")
    print(f"[TODO - TV1] Xuất dữ liệu cuối cùng vào: {out_path.resolve()}")

    # TODO (Giai đoạn 2): Thực thi pipeline ML, kiểm tra assert len(df) >= 5000.


if __name__ == "__main__":
    clean_by_machine_learning()
