"""
Module: src/08_predictive_model.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu & Học máy
Mục đích:
    - Dự báo 10 năm tới (2026–2035) bằng Hồi quy tuyến tính (Linear Regression, scikit-learn) cho 3 chỉ số theo năm:
        1. `n_fires`   – số vụ cháy mỗi năm (thang gốc).
        2. `area_ha`   – tổng diện tích cháy (huấn luyện trên log1p do phân phối lệch nặng).
        3. `destroyed` – tổng số công trình bị phá hủy (huấn luyện trên log1p).
    - Đánh giá bằng rolling origin (cửa sổ mở rộng): train đến năm t-1, dự báo năm t, với t = 2016..2025;
      không chia ngẫu nhiên vì dữ liệu là chuỗi thời gian (xáo trộn = học từ tương lai, sai số bị đánh giá thấp).
    - Chỉ số sai số: R², MAE, RMSE; so sánh với mô hình "đoán bằng trung bình quá khứ".
    - Khoảng dự báo 95% (prediction interval) của hồi quy tuyến tính đơn.

Đầu ra:
    - `data/clean/forecast_results.csv`  : year, metric, actual, predicted, lower_95, upper_95, is_forecast (bàn giao TV2/TV3).
    - `data/clean/forecast_metrics.csv`  : sai số rolling origin + độ dốc xu hướng của từng chỉ số.
    - `reports/figures/model_01_forecast.png` : điểm thực tế, đường xu hướng, dự báo + khoảng dự báo 95%.
    - `reports/figures/model_02_metrics.png`  : độ dốc xu hướng, p-value / R², MAE so với mốc trung bình.

Cách chạy (từ thư mục gốc dự án, sau src/03_clean.py):
    python src/08_predictive_model.py
"""

import importlib.util
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error

# Dung lai ham dinh dang so kieu Viet Nam tu 02_eda.py (ten file bat dau bang so nen khong import thuong duoc)
_spec = importlib.util.spec_from_file_location("eda", Path(__file__).parent / "02_eda.py")
eda = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eda)

INPUT_PATH = Path("data/interim/master_rules_cleaned.csv")
FORECAST_PATH = Path("data/clean/forecast_results.csv")
METRICS_PATH = Path("data/clean/forecast_metrics.csv")
FIGURE_PATH = Path("reports/figures/model_01_forecast.png")
METRICS_FIGURE_PATH = Path("reports/figures/model_02_metrics.png")

FIRST_TEST_YEAR = 2016                # rolling origin: du bao lan luot 2016..2025 (10 lan)
FORECAST_YEARS = range(2026, 2036)    # 10 nam tuong lai
CONFIDENCE = 0.95
SIGNIFICANCE = 0.05                   # nguong p-value

# (ten cot, co huan luyen tren log1p khong, nhan hien thi)
FORECAST_TARGETS = [
    ("n_fires", False, "Số vụ cháy"),
    ("area_ha", True, "Tổng diện tích cháy (ha)"),
    ("destroyed", True, "Công trình bị phá hủy"),
]
# Nhan 2 dong cho truc cua bieu do thong so mo hinh
METRIC_AXIS_LABELS = {
    "n_fires": "Số vụ cháy\n(n_fires)",
    "area_ha": "Tổng diện tích\n(area_ha)",
    "destroyed": "Công trình phá hủy\n(destroyed)",
}
# Don vi trend_unit trong forecast_metrics.csv -> nhan hien thi tren bieu do
TREND_UNIT_LABELS = {"%/nam": "%/năm", "don vi/nam": "vụ/năm"}

# Mau theo docs/COLOR_GUIDE.md
COLOR_ACTUAL = "#D94801"
COLOR_FIT = "#7F7F7F"
COLOR_FORECAST = "#2171B5"
COLOR_BAND = "#9ECAE1"
COLOR_LABEL = "#084594"
COLOR_THRESHOLD = "#B2182B"
MAE_BAR_COLORS = ["#6BAED6", "#9ECAE1", "#4292C6"]


# ---------------------------------------------------------------------------
# Du lieu & mo hinh
# ---------------------------------------------------------------------------

def load_data(path: Path = INPUT_PATH) -> pd.DataFrame:
    """Doc bang vu chay da lam sach (giu county_fips dang chuoi de khong mat so 0 dau)."""
    return pd.read_csv(path, dtype={"county_fips": str}, parse_dates=["alarm_date", "cont_date"])


def build_yearly(df: pd.DataFrame) -> pd.DataFrame:
    """Gom theo nam: so vu chay, tong dien tich, tong cong trinh bi pha huy."""
    return (
        df.groupby("year")
        .agg(
            n_fires=("year", "size"),
            area_ha=("burned_area_ha", "sum"),
            destroyed=("structures_destroyed", "sum"),
        )
        .reset_index()
    )


def _fit(train: pd.DataFrame, target: str, use_log: bool) -> LinearRegression:
    """Hoi quy target theo nam; chi so lech nang duoc huan luyen tren log1p."""
    y = np.log1p(train[target]) if use_log else train[target]
    return LinearRegression().fit(train[["year"]], y)


def _to_original_scale(values, use_log: bool):
    """Dua du bao tren thang log1p ve lai don vi goc."""
    return np.expm1(values) if use_log else values


def evaluate_trend(yearly: pd.DataFrame, target: str, use_log: bool) -> dict:
    """Rolling origin: train den nam t-1, du bao nam t (t = FIRST_TEST_YEAR..nam cuoi); tinh sai so tren thang goc."""
    preds, naive_preds, actuals = [], [], []
    for t in range(FIRST_TEST_YEAR, int(yearly["year"].max()) + 1):
        train = yearly[yearly["year"] < t]
        test = yearly[yearly["year"] == t]
        model = _fit(train, target, use_log)
        preds.append(_to_original_scale(model.predict(test[["year"]])[0], use_log))
        naive_preds.append(train[target].mean())  # moc so sanh: doan bang trung binh qua khu
        actuals.append(test[target].iat[0])

    # Moi lan chi co 1 diem -> R2 tinh 1 lan tren ca 10 cap (thuc te, du bao)
    return {
        "metric": target,
        "n_folds": len(actuals),
        "r2": r2_score(actuals, preds),
        "mae": mean_absolute_error(actuals, preds),
        "rmse": root_mean_squared_error(actuals, preds),
        "mae_naive_mean": mean_absolute_error(actuals, naive_preds),
    }


def describe_trend(yearly: pd.DataFrame, target: str, use_log: bool) -> dict:
    """Do doc xu huong tren du 20 nam va muc y nghia thong ke."""
    y = np.log1p(yearly[target]) if use_log else yearly[target]
    res = stats.linregress(yearly["year"], y)
    return {
        "metric": target,
        "trained_on_log": use_log,
        # Thang log: do doc = % thay doi moi nam; thang goc: don vi / nam
        "trend_per_year": np.expm1(res.slope) * 100 if use_log else res.slope,
        "trend_unit": "%/nam" if use_log else "don vi/nam",
        "r2_fit_all_years": res.rvalue ** 2,
        "p_value": res.pvalue,
    }


def forecast_trend(yearly: pd.DataFrame, target: str, use_log: bool) -> pd.DataFrame:
    """Huan luyen tren du cac nam co du lieu, du bao den het FORECAST_YEARS kem khoang du bao 95%."""
    x = yearly["year"].to_numpy()
    y_fit = np.log1p(yearly[target].to_numpy(dtype=float)) if use_log else yearly[target].to_numpy(dtype=float)
    model = _fit(yearly, target, use_log)

    all_years = pd.DataFrame({"year": list(x) + list(FORECAST_YEARS)})
    pred = model.predict(all_years[["year"]])

    # Khoang du bao cua hoi quy tuyen tinh don: rong dan khi nam cang xa trung tam du lieu
    n = len(x)
    residuals = y_fit - model.predict(yearly[["year"]])
    residual_std = np.sqrt((residuals ** 2).sum() / (n - 2))
    x0 = all_years["year"].to_numpy()
    std_error = residual_std * np.sqrt(1 + 1 / n + (x0 - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum())
    t_critical = stats.t.ppf((1 + CONFIDENCE) / 2, df=n - 2)
    lower, upper = pred - t_critical * std_error, pred + t_critical * std_error

    pred, lower, upper = (_to_original_scale(v, use_log) for v in (pred, lower, upper))

    result = all_years.assign(
        metric=target,
        predicted=pred,
        lower_95=np.clip(lower, 0, None),  # so vu / dien tich / cong trinh khong the am
        upper_95=upper,
    )
    actual = yearly[["year", target]].rename(columns={target: "actual"})
    result = result.merge(actual, on="year", how="left")
    result["is_forecast"] = result["year"] > x.max()
    return result[["year", "metric", "actual", "predicted", "lower_95", "upper_95", "is_forecast"]]


# ---------------------------------------------------------------------------
# Bieu do
# ---------------------------------------------------------------------------

def _save_figure(fig: plt.Figure, output_path: Path, label: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"[TV1 - MODEL] Da luu {label} -> {output_path}")


def plot_forecasts(forecast: pd.DataFrame, output_path: Path = FIGURE_PATH) -> plt.Figure:
    """3 bieu do: diem thuc te, duong xu huong / du bao, vung khoang du bao 95%."""
    fig, axes = plt.subplots(len(FORECAST_TARGETS), 1, figsize=(12, 11), sharex=True)
    last_year = forecast.loc[~forecast["is_forecast"], "year"].max()

    for ax, (target, use_log, label) in zip(axes, FORECAST_TARGETS):
        data = forecast[forecast["metric"] == target]
        hist, future = data[~data["is_forecast"]], data[data["is_forecast"]]

        ax.fill_between(data["year"], data["lower_95"], data["upper_95"], color=COLOR_BAND, alpha=0.35,
                        label=f"Khoảng dự báo {CONFIDENCE:.0%}")
        ax.plot(hist["year"], hist["predicted"], color=COLOR_FIT, linewidth=1.5, label="Đường xu hướng")
        ax.plot(future["year"], future["predicted"], color=COLOR_FORECAST, linewidth=2.2, marker="o", markersize=4,
                label=f"Dự báo {future['year'].min()}–{future['year'].max()}")
        ax.scatter(hist["year"], hist["actual"], color=COLOR_ACTUAL, zorder=3, s=25, label="Thực tế")
        ax.axvline(last_year + 0.5, color=COLOR_FIT, linestyle=":", linewidth=1)

        # Ghi gia tri du bao nam cuoi kem khoang [thap - cao]
        end = future.iloc[-1]
        ax.annotate(f"{eda.vn_number(end['predicted'])}\n"
                    f"[{eda.vn_number(end['lower_95'])} – {eda.vn_number(end['upper_95'])}]",
                    xy=(end["year"], end["predicted"]), xytext=(8, 0), textcoords="offset points",
                    va="center", fontsize=8, color=COLOR_FORECAST)
        if use_log:
            ax.set_yscale("log")  # khoang du bao lech manh, truc log de doc ca 2 dau
        else:
            ax.yaxis.set_major_formatter(eda.VN_TICK_FORMATTER)
        ax.set_ylabel(label + (" (log)" if use_log else ""))
        ax.spines[["top", "right"]].set_visible(False)

    axes[0].legend(frameon=False, loc="upper left", fontsize=8, ncol=4)
    axes[-1].set_xticks(range(int(forecast["year"].min()), int(forecast["year"].max()) + 1, 2))
    fig.suptitle(f"Dự báo hồi quy tuyến tính {min(FORECAST_YEARS)}–{max(FORECAST_YEARS)} "
                 f"(vùng xanh = khoảng dự báo {CONFIDENCE:.0%})", fontsize=13, x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do du bao")
    return fig


def _style_metric_panel(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=11, fontweight="bold", loc="left")
    ax.spines[["top", "right"]].set_visible(False)


def _plot_trend_panel(ax: plt.Axes, metrics: pd.DataFrame, labels: list[str]) -> None:
    """Khung 1: do doc xu huong moi nam (thang log: %/nam, thang goc: vu/nam)."""
    bars = ax.barh(labels, metrics["trend_per_year"], color=COLOR_FORECAST, alpha=0.85, height=0.55)
    ax.axvline(0, color=COLOR_FIT, linestyle="--", linewidth=1)
    max_trend = float(metrics["trend_per_year"].max())
    for bar, (_, row) in zip(bars, metrics.iterrows()):
        value = row["trend_per_year"]
        unit = TREND_UNIT_LABELS.get(row["trend_unit"], row["trend_unit"])
        sign = "+" if value >= 0 else "-"
        ax.text(value + (max_trend * 0.03), bar.get_y() + bar.get_height() / 2,
                f"{sign}{eda.vn_number(abs(value), 2)} {unit}",
                va="center", ha="left", fontsize=9, fontweight="bold", color=COLOR_LABEL)
    _style_metric_panel(ax, "1. Tốc độ thay đổi hằng năm (xu hướng)")
    ax.set_xlabel("Giá trị thay đổi mỗi năm")
    ax.set_xlim(0, max_trend * 1.5)
    ax.xaxis.set_major_formatter(eda.VN_TICK_FORMATTER)


def _plot_pvalue_panel(ax: plt.Axes, metrics: pd.DataFrame, labels: list[str]) -> None:
    """Khung 2: p-value cua do doc; cam = co y nghia, xanh nhat = gan nguong (< 0,1), xam = khong co y nghia."""
    colors = [COLOR_ACTUAL if p < SIGNIFICANCE else (COLOR_BAND if p < 0.1 else COLOR_FIT) for p in metrics["p_value"]]
    bars = ax.bar(labels, metrics["p_value"], color=colors, alpha=0.85, width=0.5)
    ax.axhline(SIGNIFICANCE, color=COLOR_THRESHOLD, linestyle=":", linewidth=1.5,
               label=f"Ngưỡng p = {eda.vn_number(SIGNIFICANCE, 2)} (độ tin cậy 95%)")
    for bar, (_, row) in zip(bars, metrics.iterrows()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"p = {eda.vn_number(row['p_value'], 3)}\nR² = {eda.vn_number(row['r2_fit_all_years'] * 100, 1)}%",
                ha="center", va="bottom", fontsize=8.5)
    _style_metric_panel(ax, "2. Kiểm định ý nghĩa thống kê (p-value)")
    ax.set_ylabel("Giá trị p-value")
    ax.set_ylim(0, float(metrics["p_value"].max()) * 1.35)
    ax.yaxis.set_major_formatter(eda.VN_TICK_FORMATTER)
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)


def _plot_mae_panel(ax: plt.Axes, metrics: pd.DataFrame, labels: list[str]) -> None:
    """Khung 3: MAE mo hinh / MAE moc 'doan bang trung binh' (%); < 100% nghia la mo hinh tot hon moc."""
    relative_mae = (metrics["mae"] / metrics["mae_naive_mean"]) * 100
    bars = ax.bar(labels, relative_mae, color=MAE_BAR_COLORS, alpha=0.9, width=0.5)
    ax.axhline(100, color=COLOR_FIT, linestyle="--", linewidth=1.2, label="Mốc so sánh: đoán bằng trung bình (100%)")
    for bar, (_, row), rel in zip(bars, metrics.iterrows(), relative_mae):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{eda.vn_number(rel, 1)}%\n(MAE: {eda.vn_number(row['mae'])})",
                ha="center", va="bottom", fontsize=8)
    _style_metric_panel(ax, "3. So sánh MAE mô hình với mốc trung bình")
    ax.set_ylabel("Tỷ lệ MAE mô hình / MAE mốc (%)")
    ax.set_ylim(0, float(relative_mae.max()) * 1.25)
    ax.yaxis.set_major_formatter(eda.VN_TICK_FORMATTER)
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)


def plot_model_metrics(metrics: pd.DataFrame, output_path: Path = METRICS_FIGURE_PATH) -> plt.Figure:
    """Truc quan hoa cac thong so danh gia mo hinh: do doc xu huong, p-value / R2 va so sanh sai so MAE."""
    fig, (ax_trend, ax_pvalue, ax_mae) = plt.subplots(1, 3, figsize=(15, 4.5))
    labels = [METRIC_AXIS_LABELS.get(m, m) for m in metrics["metric"]]

    _plot_trend_panel(ax_trend, metrics, labels)
    _plot_pvalue_panel(ax_pvalue, metrics, labels)
    _plot_mae_panel(ax_mae, metrics, labels)

    fig.suptitle("Tổng hợp các thông số đánh giá mô hình hồi quy tuyến tính (2006–2025)",
                 fontsize=12, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do thong so mo hinh")
    return fig


# ---------------------------------------------------------------------------
# Dieu phoi
# ---------------------------------------------------------------------------

def run_predictive_models() -> pd.DataFrame:
    """Danh gia (rolling origin), du bao 10 nam va xuat ket qua cho TV2 / TV3."""
    yearly = build_yearly(load_data())
    print(f"[TV1 - MODEL] Du lieu theo nam: {yearly['year'].min()}-{yearly['year'].max()} ({len(yearly)} nam)")

    forecasts, metrics = [], []
    for target, use_log, _ in FORECAST_TARGETS:
        metrics.append({**describe_trend(yearly, target, use_log), **evaluate_trend(yearly, target, use_log)})
        forecasts.append(forecast_trend(yearly, target, use_log))

    forecast = pd.concat(forecasts, ignore_index=True)
    metrics = pd.DataFrame(metrics)

    expected_rows = len(FORECAST_TARGETS) * (len(yearly) + len(FORECAST_YEARS))
    assert len(forecast) == expected_rows, f"forecast co {len(forecast)} dong, ky vong {expected_rows}"
    assert (forecast["lower_95"] <= forecast["predicted"]).all() and (forecast["predicted"] <= forecast["upper_95"]).all()

    FORECAST_PATH.parent.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(FORECAST_PATH, index=False, encoding="utf-8")
    metrics.to_csv(METRICS_PATH, index=False, encoding="utf-8")
    print(f"[TV1 - MODEL] Da xuat {len(forecast)} dong du bao -> {FORECAST_PATH}")
    print(f"[TV1 - MODEL] Da xuat sai so -> {METRICS_PATH}")

    print(f"\n[TV1 - MODEL] Danh gia rolling origin ({FIRST_TEST_YEAR}-{yearly['year'].max()}, du bao 1 nam toi):")
    print(metrics[["metric", "trend_per_year", "trend_unit", "p_value", "r2", "mae", "rmse", "mae_naive_mean"]]
          .to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    print(f"\n[TV1 - MODEL] Du bao {min(FORECAST_YEARS)} va {max(FORECAST_YEARS)}:")
    edge = forecast[forecast["year"].isin([min(FORECAST_YEARS), max(FORECAST_YEARS)])]
    print(edge.drop(columns=["actual", "is_forecast"]).to_string(index=False, float_format=lambda v: f"{v:,.0f}"))

    plt.close(plot_forecasts(forecast))
    plt.close(plot_model_metrics(metrics))
    return forecast


if __name__ == "__main__":
    run_predictive_models()
