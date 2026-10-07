"""
Module: src/03_clean.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Làm sạch dữ liệu Bước 1 theo quy tắc (Rule-based cleaning), mỗi dòng đầu ra = 1 vụ cháy FRAP 2006–2025.
    - Chuẩn hóa 3 khóa liên kết (docs/DATA_DICTIONARY.md mục 3):
        Khóa 1 `fire_name` (viết hoa, CMPLX -> COMPLEX, bỏ hậu tố FIRE / INCIDENT / COMPLEX),
        Khóa 2 `year` (số nguyên 2006–2025),
        Khóa 3 `unit_id` (FRAP `Unit ID` = DINS `* CAL FIRE Unit` = mã trong ICS-209 `INCIDENT_NUMBER`).
    - Chuẩn hóa ngày tháng về ISO 8601 (YYYY-MM-DD), diện tích về Hecta (giữ song song Acres).
    - Hợp nhất số công trình bị phá hủy / hư hại thành chuỗi 20 năm: ICS-209 (2006–2012) + DINS (2013–2025).
    - Loại trùng lặp, chuyển giá trị bất hợp lý (âm, thời gian dập lửa > 1 năm) thành NULL.
    - Bảo toàn cột gốc để lưu vết (vd: `fire_name_raw`).
    - Xuất tập dữ liệu trung gian: `data/interim/master_rules_cleaned.csv`.

Cách chạy (từ thư mục gốc dự án):
    python src/03_clean.py
"""

import importlib.util
import re
from pathlib import Path

import numpy as np
import pandas as pd

# Dung lai ham doc du lieu / chuan hoa ten tu 02_eda.py (ten file bat dau bang so nen khong import thuong duoc)
_spec = importlib.util.spec_from_file_location("eda", Path(__file__).parent / "02_eda.py")
eda = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eda)

OUTPUT_PATH = Path("data/interim/master_rules_cleaned.csv")
MIN_ROWS = 5000  # yeu cau cung cua barem

# Bang ma nguyen nhan CAL FIRE FRAP (metadata FRAP fire perimeters)
CAUSE_NAMES = {
    1: "Lightning", 2: "Equipment Use", 3: "Smoking", 4: "Campfire", 5: "Debris", 6: "Railroad",
    7: "Arson", 8: "Playing with Fire", 9: "Miscellaneous", 10: "Vehicle", 11: "Powerline",
    12: "Firefighter Training", 13: "Non-Firefighter Training", 14: "Unknown / Unidentified",
    15: "Structure", 16: "Aircraft", 17: "Volcanic", 18: "Escaped Prescribed Burn", 19: "Illegal Alien Campfire",
}
NATURAL_CAUSES = {1, 17}
UNDETERMINED_CAUSES = {9, 14}

# Cot de nhan dien 1 cong trinh DINS bi kiem ke lap
DINS_DUPLICATE_KEY = [
    "* Incident Name", "Incident Start Date", "* Street Number", "* Street Name", "* City",
    "* Structure Type", "Latitude", "Longitude",
]
DINS_DAMAGED_LEVELS = ["Affected (>0-10%)", "Minor (10-25%)", "Major (25-50%)"]

FIRE_KEY = ["year", "fire_name", "unit_id"]

OUTPUT_COLUMNS = [
    "incident_id", "fire_name", "fire_name_raw", "year", "alarm_date", "cont_date", "duration_days",
    "county", "county_fips", "county_population", "county_area_sqmi", "unit_id", "agency",
    "cause_code", "cause_name", "cause_group", "acres_burned", "burned_area_ha",
    "structures_destroyed", "structures_damaged", "damage_source", "damage_match", "n_polygons", "frap_global_id",
]

CLEANING_LOG: list[dict] = []


def log_step(step: str, before: int, after: int, note: str = "") -> None:
    """Ghi lai 1 buoc lam sach (de dien vao docs/CLEANING_LOG.md) va in ra man hinh."""
    CLEANING_LOG.append({"buoc": step, "truoc": before, "sau": after, "loai_bo": before - after, "ghi_chu": note})
    print(f"[TV1 - CLEAN] {step}: {before:,} -> {after:,} dong. {note}")


def log_as_markdown() -> str:
    """Xuat CLEANING_LOG thanh bang Markdown (khong can thu vien tabulate)."""
    header = "| Buoc | So dong truoc | So dong sau | So dong loai bo | Ghi chu |\n|---|---|---|---|---|"
    rows = [f"| {r['buoc']} | {r['truoc']:,} | {r['sau']:,} | {r['loai_bo']:,} | {r['ghi_chu']} |" for r in CLEANING_LOG]
    return "\n".join([header, *rows])


# ---------------------------------------------------------------------------
# Buoc 1: FRAP - bang vu chay chinh
# ---------------------------------------------------------------------------

def clean_frap(frap: pd.DataFrame) -> pd.DataFrame:
    """Loc 2006-2025, chuan hoa khoa / ngay / dien tich / nguyen nhan, gop nhieu polygon thanh 1 vu chay."""
    n_raw = len(frap)
    df = frap[frap["Year"].between(*eda.STUDY_YEARS)].copy()
    log_step("1. Loc nam 2006-2025 (FRAP)", n_raw, len(df), "Bo vu truoc 2006 va 77 dong thieu Year")

    df = pd.DataFrame({
        "year": df["Year"].astype(int),
        "fire_name_raw": df["Fire Name"],
        "fire_name": eda.normalize_fire_name(df["Fire Name"]),
        "unit_id": df["Unit ID"].str.strip().str.upper(),
        "agency": df["Agency"],
        "alarm_date": pd.to_datetime(df["Alarm Date"], format=eda.DATE_FORMAT, errors="coerce"),
        "cont_date": pd.to_datetime(df["Containment Date"], format=eda.DATE_FORMAT, errors="coerce"),
        "cause_code": df["Cause"].astype("Int64"),
        "acres_burned": df["GIS Calculated Acres"],
        "objectid": df["OBJECTID"],
        "frap_global_id": df["GlobalID"],
    })

    # Vu khong ten: khoa gop rieng theo OBJECTID de khong bi gop chung voi nhau
    unnamed = df["fire_name"].isna()
    df["_group_name"] = df["fire_name"].fillna("_UNNAMED_" + df["objectid"].astype(str))
    df["fire_name"] = df["fire_name"].fillna("UNNAMED")

    # Gop polygon: (nam, ten, don vi). Thuoc tinh dang chu lay theo polygon lon nhat
    n_before = len(df)
    df = df.sort_values("acres_burned", ascending=False)
    fires = df.groupby(["year", "_group_name", "unit_id"], dropna=False, sort=False).agg(
        fire_name=("fire_name", "first"),
        fire_name_raw=("fire_name_raw", "first"),
        agency=("agency", "first"),
        cause_code=("cause_code", "first"),
        frap_global_id=("frap_global_id", "first"),
        alarm_date=("alarm_date", "min"),
        cont_date=("cont_date", "max"),
        acres_burned=("acres_burned", "sum"),
        n_polygons=("objectid", "size"),
    ).reset_index().drop(columns="_group_name")
    log_step("3. Gop polygon trung lap logic (FRAP)", n_before, len(fires),
             f"Khoa (year, fire_name, unit_id); {int(unnamed.sum())} vu khong ten giu rieng")

    # Quy doi don vi, giu song song acres va ha
    fires["burned_area_ha"] = fires["acres_burned"] * eda.ACRE_TO_HA

    # Thoi gian dap lua: < 0 hoac > 1 nam coi la loi nhap lieu -> NULL
    days = (fires["cont_date"] - fires["alarm_date"]).dt.days
    invalid = days.notna() & ~days.between(0, eda.MAX_CONTAINMENT_DAYS)
    fires["duration_days"] = days.where(~invalid).astype(float)
    fires.loc[invalid, "cont_date"] = pd.NaT
    log_step("8a. Thoi gian dap lua bat hop ly -> NULL", len(fires), len(fires),
             f"{int(invalid.sum())} vu co cont_date < alarm_date hoac > {eda.MAX_CONTAINMENT_DAYS} ngay")

    fires["cause_name"] = fires["cause_code"].map(CAUSE_NAMES)
    fires["cause_group"] = np.select(
        [fires["cause_code"].isin(NATURAL_CAUSES), fires["cause_code"].isin(UNDETERMINED_CAUSES) | fires["cause_code"].isna()],
        ["Natural", "Undetermined"], default="Human",
    )
    return fires


# ---------------------------------------------------------------------------
# Buoc 2-3: thiet hai cong trinh DINS + ICS-209
# ---------------------------------------------------------------------------

def clean_dins(dins: pd.DataFrame) -> pd.DataFrame:
    """Bo kiem ke lap, dem cong trinh bi pha huy / hu hai theo (year, fire_name, unit_id)."""
    n_raw = len(dins)
    dins = dins.drop_duplicates(subset=DINS_DUPLICATE_KEY)
    log_step("3b. Khu trung lap logic (DINS)", n_raw, len(dins), "Cung vu chay, dia chi, loai cong trinh va toa do")

    df = pd.DataFrame({
        "year": pd.to_datetime(dins["Incident Start Date"], format=eda.DATE_FORMAT).dt.year,
        "fire_name": eda.normalize_fire_name(dins["* Incident Name"]),
        "unit_id": dins["* CAL FIRE Unit"].str.strip().str.upper(),
        "county": dins["County"].str.strip(),
        "destroyed": dins["* Damage"].eq("Destroyed (>50%)"),
        "damaged": dins["* Damage"].isin(DINS_DAMAGED_LEVELS),
    })
    return df.groupby(FIRE_KEY, as_index=False).agg(
        structures_destroyed=("destroyed", "sum"),
        structures_damaged=("damaged", "sum"),
        county=("county", lambda s: s.mode().iat[0] if s.notna().any() else np.nan),
    ).assign(damage_source="CAL_FIRE_DINS")


def parse_ics_county(value, county_names: list[str]):
    """POO_COUNTY rat lon xon ('Teh,Sha,Sisk,Trinity', 'Kern County', 'Mendo.') -> ten Hat dau tien hop le."""
    if pd.isna(value):
        return np.nan
    first = re.split(r",|/|&|\band\b| - ", str(value), flags=re.IGNORECASE)[0]
    token = first.lower().replace("county", "").replace(".", "").replace(" ", "").strip()
    if len(token) < 3:
        return np.nan
    # Khop theo tien to cua ten Hat (vd 'teh' -> Tehama, 'eldorado' -> El Dorado); chi nhan khi khop duy nhat
    matches = [c for c in county_names if c.lower().replace(" ", "").startswith(token)]
    return matches[0] if len(matches) == 1 else np.nan


def clean_ics209(ics: pd.DataFrame, county_names: list[str]) -> pd.DataFrame:
    """Lay so cong trinh bi pha huy / hu hai 2006-2012; ma don vi tach tu INCIDENT_NUMBER (vd CA-RRU-062485)."""
    df = pd.DataFrame({
        "year": ics["START_YEAR"].astype(int),
        "fire_name": eda.normalize_fire_name(ics["INCIDENT_NAME"]),
        "unit_id": ics["INCIDENT_NUMBER"].str.extract(r"^CA-?([A-Z]{3})", expand=False),
        "county": ics["POO_COUNTY"].apply(parse_ics_county, county_names=county_names),
        "structures_destroyed": ics["STR_DESTROYED_TOTAL"].fillna(0),
        "structures_damaged": ics["STR_DAMAGED_TOTAL"].fillna(0),
    })
    # Giu vu co thiet hai; 1 vu co the co nhieu ban bao cao -> cong lai
    df = df[(df["structures_destroyed"] > 0) | (df["structures_damaged"] > 0)]
    return df.groupby(FIRE_KEY, as_index=False, dropna=False).agg(
        structures_destroyed=("structures_destroyed", "sum"),
        structures_damaged=("structures_damaged", "sum"),
        county=("county", "first"),
    ).assign(damage_source="USDA_ICS_209")


# ---------------------------------------------------------------------------
# Buoc 4-5: ghep thiet hai + Hat vao bang vu chay
# ---------------------------------------------------------------------------

def attach_damage(fires: pd.DataFrame, damage: pd.DataFrame) -> pd.DataFrame:
    """Ghep thiet hai vao vu chay: khop du 3 khoa truoc, sau do khop (year, fire_name) -> vu lon nhat cung ten."""
    fires = fires.reset_index(drop=True)
    fires["_fire_idx"] = fires.index

    # Vu khong ten (fire_name = UNNAMED) khong the doi chieu theo ten -> loai khoi ca 2 lan khop
    named = fires[fires["fire_name"] != "UNNAMED"]

    # Lan 1: khop chinh xac (year, fire_name, unit_id)
    exact = damage.merge(named[[*FIRE_KEY, "_fire_idx"]], on=FIRE_KEY, how="left", validate="m:1")
    exact["damage_match"] = np.where(exact["_fire_idx"].notna(), "exact", None)

    # Lan 2: dong chua khop (thuong do nguon ghi ma don vi khac) -> vu lon nhat cung (year, fire_name).
    # Neu ten la duy nhat trong nam thi gan chac chan; neu nhieu vu trung ten thi co the gan nham -> danh dau rieng
    largest = (
        named.sort_values("acres_burned", ascending=False)
        .groupby(["year", "fire_name"], as_index=False)
        .agg(_fire_idx=("_fire_idx", "first"), _n_same_name=("_fire_idx", "size"))
    )
    unmatched = exact["_fire_idx"].isna()
    fallback = exact.loc[unmatched, ["year", "fire_name"]].merge(largest, on=["year", "fire_name"], how="left")
    exact.loc[unmatched, "_fire_idx"] = fallback["_fire_idx"].to_numpy()
    exact.loc[unmatched, "damage_match"] = np.select(
        [fallback["_n_same_name"].eq(1), fallback["_n_same_name"].gt(1)],
        ["name_year_unique", "name_year_largest"], default=None,
    )

    matched = exact["_fire_idx"].notna()
    total = damage["structures_destroyed"].sum()
    got = exact.loc[matched, "structures_destroyed"].sum()
    by_method = exact[matched].groupby("damage_match")["structures_destroyed"].agg(["size", "sum"])
    method_note = ", ".join(f"{m}: {int(r['size'])} vu / {r['sum']:,.0f} cong trinh" for m, r in by_method.iterrows())
    log_step("7. Hop nhat thiet hai 20 nam (ICS-209 + DINS)", len(damage), int(matched.sum()),
             f"Khop {got:,.0f} / {total:,.0f} cong trinh bi pha huy ({got / total:.1%}) [{method_note}]; "
             f"{int((~matched).sum())} vu thiet hai khong tim thay trong FRAP")
    top_unmatched = exact[~matched].nlargest(10, "structures_destroyed")
    print("[TV1 - CLEAN] 10 vu thiet hai lon nhat chua khop (ghi vao CLEANING_LOG):")
    print(top_unmatched[[*FIRE_KEY, "structures_destroyed", "damage_source"]].to_string(index=False))

    per_fire = exact[matched].groupby("_fire_idx").agg(
        structures_destroyed=("structures_destroyed", "sum"),
        structures_damaged=("structures_damaged", "sum"),
        damage_source=("damage_source", "first"),
        damage_match=("damage_match", "first"),
        county=("county", "first"),
    )
    fires = fires.join(per_fire, on="_fire_idx").drop(columns="_fire_idx")
    fires[["structures_destroyed", "structures_damaged"]] = fires[["structures_destroyed", "structures_damaged"]].fillna(0)
    fires["damage_source"] = fires["damage_source"].fillna("NONE")
    fires["damage_match"] = fires["damage_match"].fillna("none")
    return fires


def attach_county(fires: pd.DataFrame, damage: pd.DataFrame, demographics: pd.DataFrame) -> pd.DataFrame:
    """Hat lay tu nguon thiet hai; vu con thieu -> Hat pho bien nhat cua don vi (unit_id). Ghep dien tich / FIPS."""
    unit_to_county = damage.dropna(subset=["unit_id", "county"]).groupby("unit_id")["county"].agg(lambda s: s.mode().iat[0])
    before_missing = int(fires["county"].isna().sum())
    fires["county"] = fires["county"].fillna(fires["unit_id"].map(unit_to_county))
    log_step("4. Chuan hoa Hat (county)", len(fires), len(fires),
             f"{before_missing - int(fires['county'].isna().sum()):,} vu suy Hat tu unit_id; "
             f"con {int(fires['county'].isna().sum()):,} vu khong xac dinh duoc Hat")

    counties = pd.DataFrame({
        "county": demographics["CDT_NAME_SHORT"],
        "county_fips": demographics["CENSUS_GEOID"].astype(int).astype(str).str.zfill(5),
        "county_population": demographics["CENSUS_POPULATION"],  # trong 100% o file goc -> NULL, xem DATA_QUALITY_REPORT
        "county_area_sqmi": demographics["AREA_SQMI"],
    })
    return fires.merge(counties, on="county", how="left", validate="m:1")


# ---------------------------------------------------------------------------
# Kiem tra quy tac + xuat file
# ---------------------------------------------------------------------------

def apply_rule_checks(fires: pd.DataFrame) -> pd.DataFrame:
    """Gia tri am bat hop ly -> NULL (khong xoa dong)."""
    cols = ["acres_burned", "burned_area_ha", "structures_destroyed", "structures_damaged"]
    negative = fires[cols] < 0
    fires[cols] = fires[cols].mask(negative)
    log_step("8b. Gia tri am bat hop ly -> NULL", len(fires), len(fires),
             f"{int(negative.to_numpy().sum())} o am trong {', '.join(cols)}")
    log_step("5. Chuan hoa toa do (bounding box)", len(fires), len(fires),
             "N/A: FRAP khong co cot lat/lon; toa do DINS / ICS-209 deu nam trong California (xem DATA_QUALITY_REPORT)")
    return fires


def finalize(fires: pd.DataFrame) -> pd.DataFrame:
    """Tao incident_id, ep kieu, sap xep cot theo DATA_DICTIONARY va kiem tra rang buoc."""
    fires = fires.sort_values(["year", "alarm_date", "fire_name", "unit_id"], na_position="last").reset_index(drop=True)
    fires["incident_id"] = "CALFIRE-" + fires["year"].astype(str) + "-" + fires.groupby("year").cumcount().add(1).astype(str).str.zfill(5)
    fires[["structures_destroyed", "structures_damaged"]] = fires[["structures_destroyed", "structures_damaged"]].astype(int)
    fires = fires[OUTPUT_COLUMNS]

    assert len(fires) >= MIN_ROWS, f"Chi con {len(fires)} dong, duoi muc toi thieu {MIN_ROWS}"
    assert fires["incident_id"].is_unique
    assert fires["year"].between(*eda.STUDY_YEARS).all()
    assert (fires["burned_area_ha"].dropna() >= 0).all()
    return fires


def clean_by_rules() -> pd.DataFrame:
    """Thuc hien lam sach theo quy tac tu data/raw/calfire sang data/interim/master_rules_cleaned.csv."""
    CLEANING_LOG.clear()
    print("[TV1 - CLEAN] Bat dau lam sach du lieu theo quy tac...")
    raw = eda.load_raw_data()
    log_step("0. Nap du lieu tho", sum(len(df) for df in raw.values()), sum(len(df) for df in raw.values()),
             f"{len(raw)} file tu {eda.RAW_DIR}")

    county_names = raw["demographics"]["CDT_NAME_SHORT"].tolist()
    fires = clean_frap(raw["perimeters"])
    damage = pd.concat([clean_ics209(raw["ics209"], county_names), clean_dins(raw["dins"])], ignore_index=True)

    fires = attach_damage(fires, damage)
    fires = attach_county(fires, damage, raw["demographics"])
    fires = apply_rule_checks(fires)
    fires = finalize(fires)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fires.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"[TV1 - CLEAN] Da xuat {len(fires):,} vu chay x {fires.shape[1]} cot -> {OUTPUT_PATH}")
    print("\n[TV1 - CLEAN] Bang nhat ky (dan vao docs/CLEANING_LOG.md):")
    print(log_as_markdown())
    return fires


if __name__ == "__main__":
    clean_by_rules()  # UTF-8 cho console da duoc cau hinh khi nap 02_eda.py
