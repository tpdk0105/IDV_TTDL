
import importlib.util
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score,
                             mean_absolute_error, precision_score, r2_score, recall_score, roc_auc_score,
                             roc_curve, root_mean_squared_error)
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Dung lai ham dinh dang so kieu Viet Nam tu 02_eda.py
_spec = importlib.util.spec_from_file_location("eda", Path(__file__).parent / "02_eda.py")
eda = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eda)

INPUT_PATH = Path("data/interim/master_rules_cleaned.csv")
CLF_PREDICTIONS_PATH = Path("data/clean/cause_classifier_predictions.csv")
CLF_METRICS_PATH = Path("data/clean/cause_classifier_metrics.csv")
CLF_FIGURE_PATH = Path("reports/figures/model_01_cause_classifier.png")
CLF_INSIGHT_FIGURE_PATH = Path("reports/figures/model_02_cause_insights.png")
DAMAGE_METRICS_PATH = Path("data/clean/damage_model_metrics.csv")
DAMAGE_CURVE_PATH = Path("data/clean/damage_model_curve.csv")
DAMAGE_FIRES_PATH = Path("data/clean/damage_model_fires.csv")
DAMAGE_FIGURE_PATH = Path("reports/figures/model_03_damage_loglog.png")
DAMAGE_CV_FIGURE_PATH = Path("reports/figures/model_04_damage_cv.png")

CONFIDENCE = 0.95

# Ca 2 mo hinh dung du lieu cat ngang (tung vu chay) -> kiem dinh cheo K-fold xao tron
CV_FOLDS = 5
RANDOM_STATE = 42
CURVE_ACRES = [100, 1_000, 10_000, 100_000, 1_000_000]  # cac moc dien tich de tra cuu nhanh

# Phan loai nguyen nhan Human / Natural: hoc tren vu da biet nguyen nhan, ap dung cho nhom Undetermined.
# Dia diem (don vi, hat) la bien manh nhat; cuoi tuan / ngay 4-7 / ngay trong nam khong cai thien AUC
CLF_NUMERIC = ["log_acres", "log_duration"]
CLF_CATEGORICAL = ["month", "unit_id", "county"]
CLF_FEATURES = CLF_NUMERIC + CLF_CATEGORICAL
CLF_THRESHOLD = 0.4          # nguong cho F1 cao nhat trong kiem dinh cheo
CLF_TEMPORAL_SPLIT = 2015    # kiem tra theo thoi gian: hoc <= 2015, du bao 2016-2025
CLF_MIN_CATEGORY = 20        # don vi / hat it hon 20 vu gop chung mot nhom
CLF_TOP_UNITS = 5            # so don vi in ra moi phia (nghieng ve set / ve nguoi) khi chay

# Mau theo docs/COLOR_GUIDE.md
COLOR_ACTUAL = "#D94801"
COLOR_FIT = "#7F7F7F"
COLOR_FORECAST = "#2171B5"
COLOR_BAND = "#9ECAE1"
COLOR_LABEL = "#084594"
TEXT_BOX = {"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "none", "alpha": 0.85}


def load_data(path: Path = INPUT_PATH) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"county_fips": str}, parse_dates=["alarm_date", "cont_date"])


def build_cause_data(df: pd.DataFrame) -> pd.DataFrame:
    # Can ngay bao chay de lay thang -> bo cac vu thieu alarm_date
    fires = df.dropna(subset=["alarm_date"]).copy()
    fires["month"] = fires["alarm_date"].dt.month.astype(str)
    fires["log_acres"] = np.log10(fires["acres_burned"].clip(lower=0.01))
    fires["log_duration"] = np.log1p(fires["duration_days"])  # NaN -> dien trung vi trong pipeline
    fires["county"] = fires["county"].fillna("Unknown")
    # 1 = Natural, 0 = Human, NaN = Undetermined (nhom can du doan)
    fires["is_natural"] = fires["cause_group"].map({"Natural": 1, "Human": 0})
    return fires[["incident_id", "year", "fire_name", "cause_group", "is_natural", *CLF_FEATURES]].reset_index(drop=True)


def build_damage(df: pd.DataFrame) -> pd.DataFrame:
    # Chi cac vu co pha huy cong trinh: log10(0) khong xac dinh
    damage = df.loc[df["structures_destroyed"] > 0,
                    ["incident_id", "year", "fire_name", "county", "cause_group", "acres_burned",
                     "burned_area_ha", "structures_destroyed", "structures_damaged"]].copy()
    assert (damage["acres_burned"] > 0).all(), "dien tich chay phai > 0 de lay log"
    damage["log_acres"] = np.log10(damage["acres_burned"])
    damage["log_destroyed"] = np.log10(damage["structures_destroyed"])
    return damage.reset_index(drop=True)


def _prediction_interval(x: np.ndarray, y: np.ndarray, model: LinearRegression, x0: np.ndarray):
    # Khoang du bao cua hoi quy tuyen tinh don: rong dan khi x0 cang xa trung tam du lieu
    n = len(x)
    pred = model.intercept_ + model.coef_[0] * x0
    residuals = y - (model.intercept_ + model.coef_[0] * x)
    residual_std = np.sqrt((residuals ** 2).sum() / (n - 2))
    std_error = residual_std * np.sqrt(1 + 1 / n + (x0 - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum())
    t_critical = stats.t.ppf((1 + CONFIDENCE) / 2, df=n - 2)
    return pred, pred - t_critical * std_error, pred + t_critical * std_error


def describe_damage(damage: pd.DataFrame) -> dict:
    res = stats.linregress(damage["log_acres"], damage["log_destroyed"])
    return {
        "n_fires": len(damage),
        "slope": res.slope,
        "slope_stderr": res.stderr,
        "slope_t": res.slope / res.stderr,
        "intercept": res.intercept,
        "intercept_stderr": res.intercept_stderr,
        "intercept_t": res.intercept / res.intercept_stderr,
        "r2_fit_all": res.rvalue ** 2,
        "p_value": res.pvalue,
        # Dien tich gap 10 lan -> so cong trinh pha huy gap 10^slope lan
        "multiplier_per_10x_area": 10 ** res.slope,
    }


def evaluate_damage(damage: pd.DataFrame) -> tuple[dict, pd.Series]:
    oof_log = pd.Series(np.nan, index=damage.index)
    naive_log = pd.Series(np.nan, index=damage.index)
    for train_idx, test_idx in KFold(CV_FOLDS, shuffle=True, random_state=RANDOM_STATE).split(damage):
        train, test = damage.iloc[train_idx], damage.iloc[test_idx]
        model = LinearRegression().fit(train[["log_acres"]], train["log_destroyed"])
        oof_log.iloc[test_idx] = model.predict(test[["log_acres"]])
        naive_log.iloc[test_idx] = train["log_destroyed"].mean()  # moc so sanh: bo qua dien tich

    actual = damage["structures_destroyed"]
    # 10^du bao log = trung vi (khong phai trung binh) so cong trinh o dien tich do
    predicted, naive = 10 ** oof_log, 10 ** naive_log
    metrics = {
        "cv_folds": CV_FOLDS,
        "r2_cv_log": r2_score(damage["log_destroyed"], oof_log),
        "mae_cv_log": mean_absolute_error(damage["log_destroyed"], oof_log),
        "mae_cv_log_naive": mean_absolute_error(damage["log_destroyed"], naive_log),
        "median_ae_cv": float((actual - predicted).abs().median()),
        "median_ae_cv_naive": float((actual - naive).abs().median()),
        "mae_cv": mean_absolute_error(actual, predicted),
        "rmse_cv": root_mean_squared_error(actual, predicted),
    }
    return metrics, predicted


def damage_curve(damage: pd.DataFrame, acres) -> pd.DataFrame:
    x, y = damage["log_acres"].to_numpy(), damage["log_destroyed"].to_numpy()
    model = LinearRegression().fit(x.reshape(-1, 1), y)
    pred, lower, upper = _prediction_interval(x, y, model, np.log10(np.asarray(acres, dtype=float)))
    return pd.DataFrame({
        "acres_burned": acres,
        "predicted_destroyed": 10 ** pred,
        # Mo hinh chi hoc tren cac vu co pha huy -> can duoi it nhat 1 cong trinh
        "lower_95": np.clip(10 ** lower, 1, None),
        "upper_95": 10 ** upper,
    })


def _cause_classifier() -> Pipeline:
    features = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), CLF_NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=CLF_MIN_CATEGORY), CLF_CATEGORICAL),
    ])
    return make_pipeline(features, LogisticRegression(max_iter=5000))


def _classification_scores(y_true: np.ndarray, proba: np.ndarray, label: str) -> dict:
    pred = (proba >= CLF_THRESHOLD).astype(int)
    return {
        "evaluation": label,
        "n_fires": len(y_true),
        "auc": roc_auc_score(y_true, proba),
        # 64% la Human -> accuracy de danh lua, can xem them balanced accuracy va F1
        "accuracy": accuracy_score(y_true, pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, pred),
        "precision": precision_score(y_true, pred, zero_division=0),
        "recall": recall_score(y_true, pred),
        "f1": f1_score(y_true, pred),
        "natural_actual": int(y_true.sum()),
        "natural_expected": float(proba.sum()),  # tong xac suat ~ so vu Natural neu xac suat hieu chinh tot
    }


def evaluate_cause_classifier(known: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    X, y = known[CLF_FEATURES], known["is_natural"].astype(int).to_numpy()
    cv = StratifiedKFold(CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    oof = cross_val_predict(_cause_classifier(), X, y, cv=cv, method="predict_proba")[:, 1]

    # Hoc qua khu, du bao cac nam sau: kiem tra mo hinh con dung khi du lieu troi theo thoi gian
    past = (known["year"] <= CLF_TEMPORAL_SPLIT).to_numpy()
    temporal = _cause_classifier().fit(X[past], y[past]).predict_proba(X[~past])[:, 1]

    metrics = pd.DataFrame([
        _classification_scores(y, np.zeros(len(y)), "moc: doan tat ca la Human"),
        _classification_scores(y, oof, f"kiem dinh cheo {CV_FOLDS}-fold"),
        _classification_scores(y[~past], temporal, f"hoc <= {CLF_TEMPORAL_SPLIT}, du bao {CLF_TEMPORAL_SPLIT + 1}-2025"),
    ])
    return metrics, oof


def cause_odds_ratios(model: Pipeline) -> pd.DataFrame:
    # Ty so odds > 1: nghieng ve Natural. Bien so: cho moi +1 do lech chuan
    names = model[0].get_feature_names_out()
    odds = pd.DataFrame({"feature": names, "odds_ratio": np.exp(model[-1].coef_[0])})
    odds["group"] = odds["feature"].str.extract(r"^(?:num|cat)__(log_acres|log_duration|month|unit_id|county)",
                                                expand=False)
    odds["level"] = odds.apply(lambda r: r["feature"].split(f"{r['group']}_", 1)[-1] if r["group"] in CLF_CATEGORICAL
                               else r["group"], axis=1)
    return odds


def _save_figure(fig: plt.Figure, output_path: Path, label: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")


def _style_loglog(ax: plt.Axes) -> None:
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(eda.VN_TICK_FORMATTER)
    ax.yaxis.set_major_formatter(eda.VN_TICK_FORMATTER)
    ax.spines[["top", "right"]].set_visible(False)


def plot_damage_fit(damage: pd.DataFrame, output_path: Path = DAMAGE_FIGURE_PATH) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    line = damage_curve(damage, np.logspace(damage["log_acres"].min(), damage["log_acres"].max(), 200))
    ax.fill_between(line["acres_burned"], line["lower_95"], line["upper_95"], color=COLOR_BAND, alpha=0.35,
                    label=f"Khoảng dự báo {CONFIDENCE:.0%}")
    ax.scatter(damage["acres_burned"], damage["structures_destroyed"], color=COLOR_ACTUAL, alpha=0.45, s=14,
               label="Vụ cháy thực tế")
    ax.plot(line["acres_burned"], line["predicted_destroyed"], color=COLOR_FORECAST, linewidth=2.5,
            label="Dự báo của mô hình")
    for _, row in damage_curve(damage, CURVE_ACRES[1:4]).iterrows():
        ax.annotate(f"{eda.vn_number(row['acres_burned'])} mẫu Anh\n≈ {eda.vn_number(row['predicted_destroyed'])} công trình",
                    xy=(row["acres_burned"], row["predicted_destroyed"]), xytext=(-10, 28),
                    textcoords="offset points", ha="right", fontsize=9, fontweight="bold", color=COLOR_LABEL,
                    bbox=TEXT_BOX, arrowprops={"arrowstyle": "-", "color": COLOR_LABEL, "linewidth": 0.8})
    _style_loglog(ax)
    ax.set_xlabel("Diện tích cháy (mẫu Anh, thang log)")
    ax.set_ylabel("Số công trình bị phá hủy (thang log)")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    ax.set_title("Diện tích cháy càng lớn, càng nhiều công trình bị phá hủy",
                 fontsize=12, fontweight="bold", loc="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do mo hinh log-log")
    return fig


def plot_damage_cv(damage: pd.DataFrame, metrics: dict, predicted: pd.Series,
                   output_path: Path = DAMAGE_CV_FIGURE_PATH) -> plt.Figure:
    # Diem cang sat duong cheo -> du bao ngoai mau cang dung
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(predicted, damage["structures_destroyed"], color=COLOR_FORECAST, alpha=0.45, s=14,
               label="Vụ cháy")
    x_lims = [float(predicted.min()) / 1.5, float(predicted.max()) * 2]
    ax.plot(x_lims, x_lims, color=COLOR_FIT, linestyle="--", linewidth=1.2, label="Dự báo đúng bằng thực tế")
    _style_loglog(ax)
    ax.set_xlim(x_lims)
    ax.set_ylim(0.7, float(damage["structures_destroyed"].max()) * 1.5)
    ax.set_xlabel("Số công trình mô hình dự báo (thang log)")
    ax.set_ylabel("Số công trình thực tế (thang log)")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    ax.set_title(f"Kiểm định chéo {CV_FOLDS}-fold: thực tế so với dự báo "
                 f"(R² = {eda.vn_number(metrics['r2_cv_log'], 2)})", fontsize=12, fontweight="bold", loc="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do kiem dinh cheo")
    return fig


def plot_cause_classifier(known: pd.DataFrame, oof: np.ndarray, metrics: pd.DataFrame,
                          output_path: Path = CLF_FIGURE_PATH) -> plt.Figure:
    y = known["is_natural"].astype(int).to_numpy()
    cv_row = metrics.iloc[1]
    fig, (ax_roc, ax_cm) = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [1.15, 1]})

    fpr, tpr, _ = roc_curve(y, oof)
    ax_roc.plot(fpr, tpr, color=COLOR_FORECAST, linewidth=2.2,
                label=f"Hồi quy logistic (AUC = {eda.vn_number(cv_row['auc'], 3)})")
    ax_roc.plot([0, 1], [0, 1], color=COLOR_FIT, linestyle="--", linewidth=1, label="Đoán ngẫu nhiên (AUC = 0,5)")
    ax_roc.set_xlabel("Tỷ lệ vụ do người bị đoán nhầm là do sét")
    ax_roc.set_ylabel("Tỷ lệ vụ do sét được nhận ra (Recall)")
    ax_roc.legend(frameon=False, loc="lower right", fontsize=9)
    _style_metric_panel(ax_roc, f"1. Đường ROC (kiểm định chéo {CV_FOLDS}-fold)")

    cm = confusion_matrix(y, (oof >= CLF_THRESHOLD).astype(int))
    ax_cm.imshow(cm / cm.sum(axis=1, keepdims=True), cmap="Blues", vmin=0, vmax=1)
    for (i, j), value in np.ndenumerate(cm):
        share = value / cm[i].sum()
        ax_cm.text(j, i, f"{eda.vn_number(value)}\n({eda.vn_number(share * 100, 0)}%)", ha="center", va="center",
                   fontsize=12, fontweight="bold", color="white" if share > 0.5 else COLOR_LABEL)
    ax_cm.set_xticks([0, 1], ["Dự đoán: Người", "Dự đoán: Sét"])
    ax_cm.set_yticks([0, 1], ["Thực tế: Người", "Thực tế: Sét"])
    ax_cm.set_title(f"2. Ma trận nhầm lẫn (ngưỡng {eda.vn_number(CLF_THRESHOLD, 1)})\n"
                    f"F1 = {eda.vn_number(cv_row['f1'], 2)} · Balanced accuracy = "
                    f"{eda.vn_number(cv_row['balanced_accuracy'], 2)}", fontsize=11, fontweight="bold", loc="left")

    fig.suptitle(f"Phân loại nguyên nhân cháy: con người hay sét ({eda.vn_number(len(known))} vụ đã biết nguyên nhân)",
                 fontsize=12, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do phan loai nguyen nhan")
    return fig


def plot_cause_insights(predictions: pd.DataFrame, output_path: Path = CLF_INSIGHT_FIGURE_PATH) -> plt.Figure:
    fig, ax_year = plt.subplots(figsize=(12, 5.8))

    # Thanh phan moi nam: da biet + uoc tinh cho nhom Undetermined (tong xac suat)
    und = predictions[predictions["cause_is_predicted"] == 1]
    by_year = pd.DataFrame({
        "Người (đã biết)": predictions[predictions["cause_group"] == "Human"].groupby("year").size(),
        "Sét (đã biết)": predictions[predictions["cause_group"] == "Natural"].groupby("year").size(),
        "Không rõ → ước tính người": und.groupby("year")["p_natural"].apply(lambda s: (1 - s).sum()),
        "Không rõ → ước tính sét": und.groupby("year")["p_natural"].sum(),
    }).fillna(0)
    colors = [COLOR_FORECAST, COLOR_ACTUAL, COLOR_BAND, eda.COLOR_FIRE_LIGHT]
    bottom = np.zeros(len(by_year))
    for (label, values), color in zip(by_year.items(), colors):
        ax_year.bar(by_year.index, values, bottom=bottom, color=color, label=label, width=0.75)
        bottom += values.to_numpy()
    ax_year.set_ylabel("Số vụ cháy")
    ax_year.yaxis.set_major_formatter(eda.VN_TICK_FORMATTER)
    ax_year.set_xticks(by_year.index[::2])
    ax_year.legend(frameon=False, loc="upper left", fontsize=9, ncol=2)
    _style_metric_panel(ax_year, "Số vụ cháy theo nguyên nhân mỗi năm, nhóm không rõ nguyên nhân được phân bổ theo xác suất dự đoán")

    human_like = (1 - und["p_natural"]).sum()
    fig.suptitle(f"Phần lớn vụ cháy không rõ nguyên nhân mang đặc điểm cháy do con người: ước tính "
                 f"{eda.vn_number(human_like)} / {eda.vn_number(len(und))} vụ ({eda.vn_number(human_like / len(und) * 100, 0)}%)",
                 fontsize=12, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout()
    _save_figure(fig, output_path, "bieu do dien giai phan loai")
    return fig


def _style_metric_panel(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=11, fontweight="bold", loc="left")
    ax.spines[["top", "right"]].set_visible(False)


def run_cause_classifier() -> pd.DataFrame:
    fires = build_cause_data(load_data())
    known = fires[fires["is_natural"].notna()].reset_index(drop=True)
    undetermined = fires[fires["is_natural"].isna()].reset_index(drop=True)
    print(f"[TV1 - MODEL] Phan loai nguyen nhan: hoc tren {len(known)} vu da biet "
          f"(Natural = {known['is_natural'].mean() * 100:.1f}%), du doan {len(undetermined)} vu Undetermined")

    metrics, oof = evaluate_cause_classifier(known)
    final = _cause_classifier().fit(known[CLF_FEATURES], known["is_natural"].astype(int))

    # Vu da biet: xac suat ngoai mau (CV) de danh gia; vu Undetermined: mo hinh hoc tren toan bo vu da biet
    predictions = pd.concat([
        known.assign(p_natural=oof, p_source="cv_out_of_fold", cause_is_predicted=0),
        undetermined.assign(p_natural=final.predict_proba(undetermined[CLF_FEATURES])[:, 1],
                            p_source="final_model", cause_is_predicted=1),
    ], ignore_index=True)
    predictions["cause_predicted"] = np.where(predictions["p_natural"] >= CLF_THRESHOLD, "Natural", "Human")
    # Khong ghi de nguyen nhan goc: du doan nam o cot rieng, danh dau bang cause_is_predicted
    predictions["prediction_correct"] = (predictions["cause_predicted"] == predictions["cause_group"]).where(
        predictions["cause_is_predicted"] == 0)
    assert len(predictions) == len(fires) and predictions["incident_id"].is_unique
    assert predictions["p_natural"].between(0, 1).all()

    CLF_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(CLF_METRICS_PATH, index=False, encoding="utf-8")
    predictions.drop(columns=["is_natural"]).to_csv(CLF_PREDICTIONS_PATH, index=False, encoding="utf-8")

    odds = cause_odds_ratios(final)
    print(metrics.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    und = predictions[predictions["cause_is_predicted"] == 1]
    print(f"  Undetermined: uoc {und['p_natural'].sum():.0f} / {len(und)} vu co dac diem chay do set "
          f"({und['p_natural'].mean() * 100:.1f}%), nguong {CLF_THRESHOLD} -> "
          f"{(und['cause_predicted'] == 'Natural').sum()} vu gan nhan Natural")
    numeric = odds[odds["group"].isin(CLF_NUMERIC)].set_index("level")["odds_ratio"]
    print("  Ty so odds bien so (moi +1 do lech chuan):", numeric.round(2).to_dict())
    # Don vi quan ly nghieng ve set / ve nguoi nhieu nhat (bo nhom gop "infrequent")
    units = odds[(odds["group"] == "unit_id") & ~odds["level"].str.startswith("infrequent")].set_index("level")
    print("  Don vi nghieng ve set nhat:", units["odds_ratio"].nlargest(CLF_TOP_UNITS).round(2).to_dict())
    print("  Don vi nghieng ve nguoi nhat:", units["odds_ratio"].nsmallest(CLF_TOP_UNITS).round(2).to_dict())

    plt.close(plot_cause_classifier(known, oof, metrics))
    plt.close(plot_cause_insights(predictions))
    return predictions


def run_damage_model() -> pd.DataFrame:
    damage = build_damage(load_data())
    summary = describe_damage(damage)
    metrics, predicted = evaluate_damage(damage)
    curve = damage_curve(damage, CURVE_ACRES)
    assert (curve["lower_95"] <= curve["predicted_destroyed"]).all()
    assert (curve["predicted_destroyed"] <= curve["upper_95"]).all()

    DAMAGE_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{**summary, **metrics}]).to_csv(DAMAGE_METRICS_PATH, index=False, encoding="utf-8")
    curve.to_csv(DAMAGE_CURVE_PATH, index=False, encoding="utf-8")
    # Tung vu chay kem du bao cua mo hinh -> dung cho Tableau
    fitted = damage_curve(damage, damage["acres_burned"]).drop(columns="acres_burned")
    fires = pd.concat([damage, fitted], axis=1).assign(predicted_destroyed_cv=predicted)
    assert len(fires) == summary["n_fires"]
    fires.to_csv(DAMAGE_FIRES_PATH, index=False, encoding="utf-8")

    print(f"\n[TV1 - MODEL] Hoi quy log-log tren {summary['n_fires']} vu co pha huy cong trinh:")
    print(f"  log10(destroyed) = {summary['slope']:.6f} * log10(acres) + {summary['intercept']:.6f}")
    print(f"  R2 = {summary['r2_fit_all']:.3f}, t = {summary['slope_t']:.3f}, p = {summary['p_value']:.2e}, "
          f"dien tich x10 -> cong trinh x{summary['multiplier_per_10x_area']:.2f}")
    print(f"  {CV_FOLDS}-fold: R2 log = {metrics['r2_cv_log']:.3f}, MAE log = {metrics['mae_cv_log']:.3f} "
          f"(moc {metrics['mae_cv_log_naive']:.3f}), median AE = {metrics['median_ae_cv']:.1f} "
          f"(moc {metrics['median_ae_cv_naive']:.1f})")
    print(curve.to_string(index=False, float_format=lambda v: f"{v:,.1f}"))

    plt.close(plot_damage_fit(damage))
    plt.close(plot_damage_cv(damage, metrics, predicted))
    return curve


if __name__ == "__main__":
    run_cause_classifier()
    run_damage_model()
