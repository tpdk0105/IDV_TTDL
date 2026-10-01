"""
Module: src/05_build_db.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 2 - Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer)
Mục đích:
    - Khởi tạo cơ sở dữ liệu SQLite tại `data/tables/database.sqlite`.
    - Kích hoạt cơ chế kiểm soát khóa ngoại: `PRAGMA foreign_keys = ON;`.
    - Thực thi DDL từ `sql/schema.sql` để tạo cấu trúc bảng với đầy đủ PK, FK, CHECK, UNIQUE, INDEX.
    - Nạp toàn bộ dữ liệu từ các tệp CSV trong `data/tables/` vào các bảng tương ứng.
    - Bắt lỗi và thông báo nếu có bất kỳ vi phạm ràng buộc toàn vẹn nào.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 3.
"""

import sqlite3
import sys
from pathlib import Path


def build_sqlite_database() -> None:
    """Tạo database.sqlite, thực thi schema.sql và nạp dữ liệu từ data/tables/."""
    db_path = Path("data/tables/database.sqlite")
    schema_path = Path("sql/schema.sql")

    print(f"[TODO - TV2] Bắt đầu khởi tạo CSDL SQLite tại: {db_path.resolve()}")
    print("[TODO - TV2] Bật PRAGMA foreign_keys = ON;")
    print(f"[TODO - TV2] Thực thi cấu trúc schema từ: {schema_path.resolve()}")
    print("[TODO - TV2] Nạp các file CSV từ data/tables/ vào các bảng tương ứng...")
    # TODO (Giai đoạn 3): Kết nối SQLite, tạo bảng và nạp dữ liệu.


if __name__ == "__main__":
    build_sqlite_database()
