"""
Module: src/01_download.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng / thảm họa thiên nhiên (2005–2024)
Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
Mục đích:
    - Thu thập dữ liệu thô NGUYÊN BẢN từ các nguồn mở uy tín quốc tế:
        1. Our World in Data (OWID): Thống kê vĩ mô thảm họa thiên nhiên toàn cầu (CC-BY 4.0).
        2. NASA FIRMS: Dữ liệu điểm cháy vệ tinh MODIS & VIIRS thời gian thực (Public Domain).
        3. NOAA NCEI Storm Events: Dữ liệu sự kiện thảm họa và cháy rừng cấp sự kiện (Public Domain).
        4. USDA Forest Service FPA-FOD: Dữ liệu sự kiện cháy rừng 2005-2020 (Public Domain).
    - Lưu trữ tệp tin nguyên bản vào thư mục `data/raw/<ten_nguon>/` mà không chỉnh sửa giá trị.
    - Tự động sinh `data/raw/MANIFEST.md` và `data/raw/manifest.json`.
"""

import os
import sys
import json
import time
import gzip
import shutil
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path
import pandas as pd

# Thiết lập UTF-8 cho console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_RAW_DIR = Path("data/raw")


def calculate_sha256(file_path: Path) -> str:
    """Tính mã băm SHA-256 của tập tin."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def download_file(url: str, out_path: Path, timeout: int = 60) -> bool:
    """Tải tệp tin qua HTTP stream có báo cáo dung lượng."""
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


def download_owid() -> None:
    """Tải dữ liệu thô từ Our World in Data (OWID)."""
    dest_dir = DATA_RAW_DIR / "owid"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    files = {
        "natural-disasters-by-type.csv": "https://ourworldindata.org/grapher/natural-disasters-by-type.csv",
        "economic-damage-from-natural-disasters.csv": "https://ourworldindata.org/grapher/economic-damage-from-natural-disasters.csv"
    }
    
    print("\n>>> [1/4] Đang thu thập dữ liệu Our World in Data (OWID)...")
    for filename, url in files.items():
        download_file(url, dest_dir / filename)


def download_nasa_firms() -> None:
    """Tải dữ liệu thô điểm cháy từ NASA FIRMS."""
    dest_dir = DATA_RAW_DIR / "nasa_firms"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    files = {
        "MODIS_C6_1_Global_7d.csv": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_7d.csv",
        "SUOMI_VIIRS_C2_Global_7d.csv": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_7d.csv"
    }
    
    print("\n>>> [2/4] Đang thu thập dữ liệu NASA FIRMS Active Fire Hotspots...")
    for filename, url in files.items():
        download_file(url, dest_dir / filename, timeout=90)


def download_noaa_ncei() -> None:
    """Tải dữ liệu sự kiện thảm họa và cháy rừng từ NOAA NCEI Storm Events Database."""
    dest_dir = DATA_RAW_DIR / "noaa_ncei"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Hai năm đại diện tiêu biểu (2020: đỉnh cháy rừng bờ Tây Mỹ; 2023: năm cháy rừng kỷ lục)
    files = {
        "StormEvents_details_2020.csv.gz": "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2020_c20260323.csv.gz",
        "StormEvents_details_2023.csv.gz": "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2023_c20260323.csv.gz"
    }
    
    print("\n>>> [3/4] Đang thu thập dữ liệu thảm họa cấp sự kiện từ NOAA NCEI (2020, 2023)...")
    for filename, url in files.items():
        download_file(url, dest_dir / filename, timeout=60)


def download_usfs_fod(limit_per_year: int = 500) -> None:
    """
    Tải dữ liệu thô sự kiện cháy rừng từ USDA Forest Service (FPA-FOD 6th Edition).
    Thực hiện truy vấn mẫu có chỉ mục fire_year.
    """
    dest_dir = DATA_RAW_DIR / "usfs_fod"
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_path = dest_dir / "usfs_wildfires_sample.csv"
    
    print("\n>>> [4/4] Đang thu thập dữ liệu sự kiện cháy rừng USDA Forest Service (FPA-FOD)...")
    if out_path.exists() and out_path.stat().st_size > 0:
        print(f"  [Đã có] {out_path.name} ({out_path.stat().st_size:,} bytes). Bỏ qua.")
        return

    base_url = "https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_FireOccurrence6thEdition_01/MapServer/29/query"
    fields = "fod_id,fire_name,fire_year,discovery_date,nwcg_cause_classification,nwcg_general_cause,fire_size,latitude,longitude,state"
    
    all_records = []
    # Thu thập 3 năm mẫu: 2018, 2019, 2020
    test_years = [2018, 2019, 2020]
    
    for year in test_years:
        where_clause = f"fire_year={year}"
        params = f"?where={urllib.parse.quote(where_clause)}&outFields={fields}&resultRecordCount={limit_per_year}&f=json"
        url = base_url + params
        
        print(f"  Đang lấy dữ liệu năm {year} (tối đa {limit_per_year} vụ)...", end="", flush=True)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                features = data.get('features', [])
                if features:
                    batch = [f['attributes'] for f in features]
                    all_records.extend(batch)
                    print(f" Lấy được {len(batch)} vụ.")
                else:
                    print(" Không có bản ghi.")
            time.sleep(1)
        except Exception as e:
            print(f" Bỏ qua ({e})")
            
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(out_path, index=False, encoding='utf-8')
        print(f"  [Thành công] Đã lưu {len(df):,} bản ghi vào {out_path.name}.")


def build_manifest() -> None:
    """Tạo MANIFEST.md và manifest.json ghi nhận thông tin chi tiết từng tệp tin thô."""
    print("\n>>> Đang sinh tệp MANIFEST.md và manifest.json...")
    manifest_entries = []
    
    # Duyệt toàn bộ tệp trong data/raw/
    for file_path in sorted(DATA_RAW_DIR.glob("**/*")):
        if not file_path.is_file() or file_path.name in [".gitkeep", "MANIFEST.md", "manifest.json", "README.md"]:
            continue
            
        rel_path = file_path.relative_to(DATA_RAW_DIR).as_posix()
        size_bytes = file_path.stat().st_size
        sha256 = calculate_sha256(file_path)
        
        source_name = file_path.parent.name
        source_meta = {
            "owid": {
                "source": "Our World in Data (OWID)",
                "url": "https://ourworldindata.org/natural-disasters",
                "license": "Creative Commons Attribution (CC-BY 4.0)"
            },
            "nasa_firms": {
                "source": "NASA FIRMS (Earthdata)",
                "url": "https://firms.modaps.eosdis.nasa.gov/",
                "license": "NASA Open Data Policy (Public Domain)"
            },
            "noaa_ncei": {
                "source": "NOAA NCEI Storm Events Database",
                "url": "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/",
                "license": "U.S. Federal Government (Public Domain)"
            },
            "usfs_fod": {
                "source": "USDA Forest Service (FPA-FOD 6th Edition)",
                "url": "https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_FireOccurrence6thEdition_01/MapServer/29",
                "license": "U.S. Federal Government (Public Domain)"
            }
        }.get(source_name, {"source": "Khác", "url": "N/A", "license": "Open Access"})
        
        # Đọc cấu trúc nhanh (số dòng, số cột, danh sách cột)
        num_rows, num_cols = "N/A", "N/A"
        columns_list = []
        date_range = "N/A"
        
        try:
            if file_path.suffix == ".csv":
                df = pd.read_csv(file_path, nrows=50)
                # Đếm dòng file csv không nạp hết vào RAM
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    num_rows = sum(1 for _ in f) - 1
                num_cols = len(df.columns)
                columns_list = list(df.columns)
            elif file_path.suffix == ".gz":
                with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as f:
                    df = pd.read_csv(f, nrows=50, low_memory=False)
                    num_cols = len(df.columns)
                    columns_list = list(df.columns)
                with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as f:
                    num_rows = sum(1 for _ in f) - 1
        except Exception as err:
            num_rows, num_cols = f"Lỗi: {err}", "N/A"
            
        manifest_entries.append({
            "file": rel_path,
            "source": source_meta["source"],
            "url": source_meta["url"],
            "license": source_meta["license"],
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "sha256": sha256,
            "rows": num_rows,
            "cols": num_cols,
            "columns": columns_list
        })
        
    # Ghi manifest.json
    with open(DATA_RAW_DIR / "manifest.json", "w", encoding="utf-8") as jf:
        json.dump(manifest_entries, jf, indent=2, ensure_ascii=False)
        
    # Ghi MANIFEST.md
    with open(DATA_RAW_DIR / "MANIFEST.md", "w", encoding="utf-8") as mf:
        mf.write("# BẢN ĐĂNG KÝ TẬP TIN DỮ LIỆU THÔ (RAW DATA MANIFEST)\n\n")
        mf.write("> Tài liệu ghi nhận mã băm toàn vẹn SHA-256, dung lượng, số dòng và giấy phép của từng tệp tin thô trong `data/raw/`.\n\n")
        mf.write("| Tệp tin | Nguồn | Dung lượng | Số dòng | Số cột | Giấy phép | SHA-256 |\n")
        mf.write("|---------|-------|------------|---------|--------|-----------|---------|\n")
        for e in manifest_entries:
            mf.write(f"| `{e['file']}` | {e['source']} | {e['size_mb']} MB | {e['rows']:,} | {e['cols']} | {e['license']} | `{e['sha256'][:16]}...` |\n")
            
        mf.write("\n\n## Chi Tiết Các Cột Trong Từng Tệp Tin\n\n")
        for e in manifest_entries:
            mf.write(f"### `{e['file']}` ({e['source']})\n")
            mf.write(f"- **URL chính thức**: {e['url']}\n")
            mf.write(f"- **Dung lượng**: {e['size_bytes']:,} bytes ({e['size_mb']} MB)\n")
            mf.write(f"- **Mã SHA-256**: `{e['sha256']}`\n")
            mf.write(f"- **Số cột**: {e['cols']}\n")
            cols_preview = ", ".join([f"`{c}`" for c in e['columns'][:20]])
            if len(e['columns']) > 20:
                cols_preview += f" ... (tổng cộng {len(e['columns'])} cột)"
            mf.write(f"- **Danh sách cột**: {cols_preview}\n\n")

    print(f"  [Hoàn thành] Đã tạo MANIFEST.md và manifest.json ({len(manifest_entries)} tệp).")


def main():
    print("=================================================================")
    print(" BẮT ĐẦU QUY TRÌNH THU THẬP DỮ LIỆU THÔ (GIAI ĐOẠN 2)")
    print("=================================================================")
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    download_owid()
    download_nasa_firms()
    download_noaa_ncei()
    download_usfs_fod(limit_per_year=500)
    
    build_manifest()
    
    print("\n=================================================================")
    print(" HOÀN TẤT THU THẬP DỮ LIỆU THÔ VÀ SINH BẢN ĐĂNG KÝ MANIFEST!")
    print("=================================================================")


if __name__ == "__main__":
    main()
