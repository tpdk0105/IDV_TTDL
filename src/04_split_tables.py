
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Dân số chính thức 58 Hạt California theo US Census Bureau 2020 
CALIFORNIA_POPULATION_2020 = {
    "Alameda": 1682353, "Alpine": 1204, "Amador": 40474, "Butte": 211632,
    "Calaveras": 45292, "Colusa": 21839, "Contra Costa": 1165927, "Del Norte": 27743,
    "El Dorado": 191185, "Fresno": 1008654, "Glenn": 28917, "Humboldt": 136463,
    "Imperial": 179702, "Inyo": 19016, "Kern": 909235, "Kings": 152486,
    "Lake": 68163, "Lassen": 32730, "Los Angeles": 10014009, "Madera": 156255,
    "Marin": 262321, "Mariposa": 17131, "Mendocino": 91601, "Merced": 281202,
    "Modoc": 8700, "Mono": 13195, "Monterey": 439035, "Napa": 138019,
    "Nevada": 102241, "Orange": 3186989, "Placer": 404739, "Plumas": 19790,
    "Riverside": 2418185, "Sacramento": 1585055, "San Benito": 64209, "San Bernardino": 2181654,
    "San Diego": 3298634, "San Francisco": 873965, "San Joaquin": 779233, "San Luis Obispo": 282424,
    "San Mateo": 764442, "Santa Barbara": 448229, "Santa Clara": 1936259, "Santa Cruz": 270861,
    "Shasta": 182155, "Sierra": 3236, "Siskiyou": 44076, "Solano": 453491,
    "Sonoma": 488863, "Stanislaus": 552878, "Sutter": 99633, "Tehama": 65829,
    "Trinity": 16112, "Tulare": 473117, "Tuolumne": 55625, "Ventura": 843843,
    "Yolo": 216403, "Yuba": 81575
}

# Bảng mã nguyên nhân CAL FIRE FRAP (1-19)
CAUSE_DATA = [
    (1, 1, "Lightning", "Natural"),
    (2, 2, "Equipment Use", "Human"),
    (3, 3, "Smoking", "Human"),
    (4, 4, "Campfire", "Human"),
    (5, 5, "Debris", "Human"),
    (6, 6, "Railroad", "Human"),
    (7, 7, "Arson", "Human"),
    (8, 8, "Playing with Fire", "Human"),
    (9, 9, "Miscellaneous", "Undetermined"),
    (10, 10, "Vehicle", "Human"),
    (11, 11, "Powerline", "Human"),
    (12, 12, "Firefighter Training", "Human"),
    (13, 13, "Non-Firefighter Training", "Human"),
    (14, 14, "Unknown / Unidentified", "Undetermined"),
    (15, 15, "Structure", "Human"),
    (16, 16, "Aircraft", "Human"),
    (17, 17, "Volcanic", "Natural"),
    (18, 18, "Escaped Prescribed Burn", "Human"),
    (19, 19, "Illegal Alien Campfire", "Human"),
]


def build_dim_date() -> pd.DataFrame:
    start_date = date(2006, 1, 1)
    end_date = date(2025, 12, 31)
    delta = timedelta(days=1)

    records = []
    curr = start_date
    while curr <= end_date:
        d_id = curr.year * 10000 + curr.month * 100 + curr.day
        month = curr.month
        quarter = (month - 1) // 3 + 1
        month_name = curr.strftime("%b")
        if month in [3, 4, 5]:
            season = "Spring"
        elif month in [6, 7, 8]:
            season = "Summer"
        elif month in [9, 10, 11]:
            season = "Autumn"
        else:
            season = "Winter"
        is_fire_season = 1 if month in [6, 7, 8, 9, 10] else 0

        records.append({
            "date_id": d_id,
            "full_date": curr.strftime("%Y-%m-%d"),
            "year": curr.year,
            "quarter": quarter,
            "month": month,
            "month_name": month_name,
            "season": season,
            "is_fire_season": is_fire_season,
        })
        curr += delta

    df = pd.DataFrame(records)
    print(f"[TV2 - MODEL] Đã tạo dim_date: {len(df):,} ngày (2006–2025).")
    return df


def build_dim_county(raw_demographics_path: Path) -> pd.DataFrame:
    demo = pd.read_csv(raw_demographics_path)
    counties = []
    for idx, row in demo.iterrows():
        c_name = str(row["CDT_NAME_SHORT"]).strip()
        fips = str(int(row["CENSUS_GEOID"])).zfill(5) if pd.notna(row["CENSUS_GEOID"]) else None
        area = float(row["AREA_SQMI"]) if pd.notna(row["AREA_SQMI"]) else None
        abbr = str(row["CDT_COUNTY_ABBR"]).strip() if pd.notna(row["CDT_COUNTY_ABBR"]) else None
        pop = CALIFORNIA_POPULATION_2020.get(c_name, None)
        counties.append({
            "county_id": idx + 1,
            "county_name": c_name,
            "county_fips": fips,
            "census_population": pop,
            "area_sqmi": area,
            "cdt_abbr": abbr,
        })

    # Bản ghi dự phòng cho các vụ cháy chưa xác định được Hạt (tránh lỗi khóa ngoại mồ côi)
    counties.append({
        "county_id": 59,
        "county_name": "Unknown",
        "county_fips": "06000",
        "census_population": None,
        "area_sqmi": None,
        "cdt_abbr": "UNK",
    })

    df = pd.DataFrame(counties)
    print(f"[TV2 - MODEL] Đã tạo dim_county: {len(df):,} bản ghi (58 Hạt California + 1 Unknown).")
    return df


def build_dim_cause() -> pd.DataFrame:
    df = pd.DataFrame(CAUSE_DATA, columns=["cause_id", "cause_code", "cause_name", "cause_group"])
    print(f"[TV2 - MODEL] Đã tạo dim_cause: {len(df):,} nguyên nhân.")
    return df


def match_noaa_casualties(fires: pd.DataFrame, noaa_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not noaa_path.exists():
        raise FileNotFoundError(f"Không tìm thấy {noaa_path}! Hãy chạy src/03_clean.py trước.")
    events = pd.read_csv(noaa_path, parse_dates=["begin_date"])

    # incident_id = chỉ số dòng + 1 (giống cách đánh khóa fact_fire_incident bên dưới)
    named = fires[fires["fire_name"] != "UNNAMED"]
    largest = (
        named.assign(incident_id=named.index + 1)
        .sort_values("acres_burned", ascending=False)
        .drop_duplicates(["year", "fire_name"])[["year", "fire_name", "incident_id"]]
    )
    events = events.merge(largest, on=["year", "fire_name"], how="left", validate="m:1")
    events["incident_id"] = events["incident_id"].astype("Int64")

    per_fire = events.dropna(subset=["incident_id"]).groupby("incident_id")[["deaths_direct", "injuries_direct"]].sum()
    fires["deaths_direct"] = (fires.index + 1).map(per_fire["deaths_direct"]).fillna(0).astype(int)
    fires["injuries_direct"] = (fires.index + 1).map(per_fire["injuries_direct"]).fillna(0).astype(int)

    matched = events["incident_id"].notna()
    print(f"[TV2 - MODEL] Đã đối soát NOAA: {int(matched.sum())}/{len(events)} sự kiện khớp vụ cháy FRAP, "
          f"{int(events.loc[matched, 'deaths_direct'].sum())}/{int(events['deaths_direct'].sum())} người chết trực tiếp.")
    return fires, events


def build_fact_casualty_event(events: pd.DataFrame) -> pd.DataFrame:
    df = events.reset_index(drop=True)
    return pd.DataFrame({
        "casualty_id": df.index + 1,
        "noaa_event_id": df["noaa_event_id"],
        "episode_id": df["episode_id"],
        "date_id": df["begin_date"].dt.strftime("%Y%m%d").astype(int),
        "incident_id": df["incident_id"],
        "fire_name": df["fire_name"],
        "zone_names": df["zone_names"],
        "n_zones": df["n_zones"],
        "deaths_direct": df["deaths_direct"],
        "deaths_indirect": df["deaths_indirect"],
        "injuries_direct": df["injuries_direct"],
        "injuries_indirect": df["injuries_indirect"],
    })


def build_casualties_by_year(events: pd.DataFrame) -> pd.DataFrame:
    years = pd.Index(range(2006, 2026), name="year")
    yearly = events.groupby("year").agg(
        noaa_fire_events=("noaa_event_id", "size"),
        deaths_direct=("deaths_direct", "sum"),
        deaths_indirect=("deaths_indirect", "sum"),
        injuries_direct=("injuries_direct", "sum"),
        injuries_indirect=("injuries_indirect", "sum"),
    ).reindex(years, fill_value=0)
    yearly.insert(3, "deaths_total", yearly["deaths_direct"] + yearly["deaths_indirect"])
    yearly["injuries_total"] = yearly["injuries_direct"] + yearly["injuries_indirect"]

    # Vụ cháy làm chết nhiều người nhất trong năm; bỏ trống nếu năm đó không có người chết trực tiếp
    deadliest = (
        events[events["deaths_direct"] > 0]
        .sort_values("deaths_direct", ascending=False)
        .drop_duplicates("year")
        .set_index("year")
    )
    # NOAA không ghi tên vụ cháy (vd Redwood Valley 2017)
    unnamed = "(không rõ tên) " + deadliest["zone_names"].str.title()
    yearly["deadliest_fire"] = deadliest["fire_name"].str.title().fillna(unnamed)
    yearly["deadliest_fire_deaths"] = deadliest["deaths_direct"].astype("Int64")
    yearly["deaths_share_of_period"] = (yearly["deaths_direct"] / yearly["deaths_direct"].sum()).round(4)
    return yearly.reset_index()


def extract_fire_coordinates(dins_path: Path, ics_path: Path) -> dict:
    coords = {}
    if dins_path.exists():
        dins = pd.read_csv(dins_path, usecols=["* Incident Name", "Incident Start Date", "Latitude", "Longitude"])
        dins = dins.dropna(subset=["Latitude", "Longitude"])
        dins = dins[dins["Latitude"].between(32.0, 42.0) & dins["Longitude"].between(-125.0, -114.0)]
        dins["year"] = pd.to_datetime(dins["Incident Start Date"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce").dt.year
        dins["norm_name"] = dins["* Incident Name"].str.upper().str.strip()
        agg = dins.groupby(["year", "norm_name"]).agg(lat=("Latitude", "median"), lon=("Longitude", "median")).reset_index()
        for _, r in agg.iterrows():
            coords[(int(r["year"]), r["norm_name"])] = (round(float(r["lat"]), 5), round(float(r["lon"]), 5))

    if ics_path.exists():
        ics = pd.read_csv(ics_path, usecols=["START_YEAR", "INCIDENT_NAME", "POO_LATITUDE", "POO_LONGITUDE"])
        ics = ics.dropna(subset=["POO_LATITUDE", "POO_LONGITUDE"])
        ics = ics[ics["POO_LATITUDE"].between(32.0, 42.0) & ics["POO_LONGITUDE"].between(-125.0, -114.0)]
        ics["norm_name"] = ics["INCIDENT_NAME"].str.upper().str.strip()
        for _, r in ics.iterrows():
            key = (int(r["START_YEAR"]), r["norm_name"])
            if key not in coords:
                coords[key] = (round(float(r["POO_LATITUDE"]), 5), round(float(r["POO_LONGITUDE"]), 5))

    return coords


def split_star_schema_tables() -> None:
    tables_dir = Path("data/tables")
    tables_dir.mkdir(parents=True, exist_ok=True)

    clean_file = Path("data/clean/master_clean.csv")
    if not clean_file.exists():
        clean_file = Path("data/interim/master_rules_cleaned.csv")
    if not clean_file.exists():
        raise FileNotFoundError("Không tìm thấy tệp dữ liệu đã làm sạch master_clean.csv hoặc master_rules_cleaned.csv!")

    print(f"[TV2 - MODEL] Nạp dữ liệu làm sạch từ: {clean_file.resolve()}")
    df = pd.read_csv(clean_file)

    raw_dir = Path("data/raw/calfire")
    dim_date = build_dim_date()
    dim_county = build_dim_county(raw_dir / "California_Counties_Demographics.csv")
    dim_cause = build_dim_cause()

    county_map = dict(zip(dim_county["county_name"], dim_county["county_id"]))
    cause_map = dict(zip(dim_cause["cause_code"], dim_cause["cause_id"]))

    df, noaa_events = match_noaa_casualties(df, Path("data/interim/noaa_casualties_cleaned.csv"))
    fire_coords = extract_fire_coordinates(
        raw_dir / "CAL_FIRE_Damage_Inspection_DINS.csv",
        raw_dir / "ICS209_California_Wildfires_2006_2012.csv"
    )

    fact_fires = []
    fire_id_map = {}  # Map (year, fire_name) -> integer incident_id

    for idx, row in df.iterrows():
        inc_id = idx + 1
        year = int(row["year"])
        f_name = str(row["fire_name"])
        fire_id_map[(year, f_name)] = inc_id

        # Khóa ngoại Date
        if pd.notna(row.get("alarm_date")):
            dt = pd.to_datetime(row["alarm_date"])
            d_id = dt.year * 10000 + dt.month * 100 + dt.day
        else:
            d_id = year * 10000 + 701  # Mặc định ngày 1 tháng 7 nếu thiếu alarm_date

        # Khóa ngoại County
        c_name = str(row.get("county", "")).strip()
        c_id = county_map.get(c_name, 59)  # 59 = Unknown nếu không tìm thấy

        # Khóa ngoại Cause
        ccode = int(row["cause_code"]) if pd.notna(row.get("cause_code")) else 14
        cau_id = cause_map.get(ccode, 14)  # 14 = Unknown

        # Tọa độ
        coord = fire_coords.get((year, f_name))
        lat, lon = coord if coord else (None, None)

        fact_fires.append({
            "incident_id": inc_id,
            "fire_name": f_name,
            "frap_fire_num": str(row.get("incident_id", f"CALFIRE-{year}-{inc_id:05d}")),
            "date_id": d_id,
            "county_id": c_id,
            "cause_id": cau_id,
            "acres_burned": round(float(row["acres_burned"]), 2) if pd.notna(row.get("acres_burned")) else 0.0,
            "burned_area_ha": round(float(row["burned_area_ha"]), 2) if pd.notna(row.get("burned_area_ha")) else 0.0,
            "duration_days": round(float(row["duration_days"]), 2) if pd.notna(row.get("duration_days")) else None,
            "latitude": lat,
            "longitude": lon,
            "total_structures_destroyed": int(row.get("structures_destroyed", 0)),
            "total_structures_damaged": int(row.get("structures_damaged", 0)),
            "deaths_direct": int(row.get("deaths_direct", 0)),
            "injuries_direct": int(row.get("injuries_direct", 0)),
            "is_outlier_ml": int(row.get("is_outlier_ml", 0)),
            "outlier_score": round(float(row.get("outlier_score", 0.0)), 4) if pd.notna(row.get("outlier_score")) else None,
            "burned_area_is_imputed": int(row.get("burned_area_is_imputed", 0)),
            "cause_is_predicted": int(row.get("cause_is_predicted", 0)),
        })

    df_fact_fires = pd.DataFrame(fact_fires)
    assert len(df_fact_fires) >= 5000, f"Bảng fact_fire_incident chỉ có {len(df_fact_fires)} dòng, dưới mức tối thiểu 5000!"

    fact_damage = []
    record_id = 1

    dins_path = raw_dir / "CAL_FIRE_Damage_Inspection_DINS.csv"
    if dins_path.exists():
        dins = pd.read_csv(dins_path, usecols=[
            "GLOBALID", "* Incident Name", "Incident Start Date", "County",
            "* Structure Type", "* Damage", "Latitude", "Longitude"
        ])
        dins["year"] = pd.to_datetime(dins["Incident Start Date"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce").dt.year
        dins["norm_name"] = dins["* Incident Name"].str.upper().str.strip()

        for _, row in dins.iterrows():
            yr = row["year"]
            fname = row["norm_name"]
            if pd.isna(yr) or pd.isna(fname):
                continue
            f_id = fire_id_map.get((int(yr), fname))
            if not f_id:
                continue

            c_name = str(row.get("County", "")).strip()
            c_id = county_map.get(c_name, 59)
            dmg_cat = str(row.get("* Damage", "Unknown"))
            is_destroyed = 1 if "Destroyed" in dmg_cat else 0
            is_damaged = 1 if any(w in dmg_cat for w in ["Major", "Minor", "Affected"]) else 0
            lat = float(row["Latitude"]) if pd.notna(row.get("Latitude")) and 32.0 <= float(row["Latitude"]) <= 42.0 else None
            lon = float(row["Longitude"]) if pd.notna(row.get("Longitude")) and -125.0 <= float(row["Longitude"]) <= -114.0 else None

            fact_damage.append({
                "record_id": record_id,
                "global_id": str(row.get("GLOBALID", f"DINS-{record_id:06d}")),
                "incident_id": f_id,
                "county_id": c_id,
                "damage_source": "CAL_FIRE_DINS",
                "structure_type": str(row.get("* Structure Type", "Unspecified")),
                "damage_category": dmg_cat,
                "structures_destroyed": is_destroyed,
                "structures_damaged": is_damaged,
                "latitude": lat,
                "longitude": lon,
            })
            record_id += 1

    ics_path = raw_dir / "ICS209_California_Wildfires_2006_2012.csv"
    if ics_path.exists():
        ics = pd.read_csv(ics_path, usecols=[
            "INCIDENT_ID", "INCIDENT_NAME", "START_YEAR", "POO_COUNTY",
            "STR_DESTROYED_TOTAL", "STR_DAMAGED_TOTAL", "POO_LATITUDE", "POO_LONGITUDE"
        ])
        ics = ics[(ics["STR_DESTROYED_TOTAL"] > 0) | (ics["STR_DAMAGED_TOTAL"] > 0)]
        ics["norm_name"] = ics["INCIDENT_NAME"].str.upper().str.strip()

        for _, row in ics.iterrows():
            yr = int(row["START_YEAR"])
            fname = row["norm_name"]
            f_id = fire_id_map.get((yr, fname))
            if not f_id:
                continue

            c_name = str(row.get("POO_COUNTY", "")).strip()
            c_id = county_map.get(c_name, 59)
            lat = float(row["POO_LATITUDE"]) if pd.notna(row.get("POO_LATITUDE")) and 32.0 <= float(row["POO_LATITUDE"]) <= 42.0 else None
            lon = float(row["POO_LONGITUDE"]) if pd.notna(row.get("POO_LONGITUDE")) and -125.0 <= float(row["POO_LONGITUDE"]) <= -114.0 else None

            fact_damage.append({
                "record_id": record_id,
                "global_id": str(row.get("INCIDENT_ID", f"ICS-{record_id:06d}")),
                "incident_id": f_id,
                "county_id": c_id,
                "damage_source": "USDA_ICS_209",
                "structure_type": "Unspecified",
                "damage_category": "Destroyed (>50%)",
                "structures_destroyed": int(row.get("STR_DESTROYED_TOTAL", 0)),
                "structures_damaged": int(row.get("STR_DAMAGED_TOTAL", 0)),
                "latitude": lat,
                "longitude": lon,
            })
            record_id += 1

    df_fact_damage = pd.DataFrame(fact_damage)
    df_fact_casualty = build_fact_casualty_event(noaa_events)

    def safe_to_csv(df: pd.DataFrame, target_path: Path, encoding: str = "utf-8"):
        try:
            df.to_csv(target_path, index=False, encoding=encoding)
        except PermissionError:
            print(f"  [CẢNH BÁO] Không thể ghi đè {target_path.name} do tệp đang được mở trong ứng dụng khác. Giữ nguyên tệp hiện có.")

    safe_to_csv(dim_date, tables_dir / "dim_date.csv")
    safe_to_csv(dim_county, tables_dir / "dim_county.csv")
    safe_to_csv(dim_cause, tables_dir / "dim_cause.csv")
    safe_to_csv(df_fact_fires, tables_dir / "fact_fire_incident.csv")
    safe_to_csv(df_fact_damage, tables_dir / "fact_structure_damage.csv")
    safe_to_csv(df_fact_casualty, tables_dir / "fact_casualty_event.csv")

    print(f"[TV2 - MODEL] Xuất thành công 6 bảng Star Schema vào: {tables_dir.resolve()}")
    print(f"  - dim_date: {len(dim_date):,} dòng")
    print(f"  - dim_county: {len(dim_county):,} dòng")
    print(f"  - dim_cause: {len(dim_cause):,} dòng")
    print(f"  - fact_fire_incident: {len(df_fact_fires):,} dòng (ĐẠT YÊU CẦU >= 5.000 DÒNG)")
    print(f"  - fact_structure_damage: {len(df_fact_damage):,} dòng")
    print(f"  - fact_casualty_event: {len(df_fact_casualty):,} dòng")

    casualties_by_year = build_casualties_by_year(noaa_events)
    casualties_path = Path("data/clean/casualties_by_year.csv")
    casualties_path.parent.mkdir(parents=True, exist_ok=True)
    safe_to_csv(casualties_by_year, casualties_path, encoding="utf-8-sig")  
    print(f"[TV2 - MODEL] Xuất thương vong theo năm: {casualties_path} ({len(casualties_by_year)} năm, "
          f"{int(casualties_by_year['deaths_direct'].sum())} người chết trực tiếp)")


if __name__ == "__main__":
    split_star_schema_tables()
