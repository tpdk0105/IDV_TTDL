"""
Module: src/05_build_db.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng California (2006–2025)
Người phụ trách: Thành viên 2 - Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer)
Mục đích:
    - Khởi tạo cơ sở dữ liệu SQLite tại `data/tables/database.sqlite`.
    - Kích hoạt cơ chế kiểm soát khóa ngoại: `PRAGMA foreign_keys = ON;`.
    - Thực thi DDL từ `sql/schema.sql` để tạo cấu trúc bảng với đầy đủ PK, FK, CHECK, UNIQUE, INDEX.
    - Nạp toàn bộ dữ liệu từ các tệp CSV trong `data/tables/` vào 5 bảng tương ứng:
        1. dim_date
        2. dim_county
        3. dim_cause
        4. fact_fire_incident
        5. fact_structure_damage
    - Kiểm tra tính toàn vẹn khóa ngoại (Zero Orphan Foreign Keys) và ràng buộc toàn vẹn.
"""

import sqlite3
import sys
from pathlib import Path

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def build_sqlite_database() -> None:
    """Tạo database.sqlite, thực thi schema.sql và nạp dữ liệu từ data/tables/."""
    tables_dir = Path("data/tables")
    db_path = tables_dir / "database.sqlite"
    schema_path = Path("sql/schema.sql")

    if not schema_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file DDL schema tại {schema_path}!")

    # Nếu file db cũ tồn tại, xóa để tạo mới hoàn toàn sạch sẽ
    if db_path.exists():
        try:
            db_path.unlink()
        except OSError as e:
            print(f"[TV2 - BUILD DB] Cảnh báo không thể xóa file cũ: {e}")

    print(f"[TV2 - BUILD DB] Khởi tạo CSDL SQLite tại: {db_path.resolve()}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Bật hỗ trợ khóa ngoại
    cursor.execute("PRAGMA foreign_keys = ON;")
    print("[TV2 - BUILD DB] Đã kích hoạt PRAGMA foreign_keys = ON;")

    # 2. Thực thi file schema.sql
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    print(f"[TV2 - BUILD DB] Đã thực thi thành công cấu trúc schema DDL từ: {schema_path.resolve()}")

    # 3. Danh sách nạp dữ liệu theo đúng thứ tự: Dimension trước -> Fact sau
    load_sequence = [
        ("dim_date", "dim_date.csv"),
        ("dim_county", "dim_county.csv"),
        ("dim_cause", "dim_cause.csv"),
        ("fact_fire_incident", "fact_fire_incident.csv"),
        ("fact_structure_damage", "fact_structure_damage.csv"),
    ]

    for table_name, csv_file in load_sequence:
        csv_path = tables_dir / csv_file
        if not csv_path.exists():
            raise FileNotFoundError(f"Thiếu file dữ liệu {csv_path} để nạp vào bảng {table_name}!")

        print(f"[TV2 - BUILD DB] Đang nạp dữ liệu vào bảng `{table_name}` từ {csv_file}...")
        df = pd.read_csv(csv_path)

        # Nạp dữ liệu vào SQLite với if_exists='append' để bảo toàn PK/FK/CHECK trong schema.sql
        df.to_sql(table_name, conn, if_exists="append", index=False)

        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"  -> Bảng `{table_name}`: Đã nạp thành công {count:,} bản ghi.")

    # 4. Kiểm tra toàn vẹn khóa ngoại (Foreign Key Check)
    cursor.execute("PRAGMA foreign_key_check;")
    fk_errors = cursor.fetchall()
    if fk_errors:
        print(f"[CẢNH BÁO / LỖI] Phát hiện {len(fk_errors)} vi phạm khóa ngoại:")
        for err in fk_errors[:10]:
            print("  ", err)
        raise ValueError(f"Có {len(fk_errors)} lỗi khóa ngoại trong CSDL SQLite!")
    else:
        print("[TV2 - BUILD DB] PRAGMA foreign_key_check: 0 LỖI (Zero Orphan Foreign Keys - Toàn vẹn 100%)!")

    conn.commit()
    conn.close()
    print(f"[TV2 - BUILD DB] Hoàn tất xây dựng CSDL SQLite thành công tại: {db_path.resolve()}\n")


if __name__ == "__main__":
    build_sqlite_database()
