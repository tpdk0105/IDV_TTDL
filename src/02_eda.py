"""
Module: src/02_eda.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Thực hiện phân tích khám phá dữ liệu ban đầu (EDA) trên 5 tập dữ liệu thô trong `data/raw/calfire/`.
    - Sử dụng các thư viện biểu đồ tĩnh (Matplotlib, Seaborn) vẽ 6 biểu đồ tĩnh theo đúng barem IDV:
        1. Tỷ lệ dữ liệu khuyết thiếu theo cột của cả 5 tập (Missing values bar).
        2. Phân phối diện tích cháy trên thang log (Histogram + KDE: burned_area_ha).
        3. Biểu đồ hộp phát hiện ngoại lai sơ bộ (Boxplot: structures_destroyed, ICS-209 + DINS).
        4. Bản đồ nhiệt tương quan (Pearson trên log1p / Spearman): năm, diện tích cháy, số ngày dập lửa, công trình bị phá hủy.
        5. Xu hướng theo năm: số vụ cháy, tổng diện tích cháy, công trình bị phá hủy (chuỗi 20/20 năm ICS-209 + DINS).
        6. Thiệt hại về người theo năm (NOAA): người chết / bị thương trực tiếp, tách phần bị đếm trùng giữa các vùng dự báo.
    - NOAA chỉ dùng cho thiệt hại về người; thiệt hại tài sản lấy từ DINS + ICS-209.
    - Xuất các biểu đồ tĩnh sang thư mục `reports/figures/` và lập báo cáo `docs/DATA_QUALITY_REPORT.md`.

Cách chạy (từ thư mục gốc dự án):
    python src/02_eda.py

Trạng thái: Đã hoàn thành đủ 6 biểu đồ.
"""

import math
import sys
from pathlib import Path

# Dam bao UTF-8 tren Windows console (Jupyter khong co reconfigure nen phai kiem tra truoc)
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import seaborn as sns

RAW_DIR = Path("data/raw/calfire")
FIGURES_DIR = Path("reports/figures")

# Ten ngan -> ten file tho
RAW_FILES = {
    "perimeters": "California_Fire_Perimeters_all.csv",
    "dins": "CAL_FIRE_Damage_Inspection_DINS.csv",
    "ics209": "ICS209_California_Wildfires_2006_2012.csv",
    "noaa": "NOAA_California_Wildfires_Casualties.csv",
    "demographics": "California_Counties_Demographics.csv",
}

STUDY_YEARS = (2006, 2025)
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"  # dinh dang ngay cua FRAP va DINS, vd "8/1/2025 12:00:00 AM"
MAX_CONTAINMENT_DAYS = 365  # thoi gian dap lua < 0 hoac > 1 nam coi la loi nhap lieu
ACRE_TO_HA = 0.404686
MEGAFIRE_HA = 100_000 * ACRE_TO_HA  # sieu dam chay >= 100.000 acres (theo docs/DEMO_SCRIPT.md)
# Ten vu chay trong narrative NOAA: "The Camp Fire", "the August Complex" -> CAMP, AUGUST
NOAA_FIRE_NAME_PATTERN = r"\b(?:The )?([A-Z][\w'-]*(?: [A-Z][\w'-]*)?) (?:Fire|Complex)\b"

# Bang mau theo docs/COLOR_GUIDE.md (muc 2.1 Fire Sequential + mau trung tinh)
COLOR_NEUTRAL = "#7F7F7F"
COLOR_FIRE_MID = "#F16913"
COLOR_FIRE_HIGH = "#D94801"
COLOR_FIRE_EXTREME = "#8C2D04"


# ---------------------------------------------------------------------------
# Doc du lieu
# ---------------------------------------------------------------------------

def vn_number(value, decimals: int = 0) -> str:
    """So hien thi tren bieu do theo kieu Viet Nam: 7.342 (hang nghin), 97,5 (thap phan)."""
    return f"{value:,.{decimals}f}".replace(",", "_").replace(".", ",").replace("_", ".")


# Nhan truc so kieu Viet Nam cho truc tuyen tinh (vd 20.000 thay vi 20000, 0,05 thay vi 0.05)
VN_TICK_FORMATTER = FuncFormatter(lambda x, _: vn_number(x, 2).rstrip("0").rstrip(","))


def load_raw_data(raw_dir: Path = RAW_DIR) -> dict:
    """Doc nguyen trang 5 file tho -> {ten_ngan: DataFrame}. Khong them / sua cot."""
    # utf-8-sig: bo ky tu BOM o dau mot so file CAL FIRE
    return {
        name: pd.read_csv(raw_dir / filename, encoding="utf-8-sig", low_memory=False)
        for name, filename in RAW_FILES.items()
    }


def add_derived_columns(raw: dict) -> dict:
    """Tra ve ban sao co them cot phai sinh dung cho bieu do; giu nguyen dict tho de phan tich khuyet thieu."""
    data = dict(raw)
    perimeters = raw["perimeters"].copy()
    perimeters["burned_area_ha"] = perimeters["GIS Calculated Acres"] * ACRE_TO_HA
    data.update(perimeters=perimeters)
    return data


def normalize_fire_name(names: pd.Series) -> pd.Series:
    """Khoa 1 (ban rut gon cho EDA): viet hoa, CMPLX -> COMPLEX, bo hau to FIRE / INCIDENT / COMPLEX."""
    return (
        names.str.upper().str.strip()
        .str.replace(r"\bCMPLX\b", "COMPLEX", regex=True)
        .str.replace(r"[\s-]+(FIRE|INCIDENT|COMPLEX)$", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
    )


def extract_noaa_fire_name(noaa: pd.DataFrame) -> pd.Series:
    """Tach ten vu chay tu EVENT_NARRATIVE (uu tien) hoac EPISODE_NARRATIVE, chuan hoa theo Khoa 1."""
    name = noaa["EVENT_NARRATIVE"].str.extract(NOAA_FIRE_NAME_PATTERN, expand=False)
    name = name.fillna(noaa["EPISODE_NARRATIVE"].str.extract(NOAA_FIRE_NAME_PATTERN, expand=False))
    return normalize_fire_name(name)


def noaa_fire_key(noaa: pd.DataFrame) -> pd.Series:
    """Khoa gop dong NOAA cua cung 1 vu chay (dung kem EPISODE_ID); dong khong tach duoc ten giu rieng."""
    return extract_noaa_fire_name(noaa).fillna("_EVENT_" + noaa["EVENT_ID"].astype(str))


def build_structures_destroyed(data: dict) -> pd.DataFrame:
    """Gop so cong trinh bi pha huy theo tung vu chay: ICS-209 (2006-2012) + DINS (2013-2025)."""
    ics = data["ics209"]
    ics_part = pd.DataFrame({
        "year": ics["START_YEAR"],
        "fire_name": normalize_fire_name(ics["INCIDENT_NAME"]),
        "structures_destroyed": ics["STR_DESTROYED_TOTAL"],
        "source": "ICS-209 (2006-2012)",
    })

    # DINS: moi dong la 1 cong trinh -> dem so dong "Destroyed (>50%)" theo (nam, ten vu chay)
    dins = data["dins"]
    destroyed = dins[dins["* Damage"] == "Destroyed (>50%)"]
    year = pd.to_datetime(destroyed["Incident Start Date"], format=DATE_FORMAT).dt.year
    dins_part = (
        destroyed.assign(year=year, fire_name=normalize_fire_name(destroyed["* Incident Name"]))
        .groupby(["year", "fire_name"]).size().rename("structures_destroyed").reset_index()
        .assign(source="DINS (2013-2025)")
    )

    combined = pd.concat([ics_part, dins_part], ignore_index=True)
    # Chi giu vu chay co pha huy >= 1 cong trinh (DINS von chi ghi nhan vu co thiet hai; thang log khong nhan 0)
    return combined[combined["structures_destroyed"] > 0]


def build_fire_features(data: dict) -> pd.DataFrame:
    """Moi dong 1 vu chay FRAP 2006-2025: year, burned_area_ha, containment_days, structures_destroyed."""
    perimeters = data["perimeters"]
    p = perimeters[perimeters["Year"].between(*STUDY_YEARS)]
    # Vu khong ten -> khoa rieng theo OBJECTID de khong bi gop chung voi nhau
    fire_key = normalize_fire_name(p["Fire Name"]).fillna("_NO_NAME_" + p["OBJECTID"].astype(str))
    p = p.assign(
        year=p["Year"].astype(int),
        fire_name=fire_key,
        alarm=pd.to_datetime(p["Alarm Date"], format=DATE_FORMAT, errors="coerce"),
        contained=pd.to_datetime(p["Containment Date"], format=DATE_FORMAT, errors="coerce"),
    )

    # 1 vu chay = (nam, ten, don vi CAL FIRE) -> phan biet vu trung ten cung nam (vd CAMP 2018 BTU vs SLU).
    # 1 vu co the gom nhieu polygon -> cong dien tich, lay ngay bat dau som nhat / ket thuc muon nhat
    fires = p.groupby(["year", "fire_name", "Unit ID"], as_index=False, dropna=False).agg(
        burned_area_ha=("burned_area_ha", "sum"), alarm=("alarm", "min"), contained=("contained", "max"),
    )
    days = (fires["contained"] - fires["alarm"]).dt.days
    fires["containment_days"] = days.where(days.between(0, MAX_CONTAINMENT_DAYS))

    # Ghep so cong trinh bi pha huy theo (nam, ten). Neu nhieu vu trung ten cung nam thi chi gan cho vu lon nhat,
    # doi chieu chinh xac theo don vi / hat la Khoa 3 cua src/03_clean.py. Vu khong khop = khong co ghi nhan pha huy -> 0
    destroyed = build_structures_destroyed(data).groupby(["year", "fire_name"])["structures_destroyed"].sum()
    is_largest = fires["burned_area_ha"].eq(fires.groupby(["year", "fire_name"])["burned_area_ha"].transform("max"))
    fires = fires.merge(destroyed.reset_index(), on=["year", "fire_name"], how="left")
    fires["structures_destroyed"] = fires["structures_destroyed"].where(is_largest).fillna(0)
    return fires.drop(columns=["alarm", "contained"])


def summarize_all_files(raw: dict | None = None) -> pd.DataFrame:
    """Tong quan nhanh 5 file tho: so dong, so cot, ty le o trong, so dong trung lap."""
    raw = raw if raw is not None else load_raw_data()
    summary = pd.DataFrame([
        {
            "file": RAW_FILES.get(name, name),
            "so_dong": len(df),
            "so_cot": df.shape[1],
            "o_trong_%": round(df.isna().mean().mean() * 100, 1),
            "dong_trung_lap": int(df.duplicated().sum()),
        }
        for name, df in raw.items()
    ])
    print(summary.to_string(index=False))
    return summary


def _save_figure(fig: plt.Figure, output_path: Path, label: str) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"[TV1 - EDA] Da luu {label} -> {output_path}")


# ---------------------------------------------------------------------------
# Bieu do
# ---------------------------------------------------------------------------

def plot_missing_values(df=None, output_path: Path = FIGURES_DIR / "eda_01_missing_values.png", top_n: int = 12) -> plt.Figure:
    """Ve bieu do phan tich ty le khuyet thieu cua cac cot du lieu bang Matplotlib."""
    # df: None -> doc ca 5 file tho; DataFrame -> 1 bang; dict {ten: DataFrame} -> nhieu bang
    if df is None:
        datasets = load_raw_data()
    elif isinstance(df, pd.DataFrame):
        datasets = {"data": df}
    else:
        datasets = df

    ncols = 2 if len(datasets) > 1 else 1
    nrows = math.ceil(len(datasets) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(8 * ncols, 4.5 * nrows), squeeze=False)
    cmap = plt.get_cmap("OrRd")

    for ax, (name, data) in zip(axes.flat, datasets.items()):
        missing_pct = data.isna().mean() * 100
        n_missing_cols = int((missing_pct > 0).sum())
        # Chi giu top_n cot thieu nhieu nhat, dao nguoc de cot thieu nhieu nhat nam tren cung
        top = missing_pct[missing_pct > 0].sort_values(ascending=False).head(top_n)[::-1]

        title = Path(RAW_FILES.get(name, name)).stem
        ax.set_title(f"{title}\n{vn_number(len(data))} dòng | {n_missing_cols}/{data.shape[1]} cột có ô trống", loc="left", fontsize=10)
        if top.empty:
            ax.text(0.5, 0.5, "Không có ô trống", ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off()
            continue

        labels = [c if len(c) <= 40 else c[:37] + "..." for c in top.index]
        ax.barh(labels, top.values, color=cmap(0.3 + 0.7 * top.values / 100))
        for y, v in enumerate(top.values):
            ax.text(v + 1, y, f"{vn_number(v, 1)}%", va="center", fontsize=8)
        ax.axvline(50, color=COLOR_NEUTRAL, linestyle="--", linewidth=1)  # nguong 50%: can nhac bo cot
        ax.set_xlim(0, 112)
        ax.set_xlabel("Tỷ lệ khuyết thiếu (%)")
        ax.tick_params(axis="y", labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)

    # An cac o trong thua cua luoi subplot (vd 5 bang -> luoi 3x2 thua 1 o)
    for ax in axes.flat[len(datasets):]:
        ax.set_axis_off()

    fig.suptitle(f"Tỷ lệ khuyết thiếu theo cột (top {top_n} mỗi bảng, nét đứt = 50%)", fontsize=13, x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do khuyet thieu")
    return fig


def plot_distributions(df=None, output_path: Path = FIGURES_DIR / "eda_02_distributions.png") -> plt.Figure:
    """Ve bieu do phan phoi Histogram/KDE cua dien tich chay tren thang log."""
    # df: dict tu add_derived_columns(); None -> tu doc
    data = df if df is not None else add_derived_columns(load_raw_data())
    perimeters = data["perimeters"]

    # Chi lay giai doan nghien cuu 2006-2025; thang log khong nhan gia tri <= 0
    area = perimeters.loc[perimeters["Year"].between(*STUDY_YEARS), "burned_area_ha"]
    area = area[area > 0]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(area, log_scale=True, bins=40, kde=True, color=COLOR_FIRE_MID, edgecolor="white", ax=ax)
    ax.axvline(area.median(), color=COLOR_NEUTRAL, linestyle="--", linewidth=1)
    ax.text(area.median(), 0.97, f" trung vị {vn_number(area.median())} ha", transform=ax.get_xaxis_transform(), va="top", fontsize=8)
    ax.axvline(MEGAFIRE_HA, color=COLOR_FIRE_EXTREME, linestyle=":", linewidth=1.2)
    ax.text(MEGAFIRE_HA, 0.88, f" siêu đám cháy\n ≥ {vn_number(MEGAFIRE_HA)} ha", transform=ax.get_xaxis_transform(),
            va="top", fontsize=8, color=COLOR_FIRE_EXTREME)
    ax.set_title(f"Diện tích cháy (FRAP {STUDY_YEARS[0]}–{STUDY_YEARS[1]}, n = {vn_number(len(area))} vụ)", loc="left", fontsize=11)
    ax.set_xlabel("Diện tích cháy, ha (thang log)")
    ax.set_ylabel("Số vụ cháy")
    ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Phân phối lệch phải mạnh → cần biến đổi log1p trước khi làm sạch / mô hình", fontsize=13, x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do phan phoi")
    return fig


def plot_outlier_boxplots(df=None, output_path: Path = FIGURES_DIR / "eda_03_outliers_boxplot.png", top_n: int = 3) -> plt.Figure:
    """Ve bieu do hop (Boxplot) phat hien ngoai lai so cong trinh bi pha huy moi vu chay."""
    # df: DataFrame tu build_structures_destroyed(); None -> tu doc va gop
    data = df if df is not None else build_structures_destroyed(load_raw_data())
    palette = {"ICS-209 (2006-2012)": "#FDAE6B", "DINS (2013-2025)": COLOR_FIRE_MID}

    fig, ax = plt.subplots(figsize=(12, 5))
    # whis=1.5 tinh tren truc log -> nguong ngoai lai Tukey cho phan phoi log-normal
    sns.boxplot(data=data, x="structures_destroyed", y="source", hue="source", palette=palette, order=list(palette),
                log_scale=True, whis=1.5, width=0.5, showfliers=False, legend=False, ax=ax)
    sns.stripplot(data=data, x="structures_destroyed", y="source", order=list(palette), color=COLOR_FIRE_EXTREME,
                  size=3, alpha=0.4, jitter=0.2, ax=ax)

    # Gan nhan top_n vu lon nhat MOI nguon; moi nhan 1 tang cao rieng de khong de len nhau
    for y, source in enumerate(palette):
        top = data[data["source"] == source].nlargest(top_n, "structures_destroyed")
        for k, (_, row) in enumerate(top.iterrows()):
            ax.annotate(f"{row['fire_name'].title()} {int(row['year'])}: {vn_number(row['structures_destroyed'])}",
                        xy=(row["structures_destroyed"], y), xytext=(0, 18 + 16 * k), textcoords="offset points",
                        ha="center", fontsize=8, arrowprops={"arrowstyle": "-", "color": COLOR_NEUTRAL, "lw": 0.8})

    counts = data["source"].value_counts()
    ax.set_yticks(range(len(palette)), [f"{s}\nn = {counts.get(s, 0)} vụ" for s in palette])
    ax.set_xlabel("Số công trình bị phá hủy mỗi vụ cháy (thang log)")
    ax.set_ylabel("")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Công trình bị phá hủy mỗi vụ cháy: phần lớn vụ cháy < 40 nhà, một số ít siêu thảm họa hàng nghìn nhà",
                 loc="left", fontsize=12)
    fig.tight_layout()
    _save_figure(fig, output_path, "Boxplot ngoai lai")
    return fig


def plot_correlation_heatmap(df=None, output_path: Path = FIGURES_DIR / "eda_04_correlation_heatmap.png") -> plt.Figure:
    """Ve Correlation Heatmap bang Seaborn the hien moi tuong quan giua cac bien so."""
    # df: DataFrame tu build_fire_features(); None -> tu doc va gop
    fires = df if df is not None else build_fire_features(add_derived_columns(load_raw_data()))
    labels = {
        "year": "Năm",
        "burned_area_ha": "Diện tích cháy (ha)",
        "containment_days": "Số ngày dập lửa",
        "structures_destroyed": "Công trình bị phá hủy",
    }
    values = fires[list(labels)]
    # Pearson nhay voi ngoai lai -> tinh tren log1p; Spearman dua tren hang nen dung so goc
    logged = values.assign(**{c: np.log1p(values[c]) for c in labels if c != "year"})
    matrices = {
        "Pearson (trên log1p)": logged.corr(method="pearson"),
        "Spearman (tương quan hạng)": values.corr(method="spearman"),
    }

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    # Chi ve tam giac duoi (bo duong cheo = 1 va phan doi xung): bo hang dau va cot cuoi
    mask = np.triu(np.ones((len(labels) - 1, len(labels) - 1), dtype=bool), k=1)
    for ax, (title, corr) in zip(axes, matrices.items()):
        corr = corr.rename(index=labels, columns=labels).iloc[1:, :-1]
        # RdBu phan ky theo docs/COLOR_GUIDE.md muc 2.2: am = xanh, 0 = xam nhat, duong = do
        sns.heatmap(corr, mask=mask, annot=corr.map(lambda v: vn_number(v, 2)), fmt="", cmap="RdBu_r", vmin=-1, vmax=1, center=0,
                    square=True, linewidths=0.5, cbar=ax is axes[-1], cbar_kws={"shrink": 0.8}, ax=ax)
        ax.set_title(title, loc="left", fontsize=11)
        if ax.collections[0].colorbar is not None:
            ax.collections[0].colorbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: vn_number(x, 2)))
        ax.tick_params(axis="x", rotation=30)
        ax.tick_params(axis="y", rotation=0)

    n_days = int(values["containment_days"].notna().sum())
    fig.suptitle(f"Tương quan giữa các biến vụ cháy FRAP {STUDY_YEARS[0]}–{STUDY_YEARS[1]} "
                 f"(n = {vn_number(len(fires))} vụ; {vn_number(n_days)} vụ có đủ ngày bắt đầu / dập tắt)", fontsize=13, x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "Correlation Heatmap")
    return fig


def plot_temporal_trends(df=None, output_path: Path = FIGURES_DIR / "eda_05_temporal_trend.png", top_n: int = 3) -> plt.Figure:
    """Ve xu huong tan suat tham hoa va chay rung qua cac nam (2006-2025)."""
    # df: dict tu add_derived_columns(); None -> tu doc
    data = df if df is not None else add_derived_columns(load_raw_data())
    years = range(STUDY_YEARS[0], STUDY_YEARS[1] + 1)
    perimeters = data["perimeters"]
    perimeters = perimeters[perimeters["Year"].between(*STUDY_YEARS)]
    n_fires = perimeters.groupby("Year").size().reindex(years, fill_value=0)
    area_kha = perimeters.groupby("Year")["burned_area_ha"].sum().reindex(years, fill_value=0) / 1000
    destroyed = (
        build_structures_destroyed(data).groupby(["year", "source"])["structures_destroyed"].sum()
        .unstack(fill_value=0).reindex(years, fill_value=0)
    )

    fig, axes = plt.subplots(3, 1, figsize=(13, 10), sharex=True)

    # 1. So vu chay moi nam
    ax = axes[0]
    ax.plot(n_fires.index, n_fires.values, marker="o", color=COLOR_FIRE_HIGH, linewidth=2)
    ax.axhline(n_fires.mean(), color=COLOR_NEUTRAL, linestyle="--", linewidth=1)
    ax.set_ylabel("Số vụ cháy")
    ax.set_title(f"Số vụ cháy ghi nhận (FRAP, tổng {vn_number(n_fires.sum())} vụ, nét đứt = trung bình {vn_number(n_fires.mean())} vụ/năm)",
                 loc="left", fontsize=11)

    # 2. Tong dien tich chay moi nam
    ax = axes[1]
    ax.bar(area_kha.index, area_kha.values, color=COLOR_FIRE_MID)
    ax.set_ylabel("Nghìn ha")
    ax.set_title(f"Tổng diện tích cháy (nghìn ha, tổng {vn_number(area_kha.sum())})", loc="left", fontsize=11)
    _label_top_bars(ax, area_kha, top_n)

    # 3. Cong trinh bi pha huy moi nam, to mau theo nguon du lieu
    ax = axes[2]
    palette = {"ICS-209 (2006-2012)": "#FDAE6B", "DINS (2013-2025)": COLOR_FIRE_MID}
    bottom = np.zeros(len(destroyed))
    for source, color in palette.items():
        values = destroyed.get(source, pd.Series(0, index=destroyed.index))
        ax.bar(destroyed.index, values, bottom=bottom, color=color, label=source)
        bottom += values.to_numpy()
    _label_top_bars(ax, destroyed.sum(axis=1), top_n)
    ax.axvline(2012.5, color=COLOR_NEUTRAL, linestyle=":", linewidth=1)  # moc chuyen nguon ICS-209 -> DINS
    ax.legend(frameon=False, loc="upper left")
    ax.set_ylabel("Công trình")
    ax.set_title(f"Công trình bị phá hủy hoàn toàn (tổng {vn_number(destroyed.to_numpy().sum())})", loc="left", fontsize=11)

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.yaxis.set_major_formatter(VN_TICK_FORMATTER)
    axes[-1].set_xticks(list(years))
    axes[-1].tick_params(axis="x", rotation=45)
    fig.suptitle(f"Xu hướng cháy rừng California {STUDY_YEARS[0]}–{STUDY_YEARS[1]}: "
                 f"số vụ dao động {n_fires.min()}–{n_fires.max()}/năm, diện tích và thiệt hại dồn vào vài năm cực đoan",
                 fontsize=13, x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do xu huong thoi gian")
    return fig


def _label_top_bars(ax: plt.Axes, series: pd.Series, top_n: int) -> None:
    """Ghi gia tri len top_n cot cao nhat."""
    for x, v in series.nlargest(top_n).items():
        ax.annotate(vn_number(v), xy=(x, v), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)


def plot_casualties(df=None, output_path: Path = FIGURES_DIR / "eda_06_casualties.png", top_n: int = 3) -> plt.Figure:
    """Ve so nguoi chet / bi thuong truc tiep theo nam (NOAA), tach phan bi dem trung giua cac vung du bao."""
    # df: DataFrame NOAA tho; None -> tu doc
    noaa = df if df is not None else load_raw_data()["noaa"]
    noaa = noaa[noaa["YEAR"].between(*STUDY_YEARS)]
    years = range(STUDY_YEARS[0], STUDY_YEARS[1] + 1)
    measures = {"DEATHS_DIRECT": "Người chết trực tiếp", "INJURIES_DIRECT": "Người bị thương trực tiếp"}

    # 1 vu chay lan qua nhieu vung du bao -> nhieu dong lap lai cung so thuong vong; gop giong 03_clean.py
    events = noaa.groupby(["EPISODE_ID", noaa_fire_key(noaa).rename("fire_key")]).agg(
        YEAR=("YEAR", "first"), **{c: (c, "max") for c in measures}
    ).reset_index()
    raw_by_year = noaa.groupby("YEAR")[list(measures)].sum().reindex(years, fill_value=0)
    by_year = events.groupby("YEAR")[list(measures)].sum().reindex(years, fill_value=0)

    fig, axes = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
    for ax, (col, label) in zip(axes, measures.items()):
        merged, duplicated = by_year[col], raw_by_year[col] - by_year[col]
        ax.bar(years, merged, color=COLOR_FIRE_HIGH, label="Sau khi gộp trùng")
        ax.bar(years, duplicated, bottom=merged, color="#FDAE6B", label="Bị đếm trùng (1 vụ ghi ở nhiều vùng dự báo)")

        # Nhan top_n nam: gia tri sau gop + vu chay lon nhat trong nam (neu tach duoc ten)
        for year, value in merged.nlargest(top_n).items():
            top = events[events["YEAR"] == year].nlargest(1, col).iloc[0]
            name = "" if top["fire_key"].startswith("_EVENT_") else f"\n{top['fire_key'].title()} {vn_number(top[col])}"
            ax.annotate(f"{vn_number(value)}{name}", xy=(year, raw_by_year.at[year, col]), xytext=(0, 3),
                        textcoords="offset points", ha="center", fontsize=8)
        ax.set_ylabel("Người")
        ax.set_title(f"{label}: {vn_number(merged.sum())} người sau khi gộp trùng (dữ liệu thô ghi {vn_number(raw_by_year[col].sum())})",
                     loc="left", fontsize=11)
        ax.set_ylim(0, raw_by_year[col].max() * 1.25)  # chua cho nhan 2 dong tren cot cao nhat
        ax.spines[["top", "right"]].set_visible(False)
        ax.yaxis.set_major_formatter(VN_TICK_FORMATTER)

    axes[0].legend(frameon=False, loc="upper left")
    axes[-1].set_xticks(list(years))
    axes[-1].tick_params(axis="x", rotation=45)

    deadliest = events.nlargest(1, "DEATHS_DIRECT").iloc[0]
    total_deaths = by_year["DEATHS_DIRECT"].sum()
    fig.suptitle(f"Thiệt hại về người hiếm và dồn vào vài thảm họa: riêng {deadliest['fire_key'].title()} {deadliest['YEAR']} chiếm "
                 f"{deadliest['DEATHS_DIRECT'] / total_deaths:.0%} số người chết trực tiếp {STUDY_YEARS[0]}–{STUDY_YEARS[1]}",
                 fontsize=13, x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do thiet hai ve nguoi")
    return fig


# ---------------------------------------------------------------------------
# Dieu phoi
# ---------------------------------------------------------------------------

def run_initial_eda() -> None:
    """Ham dieu phoi toan bo luong EDA du lieu tho va xuat bao cao chat luong."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[TV1 - EDA] Bat dau kham pha du lieu tho tu: {RAW_DIR.resolve()}")
    raw = load_raw_data()  # doc 1 lan, dung chung cho moi bieu do
    data = add_derived_columns(raw)

    print("[TV1 - EDA] Tong quan 5 tap du lieu tho:")
    summarize_all_files(raw)

    print("[TV1 - EDA] Khoi tao cac bieu do tinh (Matplotlib, Seaborn) theo barem do an IDV (3-5 bieu do)...")
    figures = [
        plot_missing_values(raw, output_path=FIGURES_DIR / "eda_01_missing_values.png"),
        plot_distributions(data, output_path=FIGURES_DIR / "eda_02_distributions.png"),
        plot_outlier_boxplots(build_structures_destroyed(data), output_path=FIGURES_DIR / "eda_03_outliers_boxplot.png"),
        plot_correlation_heatmap(build_fire_features(data), output_path=FIGURES_DIR / "eda_04_correlation_heatmap.png"),
        plot_temporal_trends(data, output_path=FIGURES_DIR / "eda_05_temporal_trend.png"),
        plot_casualties(raw["noaa"], output_path=FIGURES_DIR / "eda_06_casualties.png"),
    ]

    # Script khong hien thi bieu do -> dong figure de giai phong bo nho
    for fig in figures:
        plt.close(fig)

    print("[TV1 - EDA] Hoan thanh phan tich kham pha du lieu. Cap nhat ket qua vao docs/DATA_QUALITY_REPORT.md.")


if __name__ == "__main__":
    run_initial_eda()
