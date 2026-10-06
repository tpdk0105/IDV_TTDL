"""
Module: src/04_split_tables.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2005–2024)
Người phụ trách: Thành viên 2 - Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer)
Mục đích:
    - Đọc dữ liệu từ `data/clean/master_clean.csv`.
    - Phân rã dữ liệu thành các bảng Dimension và Fact theo mô hình hình sao (Star Schema, tối thiểu 3NF).
    - Tạo các khóa đại diện (Surrogate Keys) duy nhất cho từng bảng.
    - Bảo toàn các cột cờ ML trong bảng fact (is_outlier_ml, *_is_imputed, cause_is_predicted).
    - Xuất các tệp tin CSV tương ứng vào thư mục `data/tables/`.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 3.
"""

import sys
from pathlib import Path


def split_star_schema_tables() -> None:
    """Tách master_clean.csv thành các bảng dimension và fact trong data/tables/."""
    tables_dir = Path("data/tables")
    tables_dir.mkdir(parents=True, exist_ok=True)

    print(f"[TODO - TV2] Bắt đầu tách master_clean.csv sang Star Schema tại: {tables_dir.resolve()}")
    print("[TODO - TV2] 1. Tách dim_date (Surrogate key YYYYMMDD, mùa, mùa cháy).")
    print("[TODO - TV2] 2. Tách dim_location (ISO3, tên nước, châu lục, tọa độ).")
    print("[TODO - TV2] 3. Tách dim_disaster_type, dim_cause, dim_source.")
    print("[TODO - TV2] 4. Tách fact_disaster_event và fact_wildfire_detail (giữ các cờ ML).")
    # TODO (Giai đoạn 3): Viết logic phân tách bảng và lưu các file CSV.


if __name__ == "__main__":
    split_star_schema_tables()
