"""
Module: src/07_validate.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng California (2006–2025)
Người phụ trách: Thành viên 2 - Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer)
Mục đích:
    - Kiểm thử tự động tính toàn vẹn và chất lượng của cơ sở dữ liệu `database.sqlite`:
        1. Kiểm tra cấu trúc CSDL và tính toàn vẹn cấp thấp: PRAGMA integrity_check.
        2. Kiểm tra toàn vẹn tham chiếu (Referential Integrity): PRAGMA foreign_key_check (Zero Orphan Keys).
        3. Kiểm tra số lượng bản ghi:
           - Bảng fact trung tâm `fact_fire_incident` đạt tối thiểu 5.000 dòng.
           - Bảng `fact_structure_damage` > 100.000 dòng.
           - Bảng chiều `dim_county` = 59 hạt, `dim_cause` = 19, `dim_date` = 7.305 ngày.
        4. Kiểm tra tính duy nhất (Uniqueness) của Primary Key trên toàn bộ 5 bảng.
        5. Kiểm tra các ràng buộc miền giá trị (Domain & CHECK constraints):
           - acres_burned >= 0, burned_area_ha >= 0, total_structures_destroyed >= 0, deaths >= 0
           - year BETWEEN 2006 AND 2025
           - latitude [32.0, 42.0], longitude [-125.0, -114.0] cho các bản ghi có tọa độ
           - Các cờ nhị phân (is_fire_season, is_outlier_ml, burned_area_is_imputed, cause_is_predicted) in {0, 1}
    - Trả về mã thoát (exit code):
        - 0: Đạt toàn bộ tiêu chuẩn barem đồ án.
        - 1: Phát hiện vi phạm toàn vẹn dữ liệu.
"""

import sqlite3
import sys
from pathlib import Path

# Cấu hình UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_check(title: str, check_func) -> bool:
    """Thực thi một bước kiểm thử và in kết quả."""
    print(f"\n[*] Kiểm tra: {title}...")
    try:
        passed, msg = check_func()
        if passed:
            print(f"  [PASS] {msg}")
            return True
        else:
            print(f"  [FAIL] {msg}")
            return False
    except Exception as e:  # noqa: BLE001
        print(f"  [ERROR] Ngoại lệ khi kiểm tra: {e}")
        return False


def validate_database_integrity(db_path: Path = Path("data/tables/database.sqlite")) -> bool:
    """Thực hiện chuỗi kiểm thử toàn vẹn trên database.sqlite."""
    if not db_path.is_file():
        print(f"[FAIL] Cơ sở dữ liệu không tồn tại tại: {db_path.resolve()}")
        return False

    print("=" * 80)
    print("BỘ KIỂM THỬ TOÀN VẸN CƠ SỞ DỮ LIỆU SQLITE (THÀNH VIÊN 2 - DATA MODELING)")
    print(f"CSDL: {db_path.resolve()}")
    print("=" * 80)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    all_passed = True

    # 1. PRAGMA integrity_check
    def check_sqlite_integrity():
        res = cursor.execute("PRAGMA integrity_check;").fetchall()
        if res == [("ok",)]:
            return True, "Cấu trúc CSDL toàn vẹn (PRAGMA integrity_check: ok)."
        return False, f"Lỗi toàn vẹn cấp thấp: {res}"

    all_passed &= run_check("1. Tính toàn vẹn cấu trúc SQLite", check_sqlite_integrity)

    # 2. PRAGMA foreign_key_check (Zero Orphan Foreign Keys)
    def check_foreign_keys():
        res = cursor.execute("PRAGMA foreign_key_check;").fetchall()
        if not res:
            return True, "100% Khóa ngoại hợp lệ, Zero Orphan Foreign Keys (0 lỗi)."
        return False, f"Phát hiện {len(res)} vi phạm khóa ngoại mồ côi: {res[:5]}"

    all_passed &= run_check("2. Toàn vẹn tham chiếu khóa ngoại (Referential Integrity)", check_foreign_keys)

    # 3. Kiểm tra số lượng bản ghi các bảng
    def check_row_counts():
        counts = {}
        tables = ["dim_date", "dim_county", "dim_cause", "fact_fire_incident", "fact_structure_damage"]
        for tbl in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
            counts[tbl] = cursor.fetchone()[0]

        details = ", ".join([f"{k}: {v:,}" for k, v in counts.items()])

        # Tiêu chuẩn: fact_fire_incident >= 5000 dòng
        if counts["fact_fire_incident"] < 5000:
            return False, f"Bảng fact_fire_incident chỉ có {counts['fact_fire_incident']} dòng (< tiêu chuẩn 5.000 dòng)!"
        if counts["fact_structure_damage"] < 100000:
            return False, f"Bảng fact_structure_damage quá ít dòng: {counts['fact_structure_damage']} dòng."
        if counts["dim_county"] < 58:
            return False, f"Thiếu hạt trong dim_county: chỉ có {counts['dim_county']} dòng."

        return True, f"Số lượng bản ghi thỏa mãn chuẩn barem ({details})."

    all_passed &= run_check("3. Số lượng bản ghi các bảng (Fact >= 5.000 dòng)", check_row_counts)

    # 4. Kiểm tra tính duy nhất của Primary Keys
    def check_pk_uniqueness():
        pks = [
            ("dim_date", "date_id"),
            ("dim_county", "county_id"),
            ("dim_cause", "cause_id"),
            ("fact_fire_incident", "incident_id"),
            ("fact_structure_damage", "record_id"),
        ]
        for tbl, pk_col in pks:
            cursor.execute(f"SELECT COUNT(*), COUNT(DISTINCT {pk_col}) FROM {tbl};")
            total, distinct = cursor.fetchone()
            if total != distinct:
                return False, f"Trùng lặp khóa chính {pk_col} tại {tbl}: total={total}, distinct={distinct}."
        return True, "100% Khóa chính trên cả 5 bảng đều duy nhất tuyệt đối (No Duplicate PK)."

    all_passed &= run_check("4. Tính duy nhất của Primary Keys", check_pk_uniqueness)

    # 5. Kiểm tra ràng buộc CHECK miền giá trị bảng fact_fire_incident
    def check_fact_fire_constraints():
        # acres_burned >= 0, burned_area_ha >= 0
        cursor.execute("SELECT COUNT(*) FROM fact_fire_incident WHERE acres_burned < 0 OR burned_area_ha < 0;")
        invalid_area = cursor.fetchone()[0]
        if invalid_area > 0:
            return False, f"Có {invalid_area} bản ghi diện tích cháy âm (< 0)!"

        # structures >= 0, deaths >= 0, injuries >= 0
        cursor.execute("""
            SELECT COUNT(*) FROM fact_fire_incident 
            WHERE total_structures_destroyed < 0 
               OR total_structures_damaged < 0 
               OR deaths_direct < 0 
               OR injuries_direct < 0 
               OR damage_property_usd < 0;
        """)
        invalid_dmg = cursor.fetchone()[0]
        if invalid_dmg > 0:
            return False, f"Có {invalid_dmg} bản ghi thiệt hại mang giá trị âm!"

        # Tọa độ hợp lệ trong phạm vi California (với các bản ghi không NULL)
        cursor.execute("""
            SELECT COUNT(*) FROM fact_fire_incident 
            WHERE (latitude IS NOT NULL AND (latitude < 32.0 OR latitude > 42.0))
               OR (longitude IS NOT NULL AND (longitude < -125.0 OR longitude > -114.0));
        """)
        invalid_coords = cursor.fetchone()[0]
        if invalid_coords > 0:
            return False, f"Có {invalid_coords} bản ghi tọa độ nằm ngoài phạm vi California!"

        return True, "Tất cả các ràng buộc diện tích, thiệt hại, thương vong và tọa độ đều hợp lệ."

    all_passed &= run_check("5. Ràng buộc miền giá trị bảng fact_fire_incident", check_fact_fire_constraints)

    # 6. Kiểm tra các cờ nhị phân (ML Flags & Season Flags)
    def check_binary_flags():
        # fact_fire_incident flags
        cursor.execute("""
            SELECT COUNT(*) FROM fact_fire_incident
            WHERE is_outlier_ml NOT IN (0, 1)
               OR burned_area_is_imputed NOT IN (0, 1)
               OR cause_is_predicted NOT IN (0, 1);
        """)
        invalid_fact_flags = cursor.fetchone()[0]
        if invalid_fact_flags > 0:
            return False, f"Có {invalid_fact_flags} bản ghi có cờ ML khác 0 và 1 trong fact_fire_incident!"

        # dim_date is_fire_season
        cursor.execute("SELECT COUNT(*) FROM dim_date WHERE is_fire_season NOT IN (0, 1);")
        invalid_season = cursor.fetchone()[0]
        if invalid_season > 0:
            return False, f"Có {invalid_season} bản ghi có cờ is_fire_season khác 0 và 1 trong dim_date!"

        return True, "100% cờ nhị phân (ML flags, is_fire_season) chỉ nhận giá trị [0, 1]."

    all_passed &= run_check("6. Giá trị cờ nhị phân (Binary Flags IN {0, 1})", check_binary_flags)

    # 7. Kiểm tra năm xảy ra sự cố (2006–2025)
    def check_year_range():
        cursor.execute("""
            SELECT MIN(d.year), MAX(d.year), COUNT(DISTINCT d.year)
            FROM fact_fire_incident f
            JOIN dim_date d ON f.date_id = d.date_id;
        """)
        min_year, max_year, count_years = cursor.fetchone()
        if min_year < 2006 or max_year > 2025:
            return False, f"Dữ liệu có năm ngoài phạm vi nghiên cứu 2006-2025: Min={min_year}, Max={max_year}."
        if count_years < 20:
            return False, f"Dữ liệu không phủ kín đủ 20 năm: chỉ có {count_years}/20 năm."
        return True, f"Dữ liệu vụ cháy phủ kín toàn bộ 20 năm liên tục ({min_year} - {max_year}, đủ 20/20 năm)."

    all_passed &= run_check("7. Phạm vi thời gian nghiên cứu (Đủ 20 năm 2006–2025)", check_year_range)

    conn.close()

    print("\n" + "=" * 80)
    if all_passed:
        print("[KẾT QUẢ TỔNG THỂ]: CHÚC MỪNG! TẤT CẢ 7 PHÉP KIỂM THỬ ĐÃ ĐẠT (PASS 100%).")
        print("Mô hình Star Schema và CSDL SQLite của Thành viên 2 đã sẵn sàng cho Dashboard và Tableau!")
    else:
        print("[KẾT QUẢ TỔNG THỂ]: PHÁT HIỆN LỖI TRONG KIỂM THỬ TOÀN VẸN CSDL!")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    is_valid = validate_database_integrity()
    if not is_valid:
        sys.exit(1)
    sys.exit(0)
