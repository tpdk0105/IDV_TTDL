# Từ Điển Dữ Liệu (DATA DICTIONARY)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Trạng thái**: Khung tài liệu định nghĩa chuẩn hóa các trường dữ liệu (Giai đoạn 1)

---

## 1. Tổng Quan Cấu Trúc Tập Dữ Liệu `master_clean.csv`
Tập dữ liệu sau làm sạch `data/clean/master_clean.csv` đóng vai trò là bảng nguồn tổng thể (Master Dataset) phục vụ phân rã sang mô hình hình sao (Star Schema).

- **Số dòng tối thiểu cam kết**: $\ge 5.000$ dòng.
- **Phạm vi thời gian**: 2005–2024.
- **Quy tắc đặt tên cột**: Tiếng Anh, chữ thường, nối bằng dấu gạch dưới (`snake_case`).

---

## 2. Danh Mục Các Trường Dữ Liệu (Field Specifications)

| Tên Cột | Kiểu Dữ Liệu | Đơn Vị / Miền Giá Trị | Cho Phép NULL | Mô Tả Ý Nghĩa | Nguồn & Quy Tắc Xử Lý |
|---------|--------------|------------------------|---------------|---------------|------------------------|
| `event_id` | String | Định dạng `DIS-YYYY-XXXXX` | Không | Khóa định danh duy nhất của mỗi sự kiện thảm họa/vụ cháy | Tạo mới hoặc chuẩn hóa từ ID gốc |
| `disaster_type` | String | `Wildfire`, `Flood`, `Storm`, `Drought`, `Earthquake`, ... | Không | Loại thảm họa chính (Trọng tâm: Wildfire) | Chuẩn hóa danh mục |
| `disaster_subtype` | String | Chi tiết phân loại thảm họa | Có | Phân loại chi tiết (vd: Forest fire, Flash flood) | Chuẩn hóa danh mục |
| `country_iso3` | String | Mã ISO 3166-1 alpha-3 (3 ký tự) | Không | Mã định danh quốc gia chuẩn quốc tế (vd: `VNM`, `USA`, `AUS`) | Chuẩn hóa qua `country_converter` |
| `country_name` | String | Tên quốc gia chuẩn tiếng Anh | Không | Tên quốc gia đầy đủ | Tra cứu theo chuẩn ISO3 |
| `region` | String | Tên vùng địa lý | Có | Vùng lãnh thổ hành chính hoặc địa lý | Chuẩn hóa |
| `continent` | String | `Asia`, `Europe`, `Americas`, `Africa`, `Oceania` | Không | Châu lục diễn ra sự kiện | Chuẩn hóa theo ISO3 |
| `latitude` | Float | [-90.0, 90.0] | Có | Vĩ độ trọng tâm sự kiện thảm họa | Kiểm tra miền giá trị hợp lệ |
| `longitude` | Float | [-180.0, 180.0] | Có | Kinh độ trọng tâm sự kiện thảm họa | Kiểm tra miền giá trị hợp lệ |
| `start_date` | Date | `YYYY-MM-DD` | Không | Ngày bắt đầu sự kiện (thuộc khoảng 2005–2024) | Chuẩn hóa ngày chuẩn ISO |
| `end_date` | Date | `YYYY-MM-DD` | Có | Ngày kết thúc sự kiện ($\ge$ `start_date`) | Chuẩn hóa ngày chuẩn ISO |
| `year` | Integer | [2005, 2024] | Không | Năm diễn ra sự kiện | Trích xuất từ `start_date` |
| `month` | Integer | [1, 12] | Không | Tháng diễn ra sự kiện | Trích xuất từ `start_date` |
| `cause_name` | String | `Lightning`, `Human Negligence`, `Arson`, `Unknown`, ... | Có | Chi tiết nguyên nhân phát sinh thảm họa / cháy | Chuẩn hóa chuỗi ký tự |
| `cause_group` | String | `Natural`, `Human`, `Unknown` | Không | Nhóm nguyên nhân phân loại chính | Quy nạp từ `cause_name` hoặc dự đoán ML |
| `burned_area_ha_raw` | Float | Hecta (ha) | Có | Diện tích cháy rừng thu thập thô ban đầu | Lưu vết gốc phục vụ đối soát |
| `burned_area_ha` | Float | $\ge 0.0$ Hecta (ha) | Có | Diện tích cháy rừng đã quy đổi đồng nhất đơn vị ha | Quy đổi từ acres, km² về ha |
| `burned_area_ha_is_imputed` | Boolean | `True`, `False` | Không | Cờ xác định giá trị diện tích cháy được điền bởi thuật toán ML (KNN/Iterative) | Đánh dấu độ tin cậy dữ liệu |
| `damage_usd_raw` | Float | USD | Có | Thiệt hại kinh tế thô ban đầu | Lưu vết gốc phục vụ đối soát |
| `damage_usd` | Float | $\ge 0.0$ USD | Có | Thiệt hại kinh tế ước tính quy về USD | Quy đổi tiền tệ, xử lý đơn vị nghìn/triệu USD |
| `damage_usd_is_imputed` | Boolean | `True`, `False` | Không | Cờ xác định giá trị thiệt hại kinh tế được điền bởi mô hình ML | Đánh dấu độ tin cậy dữ liệu |
| `deaths` | Integer | $\ge 0$ | Có | Số người thiệt mạng do sự kiện | Kiểm tra $\ge 0$ |
| `deaths_is_imputed` | Boolean | `True`, `False` | Không | Cờ xác định số người chết được điền bởi mô hình ML | Đánh dấu độ tin cậy dữ liệu |
| `injured` | Integer | $\ge 0$ | Có | Số người bị thương | Kiểm tra $\ge 0$ |
| `affected` | Integer | $\ge 0$ | Có | Tổng số người bị ảnh hưởng trực tiếp | Kiểm tra $\ge 0$ |
| `has_deaths_data` | Boolean | `True`, `False` | Không | `True` nếu sự kiện có số liệu `deaths`; `False` nếu `deaths` trống | Tạo bằng `deaths.notna()`. Xem mục 4 |
| `has_damage_data` | Boolean | `True`, `False` | Không | `True` nếu sự kiện có số liệu thiệt hại kinh tế; `False` nếu `damage_usd` trống | Tạo bằng `damage_usd.notna()`. Xem mục 4 |
| `month_known` | Boolean | `True`, `False` | Không | `True` nếu biết tháng bắt đầu sự kiện; `False` nếu `month` trống | Tạo bằng `month.notna()`. Xem mục 4 |
| `is_outlier_ml` | Boolean | `True`, `False` | Không | Cờ phát hiện bất thường bởi Isolation Forest & LOF | Phân tích ngoại lai ML |
| `outlier_score` | Float | Số thực (Điểm bất thường) | Có | Mức độ bất thường do thuật toán Isolation Forest tính toán | Giá trị càng âm độ bất thường càng cao |
| `cause_is_predicted` | Boolean | `True`, `False` | Không | Cờ xác định nhóm nguyên nhân được phân loại bởi Random Forest Classifier | Chỉ gán True khi xác suất $\ge 0.7$ |
| `source_name` | String | Tên nguồn dữ liệu gốc | Không | Ghi rõ nguồn trích xuất dữ liệu (EM-DAT, FIRMS, USFS...) | Đối chiếu nguồn gốc dữ liệu |

---

## 3. Quy Ước Giá Trị Thiếu (Missing Values)
- Chuỗi ký tự thiếu: Biểu diễn bằng `NULL` (tránh các chuỗi `"None"`, `"N/A"`, `"-"`, `""`).
- Biến số thiếu: Giá trị `NULL` trong SQLite / `NaN` trong Pandas.
- Cột có tỷ lệ thiếu $> 60\%$: Tuyệt đối không điền bằng ML, giữ nguyên `NULL` và công bố trong báo cáo hạn chế dữ liệu.

---

## 4. Cột Cờ Dữ Liệu Thiếu (`has_deaths_data`, `has_damage_data`, `month_known`)

### 4.1. Vì sao cần các cột này?
EM-DAT **không ghi số 0**. Một ô trống ở `deaths` hoặc `damage_usd` có thể mang một trong hai nghĩa:
- Sự kiện thực sự không có người chết / không có thiệt hại, **hoặc**
- Có thiệt hại nhưng **không có số liệu** được báo cáo.

Không thể phân biệt hai trường hợp này, nên **tuyệt đối không `fillna(0)`** các cột thiệt hại. Điền 0 sẽ kéo trung bình và trung vị xuống sai lệch. Thay vào đó, giữ nguyên `NaN` và dùng 3 cột cờ để biết dòng nào có số liệu.

### 4.2. Ý nghĩa và số liệu (`data/interim/emdat_clean.csv`, 7.545 dòng)

| Cột cờ | `True` | `False` | Số dòng `False` | Ghi chú |
|---|---|---|---|---|
| `has_deaths_data` | Có số người chết | `deaths` trống | 2.146 (28,4%) | |
| `has_damage_data` | Có số thiệt hại kinh tế | `damage_usd` trống | 5.006 (66,3%) | Thiếu nhiều nhất, cần nêu trong báo cáo |
| `month_known` | Biết tháng bắt đầu | `month` trống | 45 (0,6%) | 44 Drought + 1 Flood. Hạn hán thường không có ngày bắt đầu rõ ràng |

Tỷ lệ có số liệu khác nhau rõ rệt giữa các châu lục:

| Châu lục | `has_deaths_data` | `has_damage_data` |
|---|---|---|
| Africa | 66,6% | **12,0%** |
| Americas | 68,7% | 43,5% |
| Asia | 79,1% | 37,8% |
| Europe | 67,3% | 26,7% |
| Oceania | 45,5% | 48,0% |

Ví dụ: thiệt hại kinh tế ở châu Phi "trông thấp" một phần vì **chỉ 12% sự kiện có số liệu**, không hẳn vì thiệt hại thực tế thấp.

### 4.3. Quy tắc sử dụng

| Loại phân tích | Cách làm |
|---|---|
| **Đếm tần suất** (số sự kiện) | Dùng toàn bộ dữ liệu, **không lọc** theo cột cờ |
| **Tổng** thiệt hại / người chết | Dùng toàn bộ dữ liệu. `sum()` của pandas và `SUM()` của Tableau/SQL tự bỏ qua giá trị trống |
| **Trung bình / trung vị** thiệt hại | Chỉ tính trên dòng có số liệu: lọc `has_damage_data == True` (hoặc `has_deaths_data == True`) |
| **Phân tích theo mùa / tháng** | Lọc `month_known == True` |
| **So sánh giữa châu lục / quốc gia** | Luôn kèm tỷ lệ có số liệu (bảng 4.2) để người xem không hiểu sai |

Ví dụ trong pandas:

```python
# Trung vị thiệt hại theo châu lục (chỉ các sự kiện có số liệu)
df[df["has_damage_data"]].groupby("continent")["damage_usd"].median()

# Số sự kiện theo tháng (bỏ các sự kiện không rõ tháng)
df[df["month_known"]].groupby("month").size()

# Tỷ lệ sự kiện có số liệu thiệt hại theo châu lục
df.groupby("continent")["has_damage_data"].mean().mul(100).round(1)
```

Trong Tableau: kéo cột cờ vào **Filters** và chọn `True` cho các biểu đồ trung bình / trung vị, hoặc đưa ra làm bộ lọc để người xem tự chọn.

### 4.4. Lưu ý
- Cột cờ phải được tạo **trước** khi xoá các cột trung gian `damage_k_usd`, `damage_adj_k_usd`, hoặc tạo từ `damage_usd` sau khi quy đổi.
- Khi nạp vào SQLite, `deaths` có ràng buộc `NOT NULL DEFAULT 0` trong `sql/schema.sql`. Nếu nhóm giữ ràng buộc này và điền 0, **bắt buộc** dùng `has_deaths_data` để phân biệt "0 thật" với "không có số liệu".
