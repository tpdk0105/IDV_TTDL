"""
Module: src/07_validate.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 2 - Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer)
Mục đích:
    - Kiểm thử tự động tính toàn vẹn và chất lượng của cơ sở dữ liệu `database.sqlite`:
        1. Kiểm tra toàn vẹn tham chiếu (Referential Integrity): Không có khóa ngoại mồ côi.
        2. Kiểm tra tính duy nhất (Uniqueness): Không trùng lặp bất kỳ khóa chính nào.
        3. Kiểm tra số lượng bản ghi: Bảng `fact_disaster_event` đạt tối thiểu 5.000 dòng.
        4. Kiểm tra các ràng buộc miền giá trị (CHECK constraints):
           - deaths >= 0, damage_usd >= 0, burned_area_ha >= 0
           - year BETWEEN 2006 AND 2025
           - latitude [-90, 90], longitude [-180, 180]
           - Các cột cờ ML chỉ nhận giá trị 0 hoặc 1.
    - Trả về mã thoát (exit code) = 0 nếu đạt toàn bộ tiêu chuẩn; khác 0 nếu phát hiện lỗi.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 3.
"""

import sqlite3
import sys
from pathlib import Path


def validate_database_integrity() -> bool:
    """Thực hiện các phép kiểm tra toàn vẹn và ràng buộc trên SQLite DB."""
    db_path = Path("data/tables/database.sqlite")
    print(f"[TODO - TV2] Bắt đầu kiểm thử toàn vẹn CSDL tại: {db_path.resolve()}")
    print("[TODO - TV2] 1. Kiểm tra toàn vẹn tham chiếu khóa ngoại (PRAGMA foreign_key_check)...")
    print("[TODO - TV2] 2. Kiểm tra số lượng bản ghi bảng fact >= 5.000...")
    print("[TODO - TV2] 3. Kiểm tra các ràng buộc CHECK và miền giá trị hợp lệ...")
    print("[TODO - TV2] 4. Kiểm tra các cờ ML nhận giá trị [0, 1]...")
    # TODO (Giai đoạn 3): Thực hiện các câu truy vấn kiểm thử và trả về True/False.
    return True


if __name__ == "__main__":
    is_valid = validate_database_integrity()
    if not is_valid:
        print("[FAIL] Kiểm thử chất lượng dữ liệu thất bại!")
        sys.exit(1)
    print("[PASS] Khung kiểm thử toàn vẹn sẵn sàng.")
    sys.exit(0)
