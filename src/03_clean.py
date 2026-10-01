"""
Module: src/03_clean.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Làm sạch dữ liệu Bước 1 theo quy tắc (Rule-based cleaning).
    - Chuẩn hóa tên quốc gia về chuẩn ISO 3166-1 alpha-3 (country_converter/pycountry).
    - Chuẩn hóa ngày tháng về chuẩn ISO 8601 (YYYY-MM-DD), lọc phạm vi 2006–2025.
    - Chuẩn hóa đơn vị đo: diện tích cháy quy về Hecta (ha), thiệt hại quy về USD.
    - Loại bỏ trùng lặp chính xác, sửa các lỗi hiển nhiên (giá trị âm, tọa độ ngoài miền).
    - Bảo toàn các cột dữ liệu gốc song song để lưu vết (vd: damage_usd_raw, burned_area_ha_raw).
    - Xuất tập dữ liệu trung gian: `data/interim/master_rules_cleaned.csv`.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 2.
"""

import sys
from pathlib import Path


def clean_by_rules() -> None:
    """Thực hiện làm sạch theo quy tắc từ data/raw/ sang data/interim/master_rules_cleaned.csv."""
    interim_dir = Path("data/interim")
    interim_dir.mkdir(parents=True, exist_ok=True)
    out_path = interim_dir / "master_rules_cleaned.csv"
    print(f"[TODO - TV1] Bắt đầu quy trình làm sạch dữ liệu theo quy tắc...")
    print(f"[TODO - TV1] Chuẩn hóa ISO3, ngày/giờ 2006-2025, quy đổi đơn vị ha, USD...")
    print(f"[TODO - TV1] Đầu ra dự kiến: {out_path.resolve()}")
    # TODO (Giai đoạn 2): Viết logic làm sạch theo quy tắc và lưu master_rules_cleaned.csv.


if __name__ == "__main__":
    clean_by_rules()
