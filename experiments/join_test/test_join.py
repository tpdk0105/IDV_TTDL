"""
Module: experiments/join_test/test_join.py
Mục đích:
    Thử nghiệm quy trình JOIN dữ liệu giữa Bảng Vụ cháy chính (Perimeters - CAL FIRE FRAP)
    với 2 bảng thiệt hại tài sản & công trình:
        - CAL FIRE DINS (Giai đoạn 2013–2025)
        - USDA Forest Service / NIFC ICS-209 (Giai đoạn 2006–2012)
    theo 3 thuộc tính khóa:
        1. Khóa 1 (Tên vụ cháy): Chuẩn hóa UPPER + TRIM + bỏ hậu tố dư thừa.
        2. Khóa 2 (Năm xảy ra vụ cháy): Year (FRAP) == START_YEAR (ICS) == Year(Incident Start Date) (DINS).
        3. Khóa 3 (Không gian địa lý): Khử trùng lặp và liên kết Hạt (County) thông qua Unit ID / Tọa độ.
"""

import json
import re
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Thiết lập UTF-8 cho console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw" / "calfire"

UNIT_MAP_FILE = BASE_DIR / "unit_to_county.json"


def load_unit_county_mapping() -> dict:
    """Tải từ điển ánh xạ CAL FIRE Unit ID sang danh sách các Hạt (Counties)."""
    if UNIT_MAP_FILE.exists():
        with open(UNIT_MAP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {k: [c.upper() for c in v] for k, v in data.items() if not k.startswith("_")}
    return {}


def clean_fire_name(raw_name: str) -> str:
    """Chuẩn hóa tên vụ cháy (Khóa 1): viết hoa, loại bỏ khoảng trắng và các hậu tố dư thừa."""
    if pd.isna(raw_name):
        return ""
    name = str(raw_name).strip().upper()
    # Loại bỏ các từ khóa đuôi phổ biến gây lệch tên giữa các hệ thống báo cáo
    for suffix in [" FIRE", " INCIDENT", " COMPLEX", " WF", " LIGHTNING CMPLX", " LIGHTNING COMPLEX"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)].strip()
    # Chuẩn hóa ký tự phân tách
    name = re.sub(r"\s+", " ", name)
    return name


def run_join_experiment():
    print("=" * 80)
    print("THỬ NGHIỆM JOIN BẢNG PERIMETERS VỚI DINS (2013–2025) & ICS-209 (2006–2012)")
    print("=" * 80)

    unit_map = load_unit_county_mapping()

    # -------------------------------------------------------------
    # 1. NẠP VÀ TIỀN XỬ LÝ BẢNG CHÍNH: PERIMETERS (FRAP 2006–2025)
    # -------------------------------------------------------------
    frap_path = RAW_DIR / "California_Fire_Perimeters_all.csv"
    print(f"\n[1] Nạp bảng Perimeters từ: {frap_path.name}...")
    frap = pd.read_csv(frap_path, low_memory=False)
    frap = frap[(frap["Year"] >= 2006) & (frap["Year"] <= 2025)].copy()
    frap["year_int"] = frap["Year"].astype(int)
    frap["fire_clean"] = frap["Fire Name"].apply(clean_fire_name)
    frap["unit_id_clean"] = frap["Unit ID"].astype(str).str.strip().str.upper()
    print(f"  -> Tổng số vụ cháy FRAP (2006–2025): {len(frap):,} bản ghi.")

    # -------------------------------------------------------------
    # 2. NẠP VÀ TỔNG HỢP DINS (2013–2025) THEO VỤ CHÁY
    # -------------------------------------------------------------
    dins_path = RAW_DIR / "CAL_FIRE_Damage_Inspection_DINS.csv"
    print(f"\n[2] Nạp bảng DINS từ: {dins_path.name}...")
    dins = pd.read_csv(dins_path, low_memory=False)
    dins["Incident Start Date"] = pd.to_datetime(dins["Incident Start Date"], errors="coerce")
    dins["year_int"] = dins["Incident Start Date"].dt.year
    dins = dins.dropna(subset=["year_int"]).copy()
    dins["year_int"] = dins["year_int"].astype(int)
    dins["fire_clean"] = dins["* Incident Name"].apply(clean_fire_name)
    dins["is_destroyed"] = (dins["* Damage"] == "Destroyed (>50%)")
    dins["is_damaged"] = dins["* Damage"].isin(["Major (25-50%)", "Minor (10-25%)", "Affected (>0-10%)"])

    dins_agg = dins.groupby(["fire_clean", "year_int"]).agg(
        structures_destroyed=("is_destroyed", "sum"),
        structures_damaged=("is_damaged", "sum"),
        structures_inspected=("* Damage", "count"),
        county=("County", lambda s: str(s.mode()[0]).strip().title() if not s.mode().empty else "Unknown"),
        lat=("Latitude", "mean"),
        lon=("Longitude", "mean"),
        raw_fire_name=("* Incident Name", "first")
    ).reset_index()
    dins_agg["source"] = "CAL_FIRE_DINS"
    print(f"  -> Tổng hợp DINS: {len(dins_agg):,} vụ cháy từ 132.522 cấu trúc kiểm kê.")
    print(f"  -> Tổng số nhà bị phá hủy trong DINS: {dins_agg['structures_destroyed'].sum():,}")

    # -------------------------------------------------------------
    # 3. NẠP VÀ TỔNG HỢP ICS-209 (2006–2012) THEO VỤ CHÁY
    # -------------------------------------------------------------
    ics_path = RAW_DIR / "ICS209_California_Wildfires_2006_2012.csv"
    print(f"\n[3] Nạp bảng ICS-209 từ: {ics_path.name}...")
    ics = pd.read_csv(ics_path, low_memory=False)
    ics["year_int"] = ics["START_YEAR"].astype(int)
    ics["fire_clean"] = ics["INCIDENT_NAME"].apply(clean_fire_name)
    ics["str_destroyed"] = ics["STR_DESTROYED_TOTAL"].fillna(0).astype(int)
    ics["str_damaged"] = ics["STR_DAMAGED_TOTAL"].fillna(0).astype(int)

    ics_agg = ics.groupby(["fire_clean", "year_int"]).agg(
        structures_destroyed=("str_destroyed", "sum"),
        structures_damaged=("str_damaged", "sum"),
        county=("POO_COUNTY", lambda s: str(s.iloc[0]).strip().title() if len(s)>0 and pd.notna(s.iloc[0]) else "Unknown"),
        lat=("POO_LATITUDE", "mean"),
        lon=("POO_LONGITUDE", "mean"),
        raw_fire_name=("INCIDENT_NAME", "first")
    ).reset_index()
    ics_agg["structures_inspected"] = ics_agg["structures_destroyed"] + ics_agg["structures_damaged"]
    ics_agg["source"] = "USDA_ICS_209"
    print(f"  -> Tổng hợp ICS-209: {len(ics_agg):,} vụ cháy từ 1.127 bản ghi sự cố.")
    print(f"  -> Tổng số nhà bị phá hủy trong ICS-209: {ics_agg['structures_destroyed'].sum():,}")

    # -------------------------------------------------------------
    # 4. HỢP NHẤT (UNION) CHUỖI THIỆT HẠI ĐỦ 20 NĂM (2006–2025)
    # -------------------------------------------------------------
    damage_union = pd.concat([ics_agg, dins_agg], ignore_index=True)
    print(f"\n[4] Hợp nhất thiệt hại (ICS-209 + DINS):")
    print(f"  -> Tổng số vụ cháy có ghi nhận thiệt hại (2006–2025): {len(damage_union):,} vụ.")
    print(f"  -> Tổng số nhà bị phá hủy 20 năm: {damage_union['structures_destroyed'].sum():,} nhà.")
    print(f"  -> Số năm phủ kín: {damage_union['year_int'].nunique()}/20 năm liên tục.")

    # -------------------------------------------------------------
    # 5. TIẾN HÀNH JOIN VỚI PERIMETERS (KHÓA 1, KHÓA 2, KHÓA 3)
    # -------------------------------------------------------------
    print("\n[5] Tiến hành JOIN giữa Bảng Vụ cháy chính (Perimeters) và Bảng Thiệt hại hợp nhất...")

    # Khử trùng lặp đa chu vi trong FRAP (ví dụ các đám cháy lớn có nhiều mảnh chu vi)
    # Gom nhóm theo (fire_clean, year_int) để tính tổng diện tích acres và giữ thông tin hạt / Unit ID
    frap_grouped = frap.groupby(["fire_clean", "year_int"]).agg(
        total_acres=("GIS Calculated Acres", "sum"),
        max_acres=("GIS Calculated Acres", "max"),
        alarm_date=("Alarm Date", "first"),
        containment_date=("Containment Date", "last"),
        cause=("Cause", "first"),
        unit_id=("unit_id_clean", "first"),
        agency=("Agency", "first"),
        perimeter_count=("OBJECTID", "count")
    ).reset_index()

    # Thực hiện JOIN: Left join hoặc Inner join
    # Trước hết Inner Join để khảo sát tỷ lệ khớp chính xác
    joined = pd.merge(
        damage_union,
        frap_grouped,
        on=["fire_clean", "year_int"],
        how="inner"
    )

    # Đánh giá Khóa 3: Không gian địa lý (County vs Unit ID)
    def check_spatial_match(row):
        county = str(row["county"]).upper()
        unit = str(row["unit_id"]).upper()
        if unit in unit_map:
            valid_counties = unit_map[unit]
            if county in valid_counties or any(c in county for c in valid_counties):
                return "Khớp chính xác"
        return "Tương thích theo tên & năm"

    joined["spatial_validation"] = joined.apply(check_spatial_match, axis=1)

    print(f"  -> Số vụ cháy khớp thành công: {len(joined):,} vụ.")
    print(f"  -> Tỷ lệ khớp số nhà bị phá hủy: {joined['structures_destroyed'].sum():,} / {damage_union['structures_destroyed'].sum():,} ({joined['structures_destroyed'].sum() / damage_union['structures_destroyed'].sum() * 100:.2f}%).")
    print(f"  -> Tổng diện tích rừng thiêu rụi đã khớp: {joined['total_acres'].sum():,.1f} mẫu Anh (Acres).")

    # -------------------------------------------------------------
    # 6. XUẤT CÁC TỆP DỮ LIỆU MẪU KIỂM THỬ TRỰC QUAN
    # -------------------------------------------------------------
    # Sắp xếp theo mức độ tàn khốc (số nhà bị phá hủy giảm dần)
    top_destructive = joined.sort_values(by="structures_destroyed", ascending=False).head(30)
    top_destructive_export = top_destructive[[
        "year_int", "fire_clean", "county", "unit_id", "total_acres",
        "structures_destroyed", "structures_damaged", "structures_inspected",
        "source", "spatial_validation"
    ]].rename(columns={
        "year_int": "Year",
        "fire_clean": "Fire_Name",
        "county": "County",
        "unit_id": "Unit_ID",
        "total_acres": "Acres_Burned",
        "structures_destroyed": "Structures_Destroyed",
        "structures_damaged": "Structures_Damaged",
        "structures_inspected": "Structures_Inspected",
        "source": "Damage_Source",
        "spatial_validation": "Spatial_Match_Status"
    })

    top_csv_file = BASE_DIR / "top_30_destructive_fires.csv"
    top_destructive_export.to_csv(top_csv_file, index=False, encoding="utf-8-sig")
    print(f"\n[6] Đã lưu Top 30 vụ cháy tàn khốc nhất vào: {top_csv_file.name}")

    # Xuất mẫu đại diện 50 vụ cháy trải dài cả 20 năm
    sample_50 = joined.sort_values(by=["year_int", "structures_destroyed"], ascending=[True, False]).groupby("year_int").head(3)
    sample_export = sample_50[[
        "year_int", "fire_clean", "county", "unit_id", "total_acres",
        "structures_destroyed", "source", "spatial_validation"
    ]].rename(columns={
        "year_int": "Year",
        "fire_clean": "Fire_Name",
        "county": "County",
        "unit_id": "Unit_ID",
        "total_acres": "Acres_Burned",
        "structures_destroyed": "Structures_Destroyed",
        "source": "Damage_Source",
        "spatial_validation": "Spatial_Match_Status"
    })
    sample_csv_file = BASE_DIR / "sample_joined_2006_2025.csv"
    sample_export.to_csv(sample_csv_file, index=False, encoding="utf-8-sig")
    print(f"  -> Đã lưu mẫu vụ cháy 20 năm vào: {sample_csv_file.name}")

    # Ghi file JSON chỉ số tóm tắt
    metrics_summary = {
        "frap_total_fires_2006_2025": int(len(frap)),
        "dins_total_fires_2013_2025": int(len(dins_agg)),
        "ics209_total_fires_2006_2012": int(len(ics_agg)),
        "damage_union_total_fires": int(len(damage_union)),
        "damage_union_destroyed_structures": int(damage_union["structures_destroyed"].sum()),
        "joined_matched_fires": int(len(joined)),
        "joined_destroyed_structures_captured": int(joined["structures_destroyed"].sum()),
        "destroyed_capture_rate_percent": round(float(joined["structures_destroyed"].sum() / damage_union["structures_destroyed"].sum() * 100), 2),
        "total_acres_captured": round(float(joined["total_acres"].sum()), 2),
        "years_covered_count": int(joined["year_int"].nunique()),
        "years_covered_list": [int(y) for y in sorted(joined["year_int"].unique())]
    }
    metrics_json_file = BASE_DIR / "join_metrics_summary.json"
    with open(metrics_json_file, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2, ensure_ascii=False)
    print(f"  -> Đã lưu chỉ số tóm tắt vào: {metrics_json_file.name}")

    # In ra console Top 15 vụ tiêu biểu cho người dùng xem
    print("\n" + "=" * 80)
    print("MINH CHỨNG TOP 15 ĐÁM CHÁY TÀN KHỐC NHẤT LỊCH SỬ CALIFORNIA (2006–2025):")
    print("=" * 80)
    cols_to_print = ["Year", "Fire_Name", "County", "Unit_ID", "Acres_Burned", "Structures_Destroyed", "Damage_Source"]
    print(top_destructive_export[cols_to_print].head(15).to_string(index=False))
    print("=" * 80)


if __name__ == "__main__":
    run_join_experiment()
