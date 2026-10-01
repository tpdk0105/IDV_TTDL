"""
Module: src/06_export_json.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 2 (Mô hình Dữ liệu) & Thành viên 3 (Dashboard)
Mục đích:
    - Kết nối tới `data/tables/database.sqlite`.
    - Thực thi các câu truy vấn phân tích (JOIN, GROUP BY, Window functions) từ `sql/queries_for_charts.sql`.
    - Tối ưu hóa và định dạng dữ liệu đầu ra thành các tệp tin JSON nén gọn nhẹ.
    - Lưu các tệp JSON vào thư mục `dashboard/data/` để phục vụ trực tiếp cho 12 biểu đồ trên giao diện web.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 3 & 4.
"""

import json
import sqlite3
import sys
from pathlib import Path


def export_charts_json() -> None:
    """Truy vấn CSDL và xuất các file JSON cho 12 biểu đồ vào dashboard/data/."""
    db_path = Path("data/tables/database.sqlite")
    out_dir = Path("dashboard/data")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[TODO - TV2 & TV3] Bắt đầu xuất JSON dữ liệu biểu đồ từ: {db_path.resolve()}")
    print(f"[TODO - TV2 & TV3] Thư mục đích lưu JSON: {out_dir.resolve()}")
    print("[TODO - TV2 & TV3] Xuất chart_01_data.json đến chart_12_data.json...")
    # TODO (Giai đoạn 3 & 4): Chạy truy vấn SQL và ghi các file JSON.


if __name__ == "__main__":
    export_charts_json()
