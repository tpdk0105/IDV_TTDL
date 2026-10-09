
import sys
from pathlib import Path
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_check(title: str, check_func) -> bool:
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


def validate_star_schema_csv(tables_dir: Path = Path("data/tables")) -> bool:
    print("=" * 80)
    print("BỘ KIỂM THỬ TOÀN VẸN MÔ HÌNH STAR SCHEMA CSV")
    print(f"Thư mục nguồn: {tables_dir.resolve()}")
    print("=" * 80)

    all_passed = True
    required_files = {
        "dim_date": tables_dir / "dim_date.csv",
        "dim_county": tables_dir / "dim_county.csv",
        "dim_cause": tables_dir / "dim_cause.csv",
        "fact_fire_incident": tables_dir / "fact_fire_incident.csv",
        "fact_structure_damage": tables_dir / "fact_structure_damage.csv",
    }

    def check_files_exist():
        missing = [name for name, p in required_files.items() if not p.is_file() or p.stat().st_size == 0]
        if missing:
            return False, f"Thiếu file hoặc file rỗng: {missing}"
        return True, "Cả 5 bảng CSV Star Schema đều tồn tại và có dữ liệu hợp lệ."

    all_passed &= run_check("1. Kiểm tra sự tồn tại của 5 file CSV Star Schema", check_files_exist)
    if not all_passed:
        return False

    df_date = pd.read_csv(required_files["dim_date"])
    df_county = pd.read_csv(required_files["dim_county"])
    df_cause = pd.read_csv(required_files["dim_cause"])
    df_fact = pd.read_csv(required_files["fact_fire_incident"])
    df_damage = pd.read_csv(required_files["fact_structure_damage"])

    # Kiểm tra toàn vẹn tham chiếu (Zero Orphan Foreign Keys)
    def check_referential_integrity():
        errors = []
        orphan_date = set(df_fact["date_id"]) - set(df_date["date_id"])
        if orphan_date:
            errors.append(f"fact_fire_incident chứa {len(orphan_date)} date_id không có trong dim_date")

        orphan_county = set(df_fact["county_id"]) - set(df_county["county_id"])
        if orphan_county:
            errors.append(f"fact_fire_incident chứa {len(orphan_county)} county_id không có trong dim_county")

        orphan_cause = set(df_fact["cause_id"]) - set(df_cause["cause_id"])
        if orphan_cause:
            errors.append(f"fact_fire_incident chứa {len(orphan_cause)} cause_id không có trong dim_cause")

        orphan_inc = set(df_damage["incident_id"]) - set(df_fact["incident_id"])
        if orphan_inc:
            errors.append(f"fact_structure_damage chứa {len(orphan_inc)} incident_id không có trong fact_fire_incident")

        if errors:
            return False, "; ".join(errors)
        return True, "100% Khóa ngoại hợp lệ, Zero Orphan Foreign Keys (0 lỗi toàn vẹn tham chiếu)."

    all_passed &= run_check("2. Toàn vẹn tham chiếu khóa ngoại (Referential Integrity)", check_referential_integrity)

    # Kiểm tra số lượng bản ghi
    def check_row_counts():
        counts = {
            "fact_fire_incident": len(df_fact),
            "fact_structure_damage": len(df_damage),
            "dim_county": len(df_county),
            "dim_cause": len(df_cause),
            "dim_date": len(df_date),
        }
        details = ", ".join([f"{k}: {v:,}" for k, v in counts.items()])

        if counts["fact_fire_incident"] < 5000:
            return False, f"Bảng fact_fire_incident chỉ có {counts['fact_fire_incident']} dòng (< barem 5.000 dòng)!"
        if counts["fact_structure_damage"] < 100000:
            return False, f"Bảng fact_structure_damage quá ít dòng: {counts['fact_structure_damage']} dòng."
        if counts["dim_county"] < 58:
            return False, f"Thiếu hạt trong dim_county: chỉ có {counts['dim_county']} dòng."

        return True, f"Số lượng bản ghi thỏa mãn chuẩn barem ({details})."

    all_passed &= run_check("3. Số lượng bản ghi các bảng (Fact >= 5.000 dòng)", check_row_counts)

    # Kiểm tra tính duy nhất của Primary Keys
    def check_pk_uniqueness():
        pks = [
            ("dim_date", df_date, "date_id"),
            ("dim_county", df_county, "county_id"),
            ("dim_cause", df_cause, "cause_id"),
            ("fact_fire_incident", df_fact, "incident_id"),
            ("fact_structure_damage", df_damage, "record_id"),
        ]
        for tbl_name, df, pk_col in pks:
            if df[pk_col].duplicated().any():
                dup_count = df[pk_col].duplicated().sum()
                return False, f"Trùng lặp khóa chính {pk_col} tại {tbl_name}: {dup_count} dòng trùng."
        return True, "100% Khóa chính trên cả 5 bảng đều duy nhất tuyệt đối (No Duplicate PK)."

    all_passed &= run_check("4. Tính duy nhất của Primary Keys", check_pk_uniqueness)

    # Ràng buộc miền giá trị
    def check_domain_constraints():
        neg_acres = (df_fact["acres_burned"] < 0).sum()
        neg_ha = (df_fact["burned_area_ha"] < 0).sum()
        if neg_acres > 0 or neg_ha > 0:
            return False, f"Có {neg_acres + neg_ha} bản ghi diện tích cháy âm (< 0)!"

        neg_dmg = (df_fact["total_structures_destroyed"] < 0).sum() + (df_fact["deaths_direct"] < 0).sum()
        if neg_dmg > 0:
            return False, f"Có {neg_dmg} bản ghi thiệt hại hoặc thương vong mang giá trị âm!"

        # Tọa độ California
        valid_geo = df_fact.dropna(subset=["latitude", "longitude"])
        out_of_bounds = (
            (valid_geo["latitude"] < 32.0) | (valid_geo["latitude"] > 42.0) |
            (valid_geo["longitude"] < -125.0) | (valid_geo["longitude"] > -114.0)
        ).sum()
        if out_of_bounds > 0:
            return False, f"Có {out_of_bounds} bản ghi tọa độ nằm ngoài phạm vi California!"

        return True, "Tất cả các ràng buộc diện tích, thiệt hại, thương vong và tọa độ đều hợp lệ."

    all_passed &= run_check("5. Ràng buộc miền giá trị bảng fact_fire_incident", check_domain_constraints)

    # Cờ nhị phân
    def check_binary_flags():
        for col in ["is_outlier_ml", "burned_area_is_imputed", "cause_is_predicted"]:
            if col in df_fact.columns:
                invalid = (~df_fact[col].isin([0, 1])).sum()
                if invalid > 0:
                    return False, f"Cột {col} có {invalid} giá trị khác [0, 1]!"

        if "is_fire_season" in df_date.columns:
            invalid_season = (~df_date["is_fire_season"].isin([0, 1])).sum()
            if invalid_season > 0:
                return False, f"Cột is_fire_season có {invalid_season} giá trị khác [0, 1]!"

        return True, "100% cờ nhị phân chỉ nhận giá trị [0, 1]."

    all_passed &= run_check("6. Giá trị cờ nhị phân (Binary Flags IN {0, 1})", check_binary_flags)

    # Phạm vi thời gian nghiên cứu
    def check_time_range():
        years = df_date["year"].unique()
        min_year, max_year = years.min(), years.max()
        count_years = len(years)

        if min_year < 2006 or max_year > 2025:
            return False, f"Năm ngoài phạm vi 2006-2025: Min={min_year}, Max={max_year}."
        if count_years < 20:
            return False, f"Dữ liệu không đủ 20 năm: chỉ có {count_years}/20 năm."

        return True, f"Dữ liệu phủ kín toàn bộ 20 năm liên tục ({min_year} - {max_year}, đủ {count_years}/20 năm)."

    all_passed &= run_check("7. Phạm vi thời gian nghiên cứu (Đủ 20 năm 2006–2025)", check_time_range)

    print("\n" + "=" * 80)
    if all_passed:
        print("[KẾT QUẢ TỔNG THỂ]: CHÚC MỪNG! TẤT CẢ 7 PHÉP KIỂM THỬ ĐÃ ĐẠT (PASS 100%).")
        print("Mô hình Star Schema CSV đã hoàn toàn sẵn sàng cho Tableau Desktop & Tableau Web/Public!")
    else:
        print("[KẾT QUẢ TỔNG THỂ]: PHÁT HIỆN LỖI TRONG KIỂM THỬ STAR SCHEMA CSV!")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    is_valid = validate_star_schema_csv()
    if not is_valid:
        sys.exit(1)
    sys.exit(0)
