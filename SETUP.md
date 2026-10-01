# HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG PHÁT TRIỂN (SETUP GUIDE)

Tài liệu này hướng dẫn chi tiết từng bước cài đặt và kiểm tra môi trường cho cả 3 thành viên trên hệ điều hành **Windows**, **macOS** hoặc **Linux**.

---

## 1. Yêu Cầu Tiên Quyết (Prerequisites)
1. **Git**: Phiên bản $\ge 2.30$ ([Tải về tại đây](https://git-scm.com/)).
2. **Python**: Phiên bản 3.11 hoặc 3.12 (Khuyến nghị dùng [Miniconda](https://docs.conda.io/en/latest/miniconda.html) hoặc cài đặt trực tiếp từ [python.org](https://www.python.org/)).
3. **Node.js & npm**: Phiên bản Node.js 20 LTS ([Tải về tại đây](https://nodejs.org/)).

---

## 2. Các Bước Cài Đặt Chi Tiết

### Bước 2.1: Clone Repository
Mở Terminal / PowerShell và thực hiện clone repo về máy cá nhân:
```bash
git clone https://github.com/tpdk0105/IDV_TTDL.git
cd IDV_TTDL
```

### Bước 2.2: Thiết Lập Môi Trường Python

#### Cách 1: Sử dụng Conda / Miniconda (Khuyến khích)
```bash
# Tạo môi trường ảo với Python 3.11
conda env create -f environment.yml

# Kích hoạt môi trường
conda activate idv-ttdl
```

#### Cách 2: Sử dụng Python venv chuẩn
```bash
# Trên Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Trên macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

# Nâng cấp pip và cài đặt thư viện đã ghim
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 2.3: Thiết Lập Môi Trường Node.js & Dashboard Vendor
Thực hiện cài đặt các công cụ phát triển giao diện web và copy thư viện Apache ECharts vào dự án:
```bash
# Cài đặt các gói phụ thuộc Node
npm install

# Sao chép thư viện ECharts offline vào dashboard/js/vendor/
npm run vendor
```

### Bước 2.4: Thiết Lập File Biến Môi Trường (Optional)
Tạo file `.env` từ `.env.example` nếu cần dùng Kaggle API để tự động tải dữ liệu thô:
```bash
# Trên Windows PowerShell:
Copy-Item .env.example .env

# Trên macOS / Linux:
cp .env.example .env
```
Mở `.env` và điền thông tin tài khoản Kaggle của bạn (lấy tại `kaggle.com/settings` $\to$ Create New Token).

---

## 3. Kiểm Tra Môi Trường Hoạt Động (Verification)

### 3.1. Kiểm tra môi trường Python
Chạy câu lệnh sau trong terminal:
```bash
python -c "import pandas, numpy, sklearn, sqlalchemy, rapidfuzz; print('>>> PYTHON ENVIRONMENT OK! All core libraries loaded successfully.')"
```
Nếu màn hình xuất ra dòng `>>> PYTHON ENVIRONMENT OK!` nghĩa là môi trường Python đã sẵn sàng 100%.

### 3.2. Kiểm tra Dashboard cục bộ
Khởi động máy chủ web phát triển nội bộ:
```bash
npm run start
```
Mở trình duyệt truy cập: `http://localhost:8080`. Bấm `Ctrl + C` để dừng máy chủ khi hoàn tất.

---

## 4. Xử Lý Các Lỗi Thường Gặp (Troubleshooting)

### Lỗi 1: PowerShell chặn kích hoạt venv (`UnauthorizedAccess` / `ExecutionPolicy`)
- **Nguyên nhân**: Chính sách bảo mật của Windows hạn chế chạy script PowerShell.
- **Khắc phục**: Mở PowerShell với quyền Administrator và chạy lệnh:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Lỗi 2: Trùng cổng mạng `8080` khi chạy `npm run start`
- **Nguyên nhân**: Một ứng dụng khác (vd: Tomcat, Jenkins, Docker) đang chiếm cổng 8080.
- **Khắc phục**: Đổi cổng chạy trong `package.json` hoặc chạy trực tiếp lệnh:
  ```bash
  npx http-server dashboard -p 8085 -c-1 -o
  ```

### Lỗi 3: Xung đột mã hóa ký tự tiếng Việt trên Windows CMD
- **Khắc phục**: Chuyển bảng mã console sang UTF-8 trước khi chạy script:
  ```cmd
  chcp 65001
  ```

### Lỗi 4: Khóa tệp SQLite (`sqlite3.OperationalError: database is locked`)
- **Nguyên nhân**: Đang có một tiến trình hoặc công cụ xem DB (DBeaver, DB Browser for SQLite) giữ khóa ghi.
- **Khắc phục**: Tắt các phần mềm xem CSDL đang mở kết nối trước khi chạy script nạp `05_build_db.py`.
