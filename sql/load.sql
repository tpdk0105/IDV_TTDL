-- ==============================================================================
-- KỊCH BẢN NẠP DỮ LIỆU TỪ CÁC TỆP TIN CSV VÀO CSDL SQLITE
-- Tệp tin: sql/load.sql
-- Người phụ trách: Thành viên 2 (Kỹ sư Mô hình Dữ liệu)
-- Lưu ý: SQLite CLI hỗ trợ lệnh .import, hoặc có thể nạp thông qua Python src/05_build_db.py
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- Nạp các bảng Dimension trước
-- .mode csv
-- .import data/tables/dim_date.csv dim_date
-- .import data/tables/dim_county.csv dim_county
-- .import data/tables/dim_cause.csv dim_cause

-- Nạp các bảng Fact sau
-- .import data/tables/fact_fire_incident.csv fact_fire_incident
-- .import data/tables/fact_structure_damage.csv fact_structure_damage

