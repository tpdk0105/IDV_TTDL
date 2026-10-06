"""
Module: src/02_eda.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2005–2024)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Thực hiện phân tích khám phá dữ liệu ban đầu (EDA) trên các tập dữ liệu thô trong `data/raw/`.
    - Đánh giá kiểu dữ liệu, tỷ lệ khuyết thiếu (Missing Values), trùng lặp (Duplicates), và ngoại lai sơ bộ.
    - Xuất các thống kê và ma trận thiếu sang `docs/DATA_QUALITY_REPORT.md`.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 2.
"""

import sys
from pathlib import Path


def run_initial_eda() -> None:
    """Thực hiện EDA trên dữ liệu thô và xuất báo cáo chất lượng."""
    raw_dir = Path("data/raw")
    print(f"[TODO - TV1] Thực hiện EDA dữ liệu thô từ: {raw_dir.resolve()}")
    print("[TODO - TV1] Thống kê tỷ lệ khuyết thiếu, trùng lặp và phân phối các biến định lượng...")
    # TODO (Giai đoạn 2): Nạp DataFrame, tính tỷ lệ missing, xuất sang docs/DATA_QUALITY_REPORT.md.


if __name__ == "__main__":
    run_initial_eda()
