"""
Module: src/01_download.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2006–2025)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Thu thập dữ liệu thô từ các nguồn mở uy tín (EM-DAT, NASA FIRMS, USFS/Kaggle, Our World in Data).
    - Lưu trữ tệp tin nguyên bản vào thư mục `data/raw/` mà không chỉnh sửa thủ công.
    - Ghi nhận nhật ký tải về vào `docs/DATA_SOURCES.md`.

Trạng thái: Khung mã nguồn (Giai đoạn 1) - Sẽ triển khai chi tiết trong Giai đoạn 2.
"""

import os
import sys
from pathlib import Path


def download_raw_data() -> None:
    """Tải dữ liệu thô vào thư mục data/raw/."""
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    print(f"[TODO - TV1] Bắt đầu quy trình thu thập dữ liệu thô vào: {raw_dir.resolve()}")
    print("[TODO - TV1] Kiểm tra cấu hình API token (Kaggle/NASA) hoặc nạp file EM-DAT...")
    # TODO (Giai đoạn 2): Viết logic tải dữ liệu thực tế từ API / URL chính thức.


if __name__ == "__main__":
    download_raw_data()
