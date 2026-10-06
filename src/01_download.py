"""
Module: src/01_download.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng tại California / Bắc Mỹ (2006–2025)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu & Học máy (Data & ML Engineer)
Mục đích:
    - Thu thập dữ liệu thô NGUYÊN BẢN từ các nguồn mở chính phủ Hoa Kỳ & California:
        1. CAL FIRE FRAP: Chu vi và lịch sử các vụ cháy rừng California (23.334 vụ, diện tích cháy acres, nguyên nhân).
        2. CAL FIRE DINS: Cơ sở dữ liệu kiểm kê chi tiết thiệt hại công trình & nhà cửa (132.522 công trình).
        3. California State Geoportal: Thông tin địa lý hành chính và dân số 58 hạt của California (US Census).
        4. NOAA NCEI Storm Events: Dữ liệu thương vong sinh mạng và thiệt hại tài sản quy đổi USD từ NOAA.
    - Tự động sinh `data/raw/MANIFEST.md` và `data/raw/manifest.json`.
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

# Thiết lập UTF-8 cho console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_RAW_DIR = Path("data/raw")
CALFIRE_DIR = DATA_RAW_DIR / "calfire"


def calculate_sha256(file_path: Path) -> str:
    """Tính mã băm SHA-256 của tập tin."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def download_file(url: str, out_path: Path, timeout: int = 120) -> bool:
    """Tải tệp tin qua HTTP stream có báo cáo tiến độ."""
    if out_path.exists() and out_path.stat().st_size > 0:
        print(f"  [Đã có] {out_path.name} ({out_path.stat().st_size:,} bytes). Bỏ qua.")
        return True

    print(f"  Đang tải {out_path.name} từ: {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(out_path, "wb") as out_f:
            total = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                out_f.write(chunk)
                total += len(chunk)
        elapsed = time.time() - t0
        print(f"  [Thành công] {out_path.name} ({total:,} bytes) trong {elapsed:.1f}s.")
        return True
    except Exception as e:
        print(f"  [Lỗi tải {out_path.name}]: {e}")
        if out_path.exists():
            out_path.unlink()
        return False


def download_calfire_perimeters() -> None:
    """Tải tập dữ liệu chu vi và lịch sử cháy rừng California (CAL FIRE FRAP)."""
    url = "https://gis.data.cnra.ca.gov/api/download/v1/items/c3c10388e3b24cec8a954ba10458039d/csv?layers=0"
    out_file = CALFIRE_DIR / "California_Fire_Perimeters_all.csv"
    print("\n>>> [1/3] Đang thu thập CAL FIRE Perimeters (Tần suất, Diện tích cháy, Nguyên nhân)...")
    download_file(url, out_file)


def download_calfire_dins() -> None:
    """Tải cơ sở dữ liệu kiểm kê thiệt hại tài sản & công trình CAL FIRE DINS."""
    url = "https://gis.data.cnra.ca.gov/api/download/v1/items/994d3dc4569640caadbbc3198d5a3da1/csv?layers=0"
    out_file = CALFIRE_DIR / "CAL_FIRE_Damage_Inspection_DINS.csv"
    print("\n>>> [2/3] Đang thu thập CAL FIRE DINS (Thiệt hại công trình, nhà cửa bị phá hủy)...")
    download_file(url, out_file, timeout=180)


def download_california_counties() -> None:
    """Tải bảng danh mục địa lý và dân số 58 hạt California (California State Geoportal)."""
    url = "https://gis.data.ca.gov/api/download/v1/items/60b7e0f3d33b4064a4b43bf14589bfe3/csv?layers=1"
    out_file = CALFIRE_DIR / "California_Counties_Demographics.csv"
    print("\n>>> [3/3] Đang thu thập thông tin địa lý và dân số 58 hạt California...")
    download_file(url, out_file)


def generate_manifest() -> None:
    """Tự động kiểm kê và lập bản kê dữ liệu thô MANIFEST.md và manifest.json."""
    manifest_entries = []
    print("\n>>> Đang tính toán mã băm SHA-256 cho toàn bộ dữ liệu thô...")

    for csv_file in sorted(CALFIRE_DIR.glob("*.csv")):
        sha256 = calculate_sha256(csv_file)
        source_name = "CAL FIRE / State of California Open Data"
        if "NOAA" in csv_file.name:
            source_name = "NOAA NCEI Storm Events Database"
        manifest_entries.append({
            "file_name": csv_file.name,
            "path": f"data/raw/calfire/{csv_file.name}",
            "size_bytes": csv_file.stat().st_size,
            "sha256": sha256,
            "source": source_name,
            "downloaded_at": datetime.now().isoformat()
        })

    # Ghi manifest.json
    manifest_json_path = DATA_RAW_DIR / "manifest.json"
    with open(manifest_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, indent=2, ensure_ascii=False)

    # Ghi MANIFEST.md
    manifest_md_path = DATA_RAW_DIR / "MANIFEST.md"
    with open(manifest_md_path, "w", encoding="utf-8") as f:
        f.write("# BẢN KIỂM KÊ DỮ LIỆU THÔ (RAW DATA MANIFEST)\n\n")
        f.write("> **Phân vùng nghiên cứu**: Bang California (Bắc Mỹ) - Điểm nóng cháy rừng toàn cầu\n")
        f.write(f"> **Thời gian tạo bản kê**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Tên File | Nguồn dữ liệu | Kích thước | SHA-256 (Checksum) |\n")
        f.write("|---|---|---|---|\n")
        for item in manifest_entries:
            f.write(f"| `{item['file_name']}` | {item['source']} | {item['size_bytes']:,} bytes | `{item['sha256'][:16]}...` |\n")

    print(f"  [Xong] Đã cập nhật {manifest_md_path} và {manifest_json_path}.")


def main() -> None:
    print("=" * 70)
    print("DATA PIPELINE 01: THU THẬP DỮ LIỆU CHÁY RỪNG CALIFORNIA (2006–2025)")
    print("=" * 70)
    
    CALFIRE_DIR.mkdir(parents=True, exist_ok=True)
    
    download_calfire_perimeters()
    download_calfire_dins()
    download_california_counties()
    generate_manifest()
    
    print("\n" + "=" * 70)
    print("HOÀN TẤT THU THẬP DỮ LIỆU THÔ! ĐẦY ĐỦ CÁC CHIỀU:")
    print(" - Tần suất cháy rừng & Mùa vụ (2006–2025)")
    print(" - Thiệt hại diện tích (Acres / Hecta) & Phân cấp đám cháy")
    print(" - Thiệt hại tài sản & Công trình nhà cửa bị phá hủy (DINS)")
    print(" - Thiệt hại sinh mạng & Thương vong (NOAA)")
    print(" - Nguyên nhân cháy rừng (Tự nhiên vs Nhân tạo)")
    print("=" * 70)


if __name__ == "__main__":
    main()
