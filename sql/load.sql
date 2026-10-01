-- ==============================================================================
-- KỊCH BẢN NẠP DỮ LIỆU TỪ CÁC TỆP TIN CSV VÀO CSDL SQLITE
-- Tệp tin: sql/load.sql
-- Người phụ trách: Thành viên 2 (Kỹ sư Mô hình Dữ liệu)
-- Lưu ý: SQLite CLI hỗ trợ lệnh .import, hoặc có thể nạp thông qua Python 05_build_db.py
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- Nạp các bảng Dimension trước
-- .mode csv
-- .import data/tables/dim_date.csv dim_date
-- .import data/tables/dim_location.csv dim_location
-- .import data/tables/dim_disaster_type.csv dim_disaster_type
-- .import data/tables/dim_cause.csv dim_cause
-- .import data/tables/dim_source.csv dim_source

-- Nạp các bảng Fact sau
-- .import data/tables/fact_disaster_event.csv fact_disaster_event
-- .import data/tables/fact_wildfire_detail.csv fact_wildfire_detail
