# Danh Mục Nguồn Dữ Liệu (DATA SOURCES)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Trạng thái**: Khung tài liệu (Giai đoạn 1) - Sẽ cập nhật đầy đủ trong Giai đoạn 2

---

## 1. Mục Tiêu & Tiêu Chí Chọn Nguồn
Dự án nghiên cứu: **"Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng / thảm họa thiên nhiên trong 20 năm qua (2006–2025)"**.  
Trọng tâm là cháy rừng, so sánh với các thảm họa thiên nhiên khác (lũ lụt, bão, hạn hán, động đất, núi lửa...).

### Tiêu chí lựa chọn:
1. **Độ tin cậy & Thẩm quyền**: Dữ liệu từ các tổ chức khoa học, cơ quan chính phủ hoặc tổ chức quốc tế uy tín (NASA, EM-DAT/CRED, NOAA, Copernicus, Our World in Data).
2. **Phạm vi thời gian**: Bao quát giai đoạn 2006–2025.
3. **Quy mô mẫu**: Đảm bảo sau làm sạch đạt tối thiểu 5.000 dòng sự kiện thảm họa/cháy rừng hợp lệ.
4. **Tính mở & Pháp lý**: Giấy phép rõ ràng (Open Access, CC-BY, Public Domain), có thể tái lập thông qua script tải tự động hoặc hướng dẫn tải thủ công chính thức.

---

## 2. Bảng So Sánh Các Nguồn Dữ Liệu Ứng Viên

| Nguồn | Tổ chức quản lý | Phạm vi địa lý | Thời gian | Số lượng bản ghi ước tính | Giấy phép | Phương thức thu thập | Mức độ ưu tiên |
|-------|----------------|----------------|-----------|---------------------------|-----------|----------------------|----------------|
| **EM-DAT** | CRED / UCLouvain | Toàn cầu | 1900–nay (lọc 2006–2025) | ~10.000+ thảm họa (toàn cầu) | Nghiên cứu phi thương mại (Đăng ký tài khoản) | Tải thủ công / API nếu có | Rất cao (so sánh tổng thể) |
| **NASA FIRMS** (MODIS / VIIRS) | NASA Earthdata | Toàn cầu | 2000–nay | Hàng triệu điểm cháy tích cực (lấy mẫu/tổng hợp) | NASA Open Data Policy (Public Domain) | REST API / Archive Download | Rất cao (chi tiết cháy rừng) |
| **Kaggle 1.88 Million US Wildfires** / USFS FPA-FOD | US Forest Service / Karen Short | Hoa Kỳ | 1992–2020+ | ~1.88 - 2.16 triệu vụ cháy rừng | Public Domain (U.S. Govt) | Kaggle API / USFS Archive | Cao (chi tiết nguyên nhân & diện tích) |
| **Our World in Data (Natural Disasters)** | OWID / EM-DAT | Toàn cầu | 1900–2024 | Dữ liệu tổng hợp theo quốc gia/năm | CC-BY 4.0 | Direct CSV / GitHub | Trung bình (đối soát vĩ mô) |
| **Copernicus EFFIS** | European Commission | Châu Âu & Địa Trung Hải | 2000–nay | Hàng chục nghìn đám cháy | Open Access | EFFIS Web / Download | Dự phòng |
| **NOAA NCEI Storm Events** | NOAA | Hoa Kỳ / Quốc tế | 2006–2025 | Hàng trăm nghìn bản ghi | Public Domain | NOAA FTP / Direct URL | Dự phòng |

---

## 3. Nhật Ký Thu Thập Dữ Liệu (Data Download Log)
*(Sẽ được điền trong Giai đoạn 2 khi chạy script `src/01_download.py`)*

| Ngày tải | Tên file lưu tại `data/raw/` | Nguồn (URL) | Định dạng gốc | Kích thước | Số dòng | Ghi chú & Giấy phép |
|----------|-----------------------------|-------------|---------------|------------|---------|---------------------|
| *TODO*   | *TODO*                      | *TODO*      | *TODO*        | *TODO*     | *TODO*  | *TODO*              |

---

## 4. Hướng Dẫn Tải Dữ Liệu Thủ Công (Nếu Nguồn Yêu Cầu Đăng Ký)
*(Đối với EM-DAT hoặc NASA FIRMS khi tải tập dữ liệu lớn cần token/login)*
- **EM-DAT**:
  1. Truy cập `https://public.emdat.be/`
  2. Đăng ký tài khoản học thuật / phi thương mại.
  3. Chọn dải thời gian: `2006-01-01` đến `2025-12-31`. Chọn Disaster Group: `Natural`.
  4. Xuất định dạng CSV / Excel và lưu vào `data/raw/emdat_raw.csv`.
