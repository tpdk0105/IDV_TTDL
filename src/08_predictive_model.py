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
    - `reports/figures/model_01_forecast.png`.

Cách chạy (từ thư mục gốc dự án, sau src/03_clean.py):
    python src/08_predictive_model.py
"""

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

INPUT_PATH = Path("data/interim/master_rules_cleaned.csv")
FORECAST_PATH = Path("data/clean/forecast_results.csv")
METRICS_PATH = Path("data/clean/forecast_metrics.csv")
FIGURE_PATH = Path("reports/figures/model_01_forecast.png")
METRICS_FIGURE_PATH = Path("reports/figures/model_02_metrics.png")

FIRST_TEST_YEAR = 2016                # rolling origin: du bao lan luot 2016..2025 (10 lan)
FORECAST_YEARS = range(2026, 2036)    # 10 nam tuong lai
CONFIDENCE = 0.95

# (ten cot, co huan luyen tren log1p khong, nhan hien thi)
FORECAST_TARGETS = [
    ("n_fires", False, "So vu chay"),
    ("area_ha", True, "Tong dien tich chay (ha)"),
    ("destroyed", True, "Cong trinh bi pha huy"),
]

# Mau theo docs/COLOR_GUIDE.md
COLOR_ACTUAL = "#D94801"
COLOR_FIT = "#7F7F7F"
COLOR_FORECAST = "#2171B5"
COLOR_BAND = "#9ECAE1"


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
    y = np.log1p(train[target]) if use_log else train[target]
    return LinearRegression().fit(train[["year"]], y)


def _to_original_scale(values, use_log: bool):
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
    resid = y_fit - model.predict(yearly[["year"]])
    s = np.sqrt((resid ** 2).sum() / (n - 2))
    x0 = all_years["year"].to_numpy()
    se = s * np.sqrt(1 + 1 / n + (x0 - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum())
    t = stats.t.ppf((1 + CONFIDENCE) / 2, df=n - 2)
    lower, upper = pred - t * se, pred + t * se

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


def plot_forecasts(forecast: pd.DataFrame, output_path: Path = FIGURE_PATH) -> plt.Figure:
    """3 bieu do: diem thuc te, duong xu huong / du bao, vung khoang du bao 95%."""
    fig, axes = plt.subplots(len(FORECAST_TARGETS), 1, figsize=(12, 11), sharex=True)
    last_year = forecast.loc[~forecast["is_forecast"], "year"].max()

    for ax, (target, use_log, label) in zip(axes, FORECAST_TARGETS):
        data = forecast[forecast["metric"] == target]
        hist, future = data[~data["is_forecast"]], data[data["is_forecast"]]

        ax.fill_between(data["year"], data["lower_95"], data["upper_95"], color=COLOR_BAND, alpha=0.35,
                        label=f"Khoang du bao {CONFIDENCE:.0%}")
        ax.plot(hist["year"], hist["predicted"], color=COLOR_FIT, linewidth=1.5, label="Duong xu huong")
        ax.plot(future["year"], future["predicted"], color=COLOR_FORECAST, linewidth=2.2, marker="o", markersize=4,
                label=f"Du bao {future['year'].min()}-{future['year'].max()}")
        ax.scatter(hist["year"], hist["actual"], color=COLOR_ACTUAL, zorder=3, s=25, label="Thuc te")
        ax.axvline(last_year + 0.5, color=COLOR_FIT, linestyle=":", linewidth=1)

        end = future.iloc[-1]
        ax.annotate(f"{end['predicted']:,.0f}\n[{end['lower_95']:,.0f} - {end['upper_95']:,.0f}]",
                    xy=(end["year"], end["predicted"]), xytext=(8, 0), textcoords="offset points",
                    va="center", fontsize=8, color=COLOR_FORECAST)
        if use_log:
            ax.set_yscale("log")  # khoang du bao lech manh, truc log de doc ca 2 dau
        ax.set_ylabel(label + (" (log)" if use_log else ""))
        ax.spines[["top", "right"]].set_visible(False)

    axes[0].legend(frameon=False, loc="upper left", fontsize=8, ncol=4)
    axes[-1].set_xticks(range(int(forecast["year"].min()), int(forecast["year"].max()) + 1, 2))
    fig.suptitle(f"Du bao Linear Regression {min(FORECAST_YEARS)}-{max(FORECAST_YEARS)} "
                 f"(vung xanh = khoang du bao {CONFIDENCE:.0%})", fontsize=13, x=0.01, ha="left")
    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"[TV1 - MODEL] Da luu bieu do du bao -> {output_path}")
    return fig


def plot_model_metrics(metrics: pd.DataFrame, output_path: Path = METRICS_FIGURE_PATH) -> plt.Figure:
    """Truc quan hoa cac thong so danh gia mo hinh: do doc xu huong, p-value / R2 va so sanh sai so MAE."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    labels_map = {
        "n_fires": "So vu chay\n(n_fires)",
        "area_ha": "Tong dien tich\n(area_ha)",
        "destroyed": "Cong trinh pha huy\n(destroyed)",
    }
    y_labels = [labels_map.get(m, m) for m in metrics["metric"]]

    # 1. Do doc xu huong moi nam (trend_per_year)
    ax = axes[0]
    bars = ax.barh(y_labels, metrics["trend_per_year"], color=COLOR_FORECAST, alpha=0.85, height=0.55)
    ax.axvline(0, color=COLOR_FIT, linestyle="--", linewidth=1)
    max_trend = float(metrics["trend_per_year"].max())
    for bar, (_, row) in zip(bars, metrics.iterrows()):
        val = row["trend_per_year"]
        unit = row["trend_unit"]
        ax.text(val + (max_trend * 0.03), bar.get_y() + bar.get_height() / 2,
                f"+{val:.2f} {unit}", va="center", ha="left", fontsize=9, fontweight="bold", color="#084594")
    ax.set_title("1. Toc do thay doi hang nam (Trend)", fontsize=11, fontweight="bold", loc="left")
    ax.set_xlabel("Gia tri thay doi moi nam")
    ax.set_xlim(0, max_trend * 1.5)
    ax.spines[["top", "right"]].set_visible(False)

    # 2. Muc y nghia thong ke (p-value) & R2
    ax = axes[1]
    p_colors = [COLOR_ACTUAL if p < 0.05 else (COLOR_BAND if p < 0.1 else COLOR_FIT) for p in metrics["p_value"]]
    bars = ax.bar(y_labels, metrics["p_value"], color=p_colors, alpha=0.85, width=0.5)
    ax.axhline(0.05, color="#B2182B", linestyle=":", linewidth=1.5, label="Nguong p = 0.05 (95% CI)")
    max_p = float(metrics["p_value"].max())
    for bar, (_, row) in zip(bars, metrics.iterrows()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"p={row['p_value']:.3f}\nR²={row['r2_fit_all_years']:.1%}",
                ha="center", va="bottom", fontsize=8.5)
    ax.set_title("2. Kiem dinh y nghia thong ke (p-value)", fontsize=11, fontweight="bold", loc="left")
    ax.set_ylabel("Gia tri p-value")
    ax.set_ylim(0, max_p * 1.35)
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)

    # 3. So sanh sai so MAE Model vs MAE Naive Baseline
    ax = axes[2]
    rel_mae = (metrics["mae"] / metrics["mae_naive_mean"]) * 100
    bars = ax.bar(y_labels, rel_mae, color=["#6BAED6", "#9ECAE1", "#4292C6"], alpha=0.9, width=0.5)
    ax.axhline(100, color="#7F7F7F", linestyle="--", linewidth=1.2, label="Moc Baseline Naive (100%)")
    max_rel = float(rel_mae.max())
    for bar, (_, row), r in zip(bars, metrics.iterrows(), rel_mae):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{r:.1f}%\n(MAE: {row['mae']:,.0f})",
                ha="center", va="bottom", fontsize=8)
    ax.set_title("3. So sanh MAE mo hinh vs Naive Baseline", fontsize=11, fontweight="bold", loc="left")
    ax.set_ylabel("Ty le MAE / Naive MAE (%)")
    ax.set_ylim(0, max_rel * 1.25)
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)

    fig.suptitle("Tong hop cac thong so danh gia mo hinh hoi quy (Linear Regression 2006-2025)",
                 fontsize=12, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"[TV1 - MODEL] Da luu bieu do thong so mo hinh -> {output_path}")
    return fig


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
