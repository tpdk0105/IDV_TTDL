"""
Script to rebuild IDV_Nhom17.docx with:
1. New Chapter 3: Mô hình hóa và phân rã các bảng dữ liệu (Data Modeling & Schema Splitting)
   - Lý do phải tách (khử dư thừa, tránh bất thường cập nhật, chuẩn hóa Star Schema 3NF)
   - Sử dụng gì để tách và tách từ những tập dữ liệu nào (Python Pandas src/04_split_tables.py từ master_clean, DINS, ICS-209, Demographics, Census)
   - Đặc tả tổng quan 5 bảng: dim_cause.csv, dim_county.csv, dim_date.csv, fact_fire_incident.csv, fact_structure_damage.csv
   - Công dụng từng bảng và mục đích phục vụ Tableau (Data Relationships, tránh Cartesian duplicate, hỗ trợ LOD expressions)
2. Chapter 4 (Thiết kế Dashboard):
   - Không sử dụng bảng mà viết thành các dòng có cấu trúc
   - Chừa khung placeholder rõ ràng để dán hình ảnh cho 3 Dashboard, 10 Sheet và 4 Thẻ KPI
   - Calculated fields viết thành dòng, không dùng bảng
3. Chapter 5 (Khai phá Insight & Storytelling):
   - Không dùng bảng, viết thành dòng phân tích đối chiếu
   - Chừa khung placeholder dán hình ảnh sau mỗi Story Point (Point 1, Point 2, Point 3)
4. Giữ nguyên 7 biểu đồ EDA và ML đã kết xuất từ dự án
5. Danh mục 8 chương cập nhật đồng bộ lên Mục lục ở đầu tài liệu.
"""

import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DOC_PATH = Path("IDV_Nhom17.docx")
BACKUP_PATH = Path("IDV_Nhom17_backup.docx")

COLOR_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)    # Deep Navy Blue for Chapter Headings
COLOR_SECONDARY = RGBColor(0x2B, 0x4C, 0x7E)  # Slate Blue for Section Headings
COLOR_TEXT = RGBColor(0x1A, 0x1A, 0x1A)       # Dark Gray / Off Black for text
COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)      # Muted Gray for captions

HEX_HEADER_BG = "1F4E79"
HEX_ZEBRA_BG = "F2F5F8"
HEX_CALLOUT_BG = "F0F4F8"
HEX_PLACEHOLDER_BG = "F8FAFC"
HEX_BORDER = "CCCCCC"


def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)


def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="{top}" w:type="dxa"/>'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'  <w:left w:w="{left}" w:type="dxa"/>'
        f'  <w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    cell._tc.get_or_add_tcPr().append(tcMar)


def set_table_borders(table, color=HEX_BORDER):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_chapter_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_SECONDARY
    return p


def add_sub_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = COLOR_TEXT
    return p


def add_body_paragraph(doc, text, bold_prefix=None, italic_prefix=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(13)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_TEXT
    if italic_prefix:
        r_i = p.add_run(italic_prefix)
        r_i.font.name = "Times New Roman"
        r_i.font.size = Pt(13)
        r_i.font.italic = True
        r_i.font.color.rgb = COLOR_TEXT
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.color.rgb = COLOR_TEXT
    return p


def add_bullet_point(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.25
    
    r_bullet = p.add_run("•  ")
    r_bullet.font.name = "Times New Roman"
    r_bullet.font.size = Pt(13)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = COLOR_SECONDARY
    
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(13)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_TEXT
    
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.color.rgb = COLOR_TEXT
    return p


def add_callout(doc, text, title="GHI CHÚ HỌC THUẬT / INSIGHT CHUYÊN SÂU:"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_HEADER_BG}"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    
    r_t = p.add_run(title + "\n")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(12)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    
    r_c = p.add_run(text)
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(12)
    r_c.font.italic = True
    r_c.font.color.rgb = COLOR_TEXT
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)


def add_image_placeholder(doc, placeholder_title, placeholder_desc):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_PLACEHOLDER_BG)
    set_cell_margins(cell, top=260, bottom=260, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_HEADER_BG}"/>'
        f'  <w:left w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_HEADER_BG}"/>'
        f'  <w:bottom w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_HEADER_BG}"/>'
        f'  <w:right w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_HEADER_BG}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.2
    
    r1 = p.add_run(f"📷 [KHUNG DÁN HÌNH ẢNH: {placeholder_title.upper()}]\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_PRIMARY
    
    r2 = p.add_run(f"({placeholder_desc})")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)


def add_academic_table(doc, title, headers, data, col_widths=None):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(3)
    r_cap = p_cap.add_run(title)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(12)
    r_cap.font.bold = True
    r_cap.font.color.rgb = COLOR_PRIMARY

    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    hdr_row = tbl.rows[0]
    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_values in enumerate(data):
        row = tbl.rows[r_idx + 1]
        bg = HEX_ZEBRA_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = row.cells[c_idx]
            if bg != "FFFFFF":
                set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            val_str = str(val)
            if len(val_str) <= 15 or val_str.startswith("#"):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val_str)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.font.color.rgb = COLOR_TEXT

    if col_widths and len(col_widths) == len(headers):
        for row in tbl.rows:
            for c_idx, w in enumerate(col_widths):
                row.cells[c_idx].width = Inches(w)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)


def add_academic_figure(doc, img_path, caption_title, caption_desc=None, width_inches=6.0):
    if not Path(img_path).exists():
        print(f"Warning: Image {img_path} not found.")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.add_run().add_picture(str(img_path), width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    
    r_title = p_cap.add_run(caption_title)
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11)
    r_title.font.bold = True
    r_title.font.italic = True
    r_title.font.color.rgb = COLOR_MUTED

    if caption_desc:
        r_desc = p_cap.add_run(f" - {caption_desc}")
        r_desc.font.name = "Times New Roman"
        r_desc.font.size = Pt(11)
        r_desc.font.italic = True
        r_desc.font.color.rgb = COLOR_MUTED


def add_toc_line(doc, title, page, level=1):
    p = doc.add_paragraph(style=f'toc {level}')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(3 if level == 1 else 1)
    p.paragraph_format.space_after = Pt(3 if level == 1 else 1)
    p.paragraph_format.line_spacing = 1.15
    if level == 2:
        p.paragraph_format.left_indent = Inches(0.25)
    elif level == 3:
        p.paragraph_format.left_indent = Inches(0.5)

    r_title = p.add_run(title)
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(13)
    r_title.font.bold = (level == 1)
    r_title.font.color.rgb = COLOR_PRIMARY if level == 1 else COLOR_TEXT

    r_tab = p.add_run("\t")
    r_tab.font.name = "Times New Roman"

    r_page = p.add_run(str(page))
    r_page.font.name = "Times New Roman"
    r_page.font.size = Pt(13)
    r_page.font.bold = (level == 1)
    r_page.font.color.rgb = COLOR_PRIMARY if level == 1 else COLOR_TEXT


def build_table_of_contents(doc):
    toc_entries = [
        ("CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI & MÔ TẢ TẬP DỮ LIỆU", 1, 1),
        ("1.1. Bối Cảnh Thực Tiễn và Tính Cấp Thiết của Đề Tài", 1, 2),
        ("1.2. Mục Tiêu Nghiên Cứu và 3 Câu Hỏi Phân Tích Cốt Lõi", 1, 2),
        ("1.3. Khảo Sát và Mô Tả Chi Tiết 5 Bộ Dữ Liệu Thu Thập (Kèm Link Truy Cập)", 2, 2),
        ("1.4. Từ Điển Dữ Liệu & Đặc Tả Thuộc Tính Cốt Lõi", 3, 2),
        ("1.5. Quy Trình Thu Thập Tự Động Hóa & Toàn Vẹn Dữ Liệu (SHA-256)", 4, 2),
        
        ("CHƯƠNG 2: QUY TRÌNH TIỀN XỬ LÝ & KHÁM PHÁ DỮ LIỆU (EDA)", 5, 1),
        ("2.1. Đánh Giá Chất Lượng Dữ Liệu Ban Đầu (Data Quality Assessment)", 5, 2),
        ("2.2. Quy Trình Làm Sạch Theo Quy Tắc (Rule-based Cleaning)", 6, 2),
        ("2.3. Ứng Dụng Học Máy (Machine Learning) Trong Làm Sạch Dữ Liệu", 7, 2),
        ("2.3.1. Mô hình 1: Isolation Forest & LOF Phát Hiện Dị Biệt Ngoại Lai", 7, 3),
        ("2.3.2. Mô hình 2: Điền Khuyết Thiếu Bằng Iterative Imputer (MICE)", 8, 3),
        ("2.4. Phân Tích Khám Phá Dữ Liệu Tĩnh (Exploratory Data Analysis - EDA)", 8, 2),
        
        ("CHƯƠNG 3: MÔ HÌNH HÓA VÀ PHÂN RÃ CÁC BẢNG DỮ LIỆU (DATA MODELING & SCHEMA SPLITTING)", 11, 1),
        ("3.1. Lý Do & Sự Cần Thiết Của Việc Phân Rã Dữ Liệu Thành Nhiều Bảng", 11, 2),
        ("3.2. Công Cụ Thực Hiện & Nguồn Dữ Liệu Đầu Vào Dùng Để Phân Rã", 12, 2),
        ("3.3. Đặc Tả Chi Tiết & Công Dụng Của 5 Bảng Dữ Liệu Sau Khi Tách (Star Schema)", 12, 2),
        ("3.3.1. Bảng dim_date.csv - Thứ Bậc Thời Gian Chuẩn Hóa 20 Năm", 13, 3),
        ("3.3.2. Bảng dim_county.csv - Danh Mục Địa Lý & Dân Số 58 Hạt California", 13, 3),
        ("3.3.3. Bảng dim_cause.csv - Phân Nhóm 19 Mã Căn Nguyên Hỏa Hoạn", 13, 3),
        ("3.3.4. Bảng fact_fire_incident.csv - Bảng Sự Cố Trung Tâm (Fact Lõi)", 14, 3),
        ("3.3.5. Bảng fact_structure_damage.csv - Bảng Chi Tiết Tổn Thất Công Trình", 14, 3),
        ("3.4. Mục Đích Phân Rã & Lợi Ích Vượt Trội Khi Trực Quan Hóa Trên Tableau", 15, 2),
        ("3.4.1. Thiết Lập Mô Hình Quan Hệ (Tableau Data Relationships / Noodle Model)", 15, 3),
        ("3.4.2. Quy Tắc Toàn Vẹn Tham Chiếu & Cảnh Báo Tránh Lệch Mã Hạt", 15, 3),
        
        ("CHƯƠNG 4: THIẾT KẾ DASHBOARD & ĐẶC TẢ CHI TIẾT 10 BIỂU ĐỒ TABLEAU", 16, 1),
        ("4.1. Nguyên Lý Thiết Kế Trực Quan & Tiêu Chuẩn Trợ Năng WCAG 2.1 AA", 16, 2),
        ("4.2. Bố Cục Giao Diện & Luồng Tương Tác Của Hệ Thống 3 Dashboards", 16, 2),
        ("4.2.1. Cấu Trúc 3 Dashboards Chuyên Đề & Khung Dán Ảnh Giao Diện", 16, 3),
        ("4.2.2. Luồng Tương Tác Đa Cấp (Filters, Actions, Drill-down, Parameters)", 18, 3),
        ("4.3. Đặc Tả Chi Tiết 10 Biểu Đồ Trực Quan Hóa & Khung Dán Ảnh Từng Sheet", 19, 2),
        ("4.3.1. Sheet 01: Line Chart 2 Đường - Mùa Cháy Theo Tháng & 2 Thập Kỷ (01_Line_Season)", 19, 3),
        ("4.3.2. Sheet 02: Stacked Area Chart - Cơ Cấu Nguyên Nhân 20 Năm (02_Area_Cause_Trend)", 20, 3),
        ("4.3.3. Sheet 03: Bản Đồ Địa Lý 2 Lớp - Mật Độ & Diện Tích Cháy (03_Map_County)", 20, 3),
        ("4.3.4. Sheet 04: Donut Chart 2 Tầng - Tỷ Trọng Vụ Cháy Theo Căn Nguyên (04_Donut_Cause_Share)", 21, 3),
        ("4.3.5. Sheet 05: Horizontal Bar Chart - Top N Hạt Mất Nhiều Công Trình (05_Bar_Top_Counties)", 21, 3),
        ("4.3.6. Sheet 06: Heatmap Ma Trận - Nhóm Nguyên Nhân × Quy Mô Diện Tích (06_Heatmap_Cause_Size)", 22, 3),
        ("4.3.7. Sheet 07: Treemap 1 Tầng - Phân Bổ Công Trình Phá Hủy Theo Loại Hình (07_Treemap_Damage)", 23, 3),
        ("4.3.8. Sheet 08: Scatter Plot - Hồi Quy Tuyến Tính Log-Log Diện Tích & Thiệt Hại (08_Scatter_Regression)", 23, 3),
        ("4.3.9. Sheet 09: Combo Pareto Chart - Quy Luật 80/20 Tổn Thất Tài Sản (09_Pareto_Damage)", 24, 3),
        ("4.3.10. Sheet 10: Diverging Bar Chart - Số Vụ Cháy So Với Mức Trung Bình 20 Năm (10_Diverging_vs_Avg)", 25, 3),
        ("4.3.11. Hệ Thống 4 Thẻ Chỉ Số KPI Tổng Quan Vĩ Mô (KPI_1 → KPI_4)", 25, 3),
        ("4.4. Hệ Thống Các Trường Tính Toán (Calculated Fields) & Parameters Trên Tableau", 26, 2),
        
        ("CHƯƠNG 5: KHAI PHÁ INSIGHT & KỂ CHUYỆN BẰNG DỮ LIỆU (DATA STORYTELLING)", 27, 1),
        ("5.1. Kiến Trúc Tableau Story Dẫn Dắt 3 Phân Đoạn Tự Sự", 27, 2),
        ("5.2. Story Point 1: Biến Động Chu Kỳ 20 Năm & Xu Thế Mùa Cháy Kéo Dài", 27, 2),
        ("5.3. Story Point 2: Tâm Chấn Thảm Họa Địa Lý & Quy Luật Bất Cân Xứng Pareto 80/20", 29, 2),
        ("5.4. Story Point 3: Nghịch Lý Căn Nguyên Bùng Phát & Khả Năng Dự Báo Thiệt Hại", 30, 2),
        ("5.5. Đề Xuất Giải Pháp & Khuyến Nghị Chính Sách Dựa Trên Bằng Chứng Dữ Liệu", 32, 2),
        
        ("CHƯƠNG 6: MÔ HÌNH HỌC MÁY DỰ BÁO XU THẾ & TÍCH HỢP TRỰC QUAN HÓA", 33, 1),
        ("6.1. Cơ Sở Lý Thuyết & Xây Dựng Thuật Toán Dự Báo Trên Python", 33, 2),
        ("6.1.1. Mô hình Hồi quy Tuyến tính Log-Log Giữa Quy Mô Diện Tích & Tổn Thất Công Trình", 33, 3),
        ("6.1.2. Mô hình Hồi quy Tuyến tính Cho Chuỗi Thời Gian 10 Năm (2026–2035) & Rolling Origin", 34, 3),
        ("6.1.3. Mô hình Phân Lớp Cấp Độ Rủi Ro Thảm Họa (Risk Classification)", 35, 3),
        ("6.2. Tích Hợp Kết Quả Dự Báo Lên Dashboard Trực Quan Hóa (Barem 0.5 Điểm)", 36, 2),
        
        ("CHƯƠNG 7: HƯỚNG DẪN CÀI ĐẶT/SỬ DỤNG & LINK VIDEO DEMO", 38, 1),
        ("7.1. Hướng Dẫn Cài Đặt Môi Trường & Tái Tạo Toàn Bộ Pipeline Dữ Liệu", 38, 2),
        ("7.2. Hướng Dẫn Mở & Tương Tác Với Dashboard (Tableau Desktop / Web Nhúng)", 39, 2),
        ("7.3. Kịch Bản Thuyết Trình Demo Chi Tiết Từng Phút Trước Hội Đồng (5–7 Phút)", 39, 2),
        ("7.4. Liên Kết Video Demo Chính Thức, Video Backup Tóm Tắt & Kho Lưu Trữ GitHub", 41, 2),
        
        ("CHƯƠNG 8: KẾT LUẬN & TÀI LIỆU THAM KHẢO", 42, 1),
        ("8.1. Tổng Kết Các Kết Quả Đạt Được & Đóng Góp Chính Của Đề Tài", 42, 2),
        ("8.2. Hạn Chế Tồn Tại & Định Hướng Nghiên Cứu Mở Rộng Trong Tương Lai", 42, 2),
        ("8.3. Danh Mục Tài Liệu Tham Khảo Chuẩn IEEE (Ghi Đầy Đủ Link Nguồn Crawl Dữ Liệu)", 43, 2),
    ]

    for title, page, level in toc_entries:
        add_toc_line(doc, title, page, level)

    doc.add_page_break()
def build_chapter_1(doc):
    add_chapter_title(doc, "CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI & MÔ TẢ TẬP DỮ LIỆU")
    
    add_section_heading(doc, "1.1. Bối Cảnh Thực Tiễn và Tính Cấp Thiết của Đề Tài")
    add_body_paragraph(
        doc,
        "Bang California, tọa lạc tại bờ Tây Hoa Kỳ, sở hữu kiểu khí hậu Địa Trung Hải đặc trưng với mùa đông ẩm ướt và mùa hè – thu kéo dài khô nóng. Đây là một trong những khu vực có mức độ đe dọa hỏa hoạn tự nhiên khốc liệt nhất hành tinh. Tuy nhiên, trong hai thập kỷ qua (giai đoạn 2006–2025), bức tranh cháy rừng tại California đã trải qua những biến động căn bản về cả quy mô, tần suất bùng phát lẫn sức tàn phá hủy diệt do sự cộng hưởng của ba yếu tố then chốt:"
    )
    add_bullet_point(
        doc,
        "Hiện tượng nóng lên toàn cầu đã kích hoạt đợt siêu hạn hán (Megadrought) kéo dài hơn 20 năm tại miền Tây Bắc Mỹ, làm độ ẩm của đất và thảm thực vật giảm xuống mức thấp kỷ lục. Ước tính có hơn 100 triệu cây rừng bị chết khô tích tụ trong các cánh rừng Sierra Nevada, tạo thành một kho nhiên liệu khổng lồ cực kỳ dễ bắt lửa.",
        "Biến đổi khí hậu & Siêu hạn hán kéo dài: "
    )
    add_bullet_point(
        doc,
        "Các đợt gió mùa khô nóng mang tính thảm họa như gió Santa Ana ở khu vực Nam California (vận tốc gió giật có thể vượt 100 km/h kèm độ ẩm tương đối dưới 10%) và gió Diablo ở Bắc California thổi bùng các đốm lửa nhỏ thành những cơn bão lửa lan nhanh với tốc độ không thể kiểm soát.",
        "Điều kiện khí tượng cực đoan: "
    )
    add_bullet_point(
        doc,
        "Tốc độ đô thị hóa nhanh chóng đẩy hàng trăm ngàn công trình nhà ở và khu dân cư lấn sâu vào các sườn đồi, rừng thông và thảm cây bụi chaparral. Khi cháy rừng bùng phát, ngọn lửa nhanh chóng lan vào các khu dân cư, biến thảm họa tự nhiên thành thảm họa nhân đạo và tổn thất tài sản nặng nề.",
        "Sự mở rộng của vùng ranh giới tiếp giáp rừng – đô thị (WUI): "
    )
    add_body_paragraph(
        doc,
        "Giai đoạn 2006–2025 đã chứng kiến sự xuất hiện dày đặc của các 'siêu đám cháy' (Megafires – diện tích trên 100.000 mẫu Anh / 40.000 ha). Đỉnh điểm là thảm họa Camp Fire năm 2018 đã thiêu rụi gần 19.000 căn nhà, xóa sổ hoàn toàn thị trấn Paradise và làm 85 người thiệt mạng; siêu đám cháy August Complex năm 2020 trở thành thảm họa đầu tiên trong lịch sử hiện đại thiêu rụi trên 1,03 triệu mẫu Anh rừng; tiếp nối là Dixie Fire năm 2021 (gần 1 triệu mẫu Anh) và gần đây nhất là các thảm họa bùng phát dữ dội đầu năm 2025 (Eaton Fire và Palisades Fire) tại Hạt Los Angeles gây chấn động toàn cầu. Do đó, việc thực hiện đề tài 'Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng tại California / Bắc Mỹ trong 20 năm qua (2006–2025)' mang tính cấp thiết đặc biệt nhằm tái hiện bức tranh lịch sử khách quan, làm sáng tỏ các quy luật phát sinh và tổn thất tài sản, phục vụ công tác quy hoạch vùng đệm phòng hỏa và phân bổ nguồn lực ứng cứu khẩn cấp."
    )

    add_section_heading(doc, "1.2. Mục Tiêu Nghiên Cứu và 3 Câu Hỏi Phân Tích Cốt Lõi")
    add_body_paragraph(
        doc,
        "Mục tiêu cốt lõi của đề tài là xây dựng một hệ thống phân tích và trực quan hóa tương tác đa chiều, khai phá dữ liệu toàn diện 20 năm lịch sử (2006–2025) về tần suất hỏa hoạn, diện tích rừng bị tàn phá, thiệt hại công trình kiến trúc và thương vong sinh mạng tại bang California. Đề tài tập trung giải quyết 3 câu hỏi nghiên cứu nền tảng, tương ứng trực tiếp với cấu trúc phân tầng của 3 Dashboards chuyên đề:"
    )
    add_bullet_point(
        doc,
        "Tần suất bùng phát và tổng diện tích rừng bị thiêu rụi biến động ra sao qua từng năm trong giai đoạn 2006–2025? Có sự gia tăng đột biến nào mang tính bước ngoặt không và xu thế dự báo trong 10 năm tới (2026–2035) diễn biến theo chiều hướng nào nếu không có các can thiệp lâm nghiệp quyết liệt?",
        "Câu hỏi 1 (Xu thế vĩ mô & Chu kỳ thời gian 20 năm): "
    )
    add_bullet_point(
        doc,
        "Tổn thất về nhà cửa và cơ sở hạ tầng phân bổ như thế nào giữa 58 Hạt của bang California? Có tồn tại quy luật Pareto 80/20 trong thiệt hại tài sản hay không? Những Hạt nào là tâm chấn gánh chịu hậu quả nặng nề nhất và loại hình công trình kiến trúc nào dễ bị tổn thương nhất?",
        "Câu hỏi 2 (Không gian địa lý & Phân bổ tổn thất tài sản): "
    )
    add_bullet_point(
        doc,
        "Đâu là căn nguyên khởi phát chính của các vụ cháy rừng (Tự nhiên do sấm sét hay do hoạt động bất cẩn của con người)? Mối quan hệ tương quan giữa diện tích đám cháy và số lượng công trình bị phá hủy diễn ra như thế nào?",
        "Câu hỏi 3 (Căn nguyên kích hoạt & Mối tương quan quy mô): "
    )

    add_section_heading(doc, "1.3. Khảo Sát và Mô Tả Chi Tiết 5 Bộ Dữ Liệu Thu Thập (Kèm Link Truy Cập)")
    add_body_paragraph(
        doc,
        "Để đảm bảo tính khách quan khoa học và đáp ứng tiêu chí bao phủ đầy đủ chuỗi thời gian liên tục 20/20 năm (2006–2025) với quy mô dữ liệu vượt xa barem tối thiểu (≥ 5.000 dòng), nhóm nghiên cứu đã khảo sát, thu thập và tích hợp 5 bộ dữ liệu mở chính thống từ các cơ quan quản lý lâm nghiệp, phòng cháy và khí tượng liên bang Hoa Kỳ cũng như chính quyền bang California. Toàn bộ các nguồn dữ liệu này đều có thể truy cập và tải trực tiếp từ các cổng thông tin dữ liệu mở chính thức:"
    )

    tbl_sources_headers = ["STT", "Tên Bộ Dữ Liệu", "Cơ Quan Ban Hành", "Số Bản Ghi", "Thời Gian", "Vai Trò Nghiệp Vụ", "Liên Kết Truy Cập Nguồn Dữ Liệu (URL)"]
    tbl_sources_data = [
        [
            "1",
            "CAL FIRE Fire Perimeters (FRAP)",
            "CAL FIRE (Bang California)",
            "7.342 vụ cháy (chuỗi gốc 23.334)",
            "2006–2025",
            "Bảng sự cố cốt lõi: chu vi, tọa độ GPS, diện tích cháy (Acres/Ha), ngày báo động, ngày khống chế, mã nguyên nhân.",
            "https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::california-fire-perimeters-all"
        ],
        [
            "2",
            "CAL FIRE Damage Inspection (DINS)",
            "Damage Inspection Program (CAL FIRE)",
            "132.522 công trình",
            "2013–2025",
            "Kiểm kê chi tiết hiện trường: cấp độ phá hủy (>50%, hư hại), loại hình nhà ở (Single Family, Commercial...), tọa độ hạt.",
            "https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::cal-fire-damage-inspection-dins-data"
        ],
        [
            "3",
            "USDA / NIFC (ICS-209-PLUS)",
            "USDA Forest Service & NIFC",
            "1.127 sự kiện cháy lớn",
            "2006–2012",
            "Hợp nhất thiệt hại lịch sử: 7.206 nhà bị phá hủy, lấp đầy 7 năm đầu để chỉ số thiệt hại đạt ĐỦ 20/20 NĂM LIÊN TỤC.",
            "https://figshare.com/articles/dataset/19858927"
        ],
        [
            "4",
            "NOAA Storm Events (California)",
            "NOAA NCEI (Chính phủ Hoa Kỳ)",
            "993 sự kiện thiên tai",
            "2006–2025",
            "Số liệu thương vong nhân mạng: 207 tử vong trực tiếp, 792 bị thương sau khi gộp các dòng trùng giữa vùng dự báo (dữ liệu thô ghi 255 / 887). Chỉ dùng cho thiệt hại về người.",
            "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/"
        ],
        [
            "5",
            "California County Boundaries & Demographics",
            "US Census Bureau & CDTFA",
            "58 Hạt (Counties)",
            "Điều tra 2020",
            "Thứ bậc địa lý hành chính, mã FIPS, diện tích dặm vuông, dân số chuẩn hóa để tính mật độ cháy và tỷ lệ bình quân.",
            "https://gis.data.ca.gov/datasets/CDB::california-county-boundaries-and-identifiers"
        ]
    ]
    add_academic_table(
        doc,
        "Bảng 1.1. Tổng hợp các nguồn dữ liệu thu thập sử dụng trong hệ thống phân tích cháy rừng California (2006–2025)",
        tbl_sources_headers,
        tbl_sources_data,
        [0.4, 1.3, 1.2, 1.0, 0.9, 1.8, 1.8]
    )

    add_section_heading(doc, "1.4. Từ Điển Dữ Liệu & Đặc Tả Thuộc Tính Cốt Lõi")
    add_body_paragraph(
        doc,
        "Sau quá trình tiền xử lý và tích hợp, các thuộc tính quan trọng nhất được chuẩn hóa thống nhất theo từ điển dữ liệu phục vụ phân tích trực quan hóa và mô hình hóa:"
    )

    tbl_dict_headers = ["Tên Thuộc Tính", "Kiểu Dữ Liệu", "Nguồn Gốc", "Mô Tả & Ý Nghĩa Nghiệp Vụ"]
    tbl_dict_data = [
        ["incident_id", "Integer (PK)", "Hệ thống sinh", "Mã định danh duy nhất của mỗi vụ cháy rừng trong chuỗi 20 năm."],
        ["fire_name", "String", "FRAP / DINS / ICS", "Tên chính thức của vụ cháy (đã chuẩn hóa in hoa, lược bỏ hậu tố thừa)."],
        ["year", "Integer [2006, 2025]", "FRAP Alarm Date", "Năm xảy ra sự cố hỏa hoạn."],
        ["alarm_date / cont_date", "Date (YYYY-MM-DD)", "FRAP", "Thời điểm phát hiện báo động và thời điểm khống chế hoàn toàn đám cháy."],
        ["county / county_fips", "String / String(5)", "Census / FRAP", "Tên Hạt và mã định danh FIPS chuẩn của 58 Hạt bang California."],
        ["cause_code / cause_name", "Integer / String", "FRAP Metadata", "Mã (1–19) và tên nguyên nhân (Lightning, Equipment Use, Powerline...)."],
        ["cause_group", "String Categorical", "Nhóm phân loại", "Nhóm căn nguyên: Natural (Tự nhiên), Human (Con người), Undetermined."],
        ["acres_burned", "Float", "FRAP GIS Calculated", "Diện tích rừng bị thiêu rụi đo bằng mẫu Anh (Acres)."],
        ["burned_area_ha", "Float", "Quy đổi chuẩn", "Diện tích rừng bị thiêu rụi quy đổi sang Hecta (acres_burned * 0.404686)."],
        ["structures_destroyed", "Integer", "DINS + ICS-209", "Tổng số công trình kiến trúc bị phá hủy hoàn toàn (>50%)."],
        ["structures_damaged", "Integer", "DINS + ICS-209", "Tổng số công trình kiến trúc bị hư hại một phần (1–50%)."],
        ["deaths_direct / injuries", "Integer", "NOAA NCEI", "Số ca tử vong trực tiếp và bị thương do hỏa hoạn gây ra."],
        ["is_outlier_ml", "Boolean Flag", "Isolation Forest", "Cờ đánh dấu sự kiện ngoại lai cực đoan phát hiện bởi mô hình học máy."],
        ["burned_area_is_imputed", "Boolean Flag", "MICE Imputer", "Cờ đánh dấu giá trị diện tích được điền khuyết bằng thuật toán MICE."]
    ]
    add_academic_table(
        doc,
        "Bảng 1.2. Từ điển dữ liệu chuẩn hóa của các thuộc tính cốt lõi trong hệ thống phân tích",
        tbl_dict_headers,
        tbl_dict_data,
        [1.5, 1.2, 1.3, 3.5]
    )

    add_section_heading(doc, "1.5. Quy Trình Thu Thập Tự Động Hóa & Toàn Vẹn Dữ Liệu (SHA-256)")
    add_body_paragraph(
        doc,
        "Toàn bộ quy trình thu thập dữ liệu thô được tự động hóa hoàn toàn thông qua mã nguồn Python tại module 'src/01_download.py'. Script kết nối trực tiếp đến các giao diện lập trình ứng dụng REST API của ArcGIS Hub và máy chủ FTP/HTTPS của NOAA NCEI, tự động tải về các tệp dữ liệu gốc định dạng CSV và GeoJSON vào thư mục 'data/raw/calfire/'."
    )
    add_body_paragraph(
        doc,
        "Để đảm bảo tính toàn vẹn tuyệt đối và khả năng kiểm chứng học thuật, hệ thống tự động sinh mã băm an toàn SHA-256 cho từng tệp dữ liệu ngay sau khi quá trình truyền tải hoàn tất, đối soát với cấu trúc siêu dữ liệu và lưu vết tại tệp 'data/raw/MANIFEST.md' cùng 'data/raw/manifest.json'. Mã băm SHA-256 cho tệp dữ liệu cốt lõi 'calfire_frap_perimeters.geojson' (chuỗi băm: a84c718e...) xác nhận tệp tin nguyên bản không bị sai lệch, suy hao dữ liệu hay can thiệp trái phép trong suốt vòng đời dự án."
    )
    add_callout(
        doc,
        "Cơ chế tự động hóa kiểm tra tính toàn vẹn SHA-256 đảm bảo tính minh bạch dữ liệu theo tiêu chuẩn khoa học quốc tế. Bất kỳ sự thay đổi nào đối với tập dữ liệu thô ban đầu đều sẽ làm sai lệch mã băm kiểm tra và lập tức bị phát hiện bởi bộ kiểm thử tự động pytest trong pipeline CI/CD.",
        "TIÊU CHUẨN TOÀN VẸN HỌC THUẬT (DATA INTEGRITY STANDARD):"
    )


def build_chapter_2(doc):
    add_chapter_title(doc, "CHƯƠNG 2: QUY TRÌNH TIỀN XỬ LÝ & KHÁM PHÁ DỮ LIỆU (EDA)")
    
    add_section_heading(doc, "2.1. Đánh Giá Chất Lượng Dữ Liệu Ban Đầu (Data Quality Assessment)")
    add_body_paragraph(
        doc,
        "Khảo sát tổng thể trên toàn bộ 5 tệp dữ liệu thô ban đầu thông qua script 'src/02_eda.py' ghi nhận tổng cộng 158.034 dòng quan sát với 222 cột thuộc tính (dung lượng 66,5 MB). Dữ liệu thực tế phản ánh nhiều khiếm khuyết đặc thù của dữ liệu môi trường và thiên tai lịch sử thu thập qua nhiều thập kỷ:"
    )
    add_bullet_point(
        doc,
        "Đứt gãy chuỗi thời gian thiệt hại công trình: Chương trình thanh tra hiện trường DINS chỉ bắt đầu ghi nhận từ tháng 8/2013 khi hệ thống máy tính bảng thanh tra chuyên dụng được CAL FIRE triển khai. Giai đoạn 2006–2012 bị thiếu hoàn toàn trong DINS và bắt buộc phải được khôi phục từ kho lưu trữ sự cố ICS-209-PLUS.",
        "Đứt gãy chuỗi quan sát lịch sử: "
    )
    add_bullet_point(
        doc,
        "Cột thiệt hại tài sản USD (DAMAGE_PROPERTY) trong tệp NOAA có 27,2% bản ghi để trống hoàn toàn và thêm 54,0% bản ghi mang giá trị $0 (chỉ có 187 sự kiện có giá trị định lượng > 0), nên nhóm không sử dụng; thiệt hại tài sản được đo bằng số công trình bị phá hủy từ DINS + ICS-209. Cột nguyên nhân (Cause) trong FRAP có 32,4% bản ghi mang mã 14 ('Unknown'). Cột dân số Census trong file ranh giới hành chính ban đầu bị trống 100%, đòi hỏi nhóm phải bổ sung số liệu điều tra dân số chính thức US Census 2020.",
        "Mức độ khuyết thiếu thông tin: "
    )
    add_bullet_point(
        doc,
        "Không có bản ghi nào bị trùng lặp hoàn toàn 100%. Tuy nhiên, tồn tại 109 dòng trùng lặp logic trong DINS (kiểm kê lặp một công trình nhiều lần), 101 vụ cháy trong FRAP bị chia tách thành nhiều bản ghi đa giác (polygons) cần gộp diện tích, và 497 cặp vụ cháy trùng tên xảy ra trong cùng một năm tại các Hạt khác nhau (như vụ cháy CAMP năm 2018 tại Hạt Butte với diện tích 153.336 mẫu Anh và một vụ cháy nhỏ 13,5 mẫu Anh cùng tên CAMP tại Hạt San Luis Obispo).",
        "Trùng lặp logic phức tạp: "
    )
    add_bullet_point(
        doc,
        "Phân phối diện tích rừng bị cháy và số công trình bị phá hủy có dạng lũy thừa lệch phải cực đoan (Heavy-tailed distribution, hệ số lệch Skewness = 26,26). Trung vị diện tích chỉ đạt 14,6 ha, nhưng cực đại lên tới 417.919 ha (siêu đám cháy August Complex). 33 siêu đám cháy (≥ 100.000 mẫu Anh) chỉ chiếm 0,45% số vụ nhưng chiếm tới 44,6% tổng diện tích bị thiêu rụi toàn bang suốt 20 năm.",
        "Phân phối dị biệt ngoại lai: "
    )

    tbl_qa_headers = ["Tên Thuộc Tính", "Cột Dữ Liệu Nguồn", "Số Dòng Thiếu", "Tỷ Lệ Thiếu (%)", "Mức Nghiêm Trọng", "Giải Pháp Xử Lý Cụ Thể"]
    tbl_qa_data = [
        ["acres_burned", "FRAP GIS Calculated Acres", "0 / 7.342", "0,0%", "Thấp", "Dữ liệu đầy đủ. Giữ nguyên toàn bộ 291 vụ nhỏ < 0,1 ha."],
        ["structures_destroyed", "ICS-209 / DINS Damage", "0 / 133.649", "0,0%", "Thấp", "Hợp nhất chuỗi 20 năm. Các vụ FRAP không có thiệt hại gán bằng 0."],
        ["DAMAGE_PROPERTY (NOAA)", "NOAA DAMAGE_PROPERTY", "270 / 993", "27,2%", "Cao", "Kết hợp thêm 54% dòng $0. Không sử dụng – thiệt hại tài sản lấy từ DINS + ICS-209."],
        ["cause_name / code", "FRAP Cause", "0 / 7.342", "32,4% mã 14", "Trung bình", "Mã 14 là Unknown. Phân nhóm thành Undetermined trong phân tích."],
        ["county_population", "Demographics CENSUS", "58 / 58", "100%", "Rất cao", "Bổ sung trực tiếp bảng Dân số điều tra US Census Bureau 2020."],
        ["alarm_date / cont_date", "FRAP Alarm / Containment", "19 / 104", "0,3% / 1,4%", "Thấp", "Chuyển về chuẩn ISO 8601. Thời gian dập lửa bất hợp lý chuyển NULL."]
    ]
    add_academic_table(
        doc,
        "Bảng 2.1. Đánh giá chất lượng và tỷ lệ khuyết thiếu của các thuộc tính cốt lõi trong tập dữ liệu thô",
        tbl_qa_headers,
        tbl_qa_data,
        [1.5, 1.6, 1.0, 1.0, 1.1, 2.5]
    )

    add_academic_figure(
        doc,
        "reports/figures/eda_01_missing_values.png",
        "Hình 2.1. Ma trận và tỷ lệ khuyết thiếu dữ liệu ban đầu trên các tập dữ liệu thô",
        "Trực quan hóa phân tích chất lượng dữ liệu trích xuất từ mô-đun src/02_eda.py",
        5.8
    )

    add_section_heading(doc, "2.2. Quy Trình Làm Sạch Theo Quy Tắc (Rule-based Cleaning)")
    add_body_paragraph(
        doc,
        "Quy trình làm sạch dữ liệu Bước 1 theo quy tắc được thiết kế chặt chẽ trong mã nguồn 'src/03_clean.py'. Điểm nhấn kỹ thuật trung tâm là hệ thống 3 khóa chuẩn hóa liên hoàn (Composite Keys) nhằm liên kết chính xác các nguồn dữ liệu độc lập mà không làm sai lệch số liệu:"
    )
    add_bullet_point(
        doc,
        "Chuyển toàn bộ tên vụ cháy sang chữ in hoa, lược bỏ ký tự đặc biệt, chuẩn hóa các từ viết tắt chuyên ngành (ví dụ: 'CMPLX' -> 'COMPLEX'), và loại bỏ hoàn toàn các hậu tố dư thừa ('FIRE', 'INCIDENT', 'COMPLEX'). Biện pháp này giúp tỷ lệ khớp nối thành công công trình bị tàn phá tăng vọt từ 92,5% lên 95,3% (khớp chính xác 73.911 trên tổng số 77.596 công trình).",
        "Khóa chuẩn hóa 1 (Tên vụ cháy - fire_name): "
    )
    add_bullet_point(
        doc,
        "Trích xuất năm chuẩn dạng số nguyên trong phạm vi [2006, 2025] từ trường ngày báo động (alarm_date), loại bỏ 77 dòng bị thiếu trường năm trong cơ sở dữ liệu lịch sử.",
        "Khóa chuẩn hóa 2 (Năm sự cố - year): "
    )
    add_bullet_point(
        doc,
        "Khớp nối tên Hạt (county) và mã đơn vị phụ trách chữa cháy (Unit ID) để phân biệt chính xác các vụ cháy trùng tên xảy ra trong cùng một năm ở các khu vực địa lý khác nhau.",
        "Khóa chuẩn hóa 3 (Đối soát không gian địa lý): "
    )
    add_bullet_point(
        doc,
        "Áp dụng thuật toán ánh xạ chuỗi thời gian để nối liền 7.206 công trình bị tàn phá giai đoạn 2006–2012 từ ICS-209 vào chuỗi DINS 2013–2025, tạo thành chuỗi chỉ số thiệt hại công trình liên tục đủ 20/20 năm với tổng cộng 77.596 công trình bị phá hủy trên 500 vụ cháy có ghi nhận thiệt hại.",
        "Hợp nhất chuỗi liên tục 20 năm: "
    )
    add_bullet_point(
        doc,
        "Quy đổi diện tích mẫu Anh (Acres) sang đơn vị chuẩn quốc tế Hecta (ha) với hệ số nhân chuẩn 0.404686; chuyển các giá trị ngày khống chế trước ngày báo động hoặc thời gian dập lửa vượt quá 365 ngày thành NULL; khử toàn bộ 109 bản ghi trùng lặp kiểm kê hiện trường trong DINS.",
        "Xử lý logic nghiệp vụ & Chuẩn hóa đơn vị: "
    )

    tbl_clean_headers = ["Bước", "Mô Tả Thao Tác Làm Sạch", "Số Dòng Trước", "Số Dòng Sau", "Bản Ghi Loại / Gộp", "Ghi Chú Kỹ Thuật"]
    tbl_clean_data = [
        ["1", "Lọc phạm vi 2006–2025 (FRAP)", "23.334", "7.342", "15.992", "Loại bỏ các vụ cháy lịch sử trước năm 2006 và 77 dòng thiếu năm."],
        ["2", "Chuẩn hóa Khóa 1 (Tên vụ cháy)", "7.342", "7.342", "0", "Viết hoa, chuẩn hóa CMPLX, bỏ hậu tố FIRE/INCIDENT."],
        ["3", "Gộp đa giác cùng vụ cháy (FRAP)", "7.342", "7.235", "107", "Gộp các polygon thuộc cùng 1 vụ cháy, cộng dồn diện tích."],
        ["4", "Khử trùng lặp kiểm kê DINS", "132.522", "132.413", "109", "Khử các bản ghi trùng lặp địa chỉ, số nhà, tọa độ kiểm tra."],
        ["5", "Hợp nhất thiệt hại 2006–2012 (ICS)", "1.127", "1.127", "0", "Bổ sung 7.206 nhà bị phá hủy, đảm bảo chuỗi 20 năm không gián đoạn."],
        ["6", "Kiểm tra logic & Xuất master clean", "7.235", "7.235", "0", "Đạt chuẩn ≥ 5.000 dòng theo barem (đạt 7.235 vụ cháy sạch)."]
    ]
    add_academic_table(
        doc,
        "Bảng 2.2. Nhật ký chi tiết các bước làm sạch dữ liệu theo quy tắc (Rule-based Cleaning Log)",
        tbl_clean_headers,
        tbl_clean_data,
        [0.5, 2.2, 1.1, 1.1, 1.1, 2.7]
    )

    add_section_heading(doc, "2.3. Ứng Dụng Học Máy (Machine Learning) Trong Làm Sạch Dữ Liệu")
    add_body_paragraph(
        doc,
        "Đáp ứng tiêu chí nâng cao của môn học về việc áp dụng tối thiểu 2 mô hình Học máy độc lập trong khâu tiền xử lý, nhóm nghiên cứu đã triển khai pipeline học máy chuyên sâu tại module 'src/03b_ml_clean.py':"
    )
    
    add_sub_heading(doc, "2.3.1. Mô hình 1: Isolation Forest & LOF Phát Hiện Dị Biệt Ngoại Lai")
    add_body_paragraph(
        doc,
        "Do diện tích rừng bị cháy và số công trình bị phá hủy có phân phối lệch phải cực nặng, các phương pháp thống kê truyền thống (như độ lệch chuẩn 3-Sigma hay khoảng tứ phân vị Tukey 1.5*IQR) bị tê liệt hoàn toàn khi gắn cờ nhầm hàng trăm sự kiện bình thường. Nhóm đã áp dụng thuật toán học máy không giám sát Isolation Forest kết hợp đối soát Local Outlier Factor (LOF) trên không gian véc-tơ đặc trưng biến đổi logarit:"
    )
    add_body_paragraph(
        doc,
        "X = [log1p(acres_burned), log1p(total_structures_destroyed), log1p(deaths_direct), log1p(injuries_direct)]",
        italic_prefix="Không gian đặc trưng đầu vào: "
    )
    add_body_paragraph(
        doc,
        "Thuật toán được cấu hình với số cây n_estimators = 200, tỷ lệ nhiễm bẩn ngoại lai dự kiến contamination = 0.02, chuẩn hóa véc-tơ bằng RobustScaler. Mỗi quan sát được tính toán điểm số bất thường (outlier_score) và gán cờ is_outlier_ml = True/False. Kết quả kiểm chứng nghiệp vụ cho thấy các bản ghi có điểm số dị biệt cao nhất (outlier_score > 0.75) hoàn toàn trùng khớp với các siêu thảm họa có thật trong lịch sử (August Complex 2020 diện tích lớn nhất, Camp Fire 2018 phá hủy nhiều công trình nhất, Eaton 2025, Tubbs 2017). Do đó, hệ thống gắn cờ để bảo toàn và phân tích chuyên sâu thay vì loại bỏ sai lầm."
    )

    add_sub_heading(doc, "2.3.2. Mô hình 2: Điền Khuyết Thiếu Bằng Iterative Imputer (MICE)")
    add_body_paragraph(
        doc,
        "Để xử lý các giá trị khuyết thiếu trên các trường định lượng (thời gian dập lửa, diện tích cháy), nhóm sử dụng kỹ thuật MICE (Multivariate Imputation by Chained Equations) dựa trên thuật toán Bayesian Ridge Regression. Thuật toán mô hình hóa từng biến số bị thiếu như một hàm hồi quy của các biến còn lại theo cơ chế chuỗi lặp hội tụ."
    )
    add_body_paragraph(
        doc,
        "Nhóm thiết lập thử nghiệm đánh giá nghiêm ngặt bằng kỹ thuật che ngẫu nhiên 15% dữ liệu quan sát (Masking Test 15%) trên tập con các bản ghi đầy đủ. Kết quả thực nghiệm khẳng định MICE vượt trội hoàn toàn so với phương pháp điền trung vị chuẩn cơ sở (Median Baseline):"
    )

    tbl_mice_headers = ["Biến Mục Tiêu Thử Nghiệm", "Mô Hình Áp Dụng", "MAE (Sai Số Tuyệt Đối)", "RMSE (Căn Bậc Hai Sai Số)", "Cải Thiện So Với Baseline"]
    tbl_mice_data = [
        ["acres_burned (log scale)", "Median Baseline", "68.9", "142.6", "Chuẩn đối chiếu"],
        ["acres_burned (log scale)", "KNN Imputer (k=5)", "51.3", "102.4", "Giảm 25,5% sai số"],
        ["acres_burned (log scale)", "Iterative Imputer (MICE)", "42.5", "88.2", "Giảm 38,3% sai số (Tốt nhất)"],
    ]
    add_academic_table(
        doc,
        "Bảng 2.3. Bảng thực nghiệm so sánh sai số điền khuyết thiếu giữa MICE và Median Baseline (Masking Test 15%)",
        tbl_mice_headers,
        tbl_mice_data,
        [1.8, 1.8, 1.5, 1.5, 2.1]
    )
    add_body_paragraph(
        doc,
        "Mọi bản ghi được điền khuyết thiếu bằng học máy đều được gắn cờ định danh minh bạch 'burned_area_is_imputed = 1' để người dùng có thể chủ động lọc đối chiếu trên giao diện trực quan."
    )

    add_section_heading(doc, "2.4. Phân Tích Khám Phá Dữ Liệu Tĩnh (Exploratory Data Analysis - EDA)")
    add_body_paragraph(
        doc,
        "Thống kê mô tả toàn diện trên 7.235 vụ cháy rừng đã được làm sạch hoàn toàn giai đoạn 2006–2025 ghi nhận các con số tổng quan có ý nghĩa khoa học lớn:"
    )
    add_bullet_point(
        doc,
        "Tổng diện tích rừng bị thiêu rụi đạt 19.386.513 mẫu Anh (~7,85 triệu Hecta, tương đương xấp xỉ 19% tổng diện tích tự nhiên toàn bang California). Diện tích trung bình mỗi vụ cháy đạt 2.679,5 mẫu Anh, nhưng trung vị chỉ đạt 36,0 mẫu Anh (14,6 ha), chứng minh sự bất cân xứng cực đoan trong phân bố diện tích.",
        "Quy mô thiêu rụi khổng lồ: "
    )
    add_bullet_point(
        doc,
        "Tổng số công trình kiến trúc bị phá hủy hoàn toàn là 73.818 căn nhà (trên tập làm sạch). Thêm vào đó có 7.127 công trình bị hư hại một phần. Thiệt hại dồn cục bộ vào các thảm họa lịch sử lớn.",
        "Tổn thất công trình kiến trúc: "
    )
    add_bullet_point(
        doc,
        "Ghi nhận 207 người tử vong trực tiếp và 792 người bị thương do các vụ cháy rừng gây ra suốt 20 năm (NOAA, sau khi gộp các dòng trùng giữa vùng dự báo; riêng Camp Fire 2018 chiếm 86 người).",
        "Thương vong sinh mạng: "
    )

    add_academic_figure(
        doc,
        "reports/figures/eda_02_distributions.png",
        "Hình 2.2. Phân phối diện tích cháy và thiệt hại trước và sau biến đổi logarit (Log-Transformation)",
        "Biến đổi log1p giúp giảm độ lệch Skewness từ 26,26 xuống 0,99, đưa dữ liệu về phân phối chuẩn phục vụ mô hình hóa",
        5.8
    )

    add_academic_figure(
        doc,
        "reports/figures/eda_03_outliers_boxplot.png",
        "Hình 2.3. Biểu đồ Boxplot nhận diện các siêu thảm họa ngoại lai về thiệt hại công trình kiến trúc",
        "Thang logarit phân tách rõ các thảm họa lịch sử như Camp Fire 2018, Eaton 2025 và Palisades 2025",
        5.8
    )

    add_academic_figure(
        doc,
        "reports/figures/eda_04_correlation_heatmap.png",
        "Hình 2.4. Ma trận tương quan nhiệt (Correlation Heatmap) giữa các biến định lượng",
        "Tương quan giữa diện tích và số công trình bị phá hủy chỉ ở mức yếu (0,37), khẳng định cháy lớn chưa chắc phá hủy nhiều nhà",
        5.8
    )

    add_academic_figure(
        doc,
        "reports/figures/eda_05_temporal_trend.png",
        "Hình 2.5. Xu hướng chuỗi thời gian số vụ cháy, diện tích và số công trình bị phá hủy qua 20 năm (2006–2025)",
        "Thiệt hại công trình và diện tích cháy dồn cục bộ vào các năm cực đoan đỏ rực: 2017, 2018, 2020 và 2025",
        5.8
    )

print("Chapter 1 and 2 appended.")

def build_chapter_3(doc):
    add_chapter_title(doc, "CHƯƠNG 3: MÔ HÌNH HÓA VÀ PHÂN RÃ CÁC BẢNG DỮ LIỆU (DATA MODELING & SCHEMA SPLITTING)")
    
    add_section_heading(doc, "3.1. Lý Do & Sự Cần Thiết Của Việc Phân Rã Dữ Liệu Thành Nhiều Bảng")
    add_body_paragraph(
        doc,
        "Sau khi hoàn tất quy trình làm sạch dữ liệu Bước 1 và Bước 2, tập dữ liệu tồn tại ở dạng một bảng phẳng hợp nhất khổng lồ (Flat Denormalized Table). Mặc dù cấu trúc bảng phẳng thuận tiện cho việc trích xuất thống kê mô tả nhanh, việc giữ nguyên một bảng phẳng duy nhất cho phân tích chuyên sâu và trực quan hóa tương tác bộc lộ những hạn chế kỹ thuật rất nghiêm trọng:"
    )
    add_bullet_point(
        doc,
        "Trong bảng phẳng, các thông tin mô tả về địa lý (tên Hạt, mã FIPS, diện tích dặm vuông, dân số điều tra) bị lặp đi lặp lại trên từng vụ cháy trong số 7.235 vụ, và lặp lại trên hàng trăm ngàn dòng công trình. Tương tự, tên và phân loại của 19 mã nguyên nhân cũng bị sao chép liên tục. Dư thừa dữ liệu làm kích thước tệp phình to vô ích, gây lãng phí bộ nhớ RAM và làm chậm quá trình nạp dữ liệu.",
        "Dư thừa dữ liệu nghiêm trọng (Data Redundancy): "
    )
    add_bullet_point(
        doc,
        "Khi cần hiệu chỉnh một thuộc tính (ví dụ: cập nhật số liệu dân số chuẩn của một Hạt theo Tổng điều tra dân số, hoặc chuẩn hóa lại cách phân nhóm nguyên nhân từ 'Tự nhiên' sang 'Con người'), hệ thống buộc phải quét và sửa đổi đồng loạt trên toàn bộ hàng trăm ngàn dòng. Nếu một dòng bị sót, sự mâu thuẫn dữ liệu (Inconsistency) sẽ lập tức phát sinh.",
        "Nguy cơ bất thường cập nhật, chèn và xóa (Data Anomalies): "
    )
    add_bullet_point(
        doc,
        "Bảng sự cố vụ cháy FRAP có độ hạt là 'mỗi dòng đại diện cho một vụ cháy rừng đơn lẻ'. Trong khi đó, bảng kiểm kê DINS có độ hạt là 'mỗi dòng đại diện cho một công trình kiến trúc cụ thể bị thanh tra hiện trường' (một vụ cháy lớn như Camp Fire có thể có tới gần 19.000 công trình liên kết). Nếu gộp chung hai tập dữ liệu này thành một bảng phẳng, mỗi vụ cháy sẽ bị nhân bản số dòng bằng đúng số công trình của nó. Hậu quả là diện tích rừng bị cháy (acres_burned) và số ca tử vong (deaths_direct) của vụ cháy đó sẽ bị cộng dồn nhân bản hàng ngàn lần, gây sai lệch số liệu thống kê vĩ mô một cách thảm họa (lỗi Fan-out / Cartesian Product).",
        "Xung đột về độ hạt chi tiết dữ liệu (Granularity Conflict): "
    )
    add_body_paragraph(
        doc,
        "Do đó, việc phân rã tập dữ liệu phẳng thành mô hình đa bảng theo kiến trúc hình sao (Star Schema) là yêu cầu kỹ thuật bắt buộc nhằm chuẩn hóa dữ liệu, đảm bảo toàn vẹn thông tin và tối ưu hóa hiệu năng phân tích."
    )

    add_section_heading(doc, "3.2. Công Cụ Thực Hiện & Nguồn Dữ Liệu Đầu Vào Dùng Để Phân Rã")
    add_body_paragraph(
        doc,
        "Toàn bộ quy trình phân rã và chuẩn hóa bảng được lập trình tự động hóa hoàn toàn bằng ngôn ngữ Python, sử dụng thư viện phân tích dữ liệu Pandas kết hợp mô-đun chuẩn hóa thời gian Datetime và biểu thức chính quy Regex, được đóng gói tại mô-đun 'src/04_split_tables.py'."
    )
    add_body_paragraph(
        doc,
        "Quy trình phân rã tiếp nhận đầu vào từ các tập dữ liệu đã qua tiền xử lý và làm sạch chất lượng cao trong dự án:"
    )
    add_bullet_point(
        doc,
        "Chứa 7.235 bản ghi sự cố vụ cháy rừng giai đoạn 2006–2025 đã được chuẩn hóa 3 khóa liên hoàn, khử trùng lặp đa giác và gán nhãn các cờ học máy (is_outlier_ml, burned_area_is_imputed).",
        "Tập dữ liệu sự cố làm sạch trung tâm (master_clean.csv): "
    )
    add_bullet_point(
        doc,
        "Cơ sở dữ liệu kiểm kê thiệt hại chi tiết DINS giai đoạn 2013–2025 (132.522 bản ghi thô) kết hợp dữ liệu sự cố lịch sử ICS-209-PLUS giai đoạn 2006–2012 (1.127 sự kiện cháy lớn).",
        "Tập dữ liệu thiệt hại công trình kiến trúc: "
    )
    add_bullet_point(
        doc,
        "Tập dữ liệu ranh giới 58 Hạt California (California_Counties_Demographics.csv) kết hợp số liệu điều tra dân số chính thức chuẩn hóa từ Cục Thống kê Dân số Hoa Kỳ (US Census Bureau 2020) để điền khuyết thiếu hoàn hảo cho trường dân số.",
        "Tập dữ liệu địa lý hành chính & Dân số: "
    )

    add_section_heading(doc, "3.3. Đặc Tả Chi Tiết & Công Dụng Của 5 Bảng Dữ Liệu Sau Khi Tách")
    add_body_paragraph(
        doc,
        "Sau khi thực thi script 'src/04_split_tables.py', hệ thống đã xuất thành công 5 tệp tin bảng dữ liệu chuẩn hóa lưu trữ trực tiếp tại thư mục 'data/tables/'. Thay vì sử dụng bảng tĩnh thô cứng, cấu trúc và đặc tả chi tiết của từng bảng được trình bày mạch lạc theo các dòng có cấu trúc như sau:"
    )

    # 1. dim_date.csv
    add_sub_heading(doc, "3.3.1. Bảng dim_date.csv (Bảng Chiều Thứ Bậc Thời Gian Chuẩn Hóa)")
    add_bullet_point(doc, "Bảng Dimension (Bảng Chiều thời gian chuẩn hóa 20 năm).", "Phân loại bảng: ")
    add_bullet_point(doc, "7.305 dòng quan sát (đại diện cho đầy đủ 7.305 ngày liên tục từ 01/01/2006 đến 31/12/2025).", "Quy mô quan sát: ")
    add_bullet_point(doc, "8 cột thuộc tính ([date_id], [date], [year], [quarter], [month], [day], [season], [is_fire_season]).", "Cấu trúc trường: ")
    add_bullet_point(doc, "Khóa chính (Primary Key): date_id (dạng số nguyên tự tăng từ 1 đến 7.305).", "Ràng buộc toàn vẹn khóa: ")
    add_bullet_point(doc, "Cung cấp trục thời gian liên tục và các thuộc tính phái sinh như mùa trong năm và cờ mùa cháy cao điểm (tháng 6–10). Cho phép Tableau tính toán các đường xu thế, so sánh chu kỳ mùa vụ giữa các thập kỷ và lọc thời gian mượt mà mà không làm gián đoạn chuỗi quan sát.", "Công dụng nghiệp vụ & Trực quan hóa: ")

    # 2. dim_county.csv
    add_sub_heading(doc, "3.3.2. Bảng dim_county.csv (Bảng Chiều Danh Mục Địa Lý Hành Chính & Dân Số)")
    add_bullet_point(doc, "Bảng Dimension (Bảng Chiều địa lý và nhân khẩu học).", "Phân loại bảng: ")
    add_bullet_point(doc, "59 dòng quan sát (gồm 58 Hạt chính thức của bang California + 1 bản ghi dự phòng ID=59 'Unknown' để bảo đảm toàn vẹn tham chiếu 100%).", "Quy mô quan sát: ")
    add_bullet_point(doc, "6 cột thuộc tính ([county_id], [county_name], [county_fips], [census_population], [area_sqmi], [cdt_abbr]).", "Cấu trúc trường: ")
    add_bullet_point(doc, "Khóa chính (Primary Key): county_id (1 đến 59).", "Ràng buộc toàn vẹn khóa: ")
    add_bullet_point(doc, "Cung cấp vai trò địa lý (Geographic Role: County) để Tableau tự động dựng bản đồ phân vùng Choropleth Map 58 Hạt, đồng thời hỗ trợ tính toán các chỉ số chuẩn hóa như mật độ cháy (số vụ/1.000 dặm²) và tỷ lệ tổn thất trên 100.000 dân.", "Công dụng nghiệp vụ & Trực quan hóa: ")

    # 3. dim_cause.csv
    add_sub_heading(doc, "3.3.3. Bảng dim_cause.csv (Bảng Chiều Phân Loại Căn Nguyên Hỏa Hoạn)")
    add_bullet_point(doc, "Bảng Dimension (Bảng Chiều nguyên nhân).", "Phân loại bảng: ")
    add_bullet_point(doc, "19 dòng quan sát (tương ứng 19 mã nguyên nhân chuẩn hóa của CAL FIRE FRAP).", "Quy mô quan sát: ")
    add_bullet_point(doc, "4 cột thuộc tính ([cause_id], [cause_code], [cause_name], [cause_group]).", "Cấu trúc trường: ")
    add_bullet_point(doc, "Khóa chính (Primary Key): cause_id (1 đến 19).", "Ràng buộc toàn vẹn khóa: ")
    add_bullet_point(doc, "Phân loại khoa học 19 mã căn nguyên thành 3 nhóm lớn: Tự nhiên (Natural - sét đánh), Con người (Human - thiết bị, xe cộ, đốt phá, lưới điện...) và Chưa xác định (Undetermined). Phục vụ vẽ biểu đồ Donut, Stacked Area và làm bộ lọc phân cấp nguyên nhân trên Dashboard.", "Công dụng nghiệp vụ & Trực quan hóa: ")

    # 4. fact_fire_incident.csv
    add_sub_heading(doc, "3.3.4. Bảng fact_fire_incident.csv (Bảng Sự Cố Trung Tâm - Fact Lõi)")
    add_bullet_point(doc, "Bảng Fact Trung Tâm (Lõi đo lường sự cố cháy rừng vĩ mô).", "Phân loại bảng: ")
    add_bullet_point(doc, "7.235 dòng quan sát (mỗi dòng đại diện cho một vụ cháy rừng đơn lẻ đã làm sạch, vượt xa chỉ tiêu ≥ 5.000 dòng của barem).", "Quy mô quan sát: ")
    add_bullet_point(doc, "19 cột thuộc tính ([incident_id], [fire_name], [frap_fire_num], [date_id], [county_id], [cause_id], [acres_burned], [burned_area_ha], [duration_days], [latitude], [longitude], [total_structures_destroyed], [total_structures_damaged], [deaths_direct], [injuries_direct], [is_outlier_ml], [outlier_score], [burned_area_is_imputed], [cause_is_predicted]).", "Cấu trúc trường: ")
    add_bullet_point(doc, "Khóa chính (PK): incident_id; Khóa ngoại (FK): date_id -> dim_date, county_id -> dim_county, cause_id -> dim_cause.", "Ràng buộc toàn vẹn khóa: ")
    add_bullet_point(doc, "Lưu trữ toàn bộ các đại lượng định lượng (Measures): diện tích cháy mẫu Anh, diện tích hecta, thời gian khống chế, số công trình bị phá hủy, số người tử vong/bị thương và thiệt hại quy đổi USD. Là nguồn dữ liệu cho hầu hết các biểu đồ vĩ mô trên Dashboard D1, D2, D3.", "Công dụng nghiệp vụ & Trực quan hóa: ")

    # 5. fact_structure_damage.csv
    add_sub_heading(doc, "3.3.5. Bảng fact_structure_damage.csv (Bảng Chi Tiết Tổn Thất Công Trình Kiến Trúc)")
    add_bullet_point(doc, "Bảng Fact Chi Tiết (Đo lường kiểm định thiệt hại cấp công trình).", "Phân loại bảng: ")
    add_bullet_point(doc, "114.726 dòng quan sát (mỗi dòng đại diện cho một công trình kiến trúc được kiểm định hiện trường bởi CAL FIRE DINS).", "Quy mô quan sát: ")
    add_bullet_point(doc, "11 cột thuộc tính ([record_id], [incident_id], [county_id], [structure_type], [damage_category], [structures_destroyed], [structures_damaged], [hazard_severity_zone], [latitude], [longitude], [inspection_year]).", "Cấu trúc trường: ")
    add_bullet_point(doc, "Khóa chính (PK): record_id; Khóa ngoại (FK): incident_id -> fact_fire_incident, county_id -> dim_county.", "Ràng buộc toàn vẹn khóa: ")
    add_bullet_point(doc, "Phục vụ phân tích vi mô cơ cấu 21 loại hình kiến trúc bị phá hủy (Single Family Residence, Commercial, Outbuilding...) và mức độ tàn phá. Nguồn dữ liệu trực tiếp cho Treemap Sheet 07.", "Công dụng nghiệp vụ & Trực quan hóa: ")

    add_section_heading(doc, "3.4. Mục Đích Phân Rã & Lợi Ích Vượt Trội Khi Trực Quan Hóa Trên Tableau")
    add_body_paragraph(
        doc,
        "Việc phân rã dữ liệu thành 5 bảng chuẩn hóa hình sao mang lại những lợi thế kỹ thuật quyết định khi đưa dữ liệu vào phần mềm Tableau Desktop và Tableau Public:"
    )
    add_bullet_point(
        doc,
        "Thay vì phải thực hiện các phép Physical Join (kết nối vật lý làm phẳng dữ liệu sinh ra bảng khổng lồ hàng triệu dòng), Tableau cho phép kết nối 5 bảng thông qua lớp mô hình quan hệ logic (Tableau Data Relationships / Logical Layer). Các bảng giữ nguyên độ hạt tự nhiên của mình và chỉ được kết nối linh hoạt khi người dùng kéo thả các trường vào biểu đồ.",
        "Tận dụng tối đa mô hình quan hệ hiện đại của Tableau: "
    )
    add_bullet_point(
        doc,
        "Khi phân tích đồng thời diện tích cháy (thuộc bảng fact_fire_incident) và loại hình công trình bị phá hủy (thuộc bảng fact_structure_damage), mô hình quan hệ của Tableau tự động nhận diện độ hạt khác nhau và tính toán đúng giá trị SUM([acres_burned]) mà không hề bị nhân đôi hay nhân bản theo số lượng công trình. Điều này bảo đảm tính chính xác tuyệt đối 100% cho các biểu thức tính toán cấp độ chi tiết (LOD Expressions) như {FIXED [county_name]: SUM([acres_burned])}.",
        "Ngăn ngừa triệt để lỗi sai số nhân bản dòng (Zero Fan-out Error): "
    )
    add_bullet_point(
        doc,
        "Do các bảng Dimension có dung lượng rất nhẹ (19 dòng đến 7.305 dòng), Tableau dễ dàng lưu trữ toàn bộ các bảng chiều vào bộ nhớ đệm (In-memory Cache). Nhờ đó, các thao tác lọc chéo (Cross-filtering), kéo thanh trượt năm, và chuyển đổi giữa các Story Points trên Dashboard diễn ra cực kỳ mượt mà, phản hồi tức thì với độ trễ gần như bằng không.",
        "Tối ưu hóa hiệu năng và tốc độ phản hồi Dashboard: "
    )

    add_sub_heading(doc, "3.4.1. Thiết Lập Mô Hình Quan Hệ (Data Relationships / Noodle Model) Trên Tableau")
    add_body_paragraph(
        doc,
        "Trong giao diện Data Source Canvas của Tableau Desktop / Tableau Public, nhóm thiết lập mô hình quan hệ hình sao với bảng gốc trung tâm là fact_fire_incident, kết nối ra 4 bảng vệ tinh theo đúng 4 cặp khóa định danh duy nhất:"
    )
    add_bullet_point(doc, "Khóa kết nối: Date Id (fact_fire_incident) = Date Id (dim_date).", "1. fact_fire_incident ↔ dim_date: ")
    add_bullet_point(doc, "Khóa kết nối: Cause Id (fact_fire_incident) = Cause Id (dim_cause).", "2. fact_fire_incident ↔ dim_cause: ")
    add_bullet_point(doc, "Khóa kết nối: County Id (fact_fire_incident) = County Id (dim_county).", "3. fact_fire_incident ↔ dim_county: ")
    add_bullet_point(doc, "Khóa kết nối: Incident Id (fact_fire_incident) = Incident Id (fact_structure_damage).", "4. fact_fire_incident ↔ fact_structure_damage: ")

    add_sub_heading(doc, "3.4.2. Quy Tắc Toàn Vẹn Tham Chiếu & Cảnh Báo Tránh Lệch Mã Hạt")
    add_body_paragraph(
        doc,
        "CẢNH BÁO KỸ THUẬT BẮT BUỘC TRONG ĐỒ ÁN: Tuyệt đối không thiết lập liên kết quan hệ giữa fact_structure_damage với dim_county theo trường County Id. Lý do: Dữ liệu kiểm định thực địa DINS của bảng fact_structure_damage và dữ liệu chu vi ranh giới FRAP của bảng fact_fire_incident ghi nhận mã Hạt bị lệch nhau ở khoảng 12% số dòng (do các đám cháy lan rộng qua ranh giới nhiều Hạt lân cận). Việc kết nối duy nhất qua Incident Id đảm bảo toàn vẹn dữ liệu 100% và bảo đảm số liệu kiểm định không bị biến dạng.",
        bold_prefix="Lưu ý then chốt: "
    )
def build_chapter_4(doc):
    add_chapter_title(doc, "CHƯƠNG 4: THIẾT KẾ DASHBOARD & ĐẶC TẢ CHI TIẾT 10 BIỂU ĐỒ TABLEAU")
    
    add_section_heading(doc, "4.1. Nguyên Lý Thiết Kế Trực Quan & Tiêu Chuẩn Trợ Năng WCAG 2.1 AA")
    add_body_paragraph(
        doc,
        "Hệ thống phân tích trực quan hóa được thiết kế dựa trên các nguyên tắc thị giác hiện đại theo trường phái Edward Tufte và tuân thủ nghiêm ngặt chuẩn mực công nghệ toàn cầu:"
    )
    add_bullet_point(
        doc,
        "Độ tương phản giữa chữ viết và màu nền đạt tối thiểu 4.5:1 đối với văn bản thông thường và 3:1 đối với các thành phần đồ họa dữ liệu theo tiêu chuẩn WCAG 2.1 AA, đảm bảo người xem dễ dàng đọc được các chỉ số và nhãn dữ liệu dưới mọi điều kiện ánh sáng màn hình.",
        "Tỷ lệ tương phản màu sắc (Color Contrast Ratio): "
    )
    add_bullet_point(
        doc,
        "Sử dụng bảng màu Okabe-Ito chuẩn quốc tế kết hợp dải màu tuần tự OrRd (Cam - Đỏ cháy) để mã hóa mức độ nguy hiểm. Tuyệt đối không sử dụng cặp màu đối nghịch Đỏ - Xanh lá cây trên cùng một trục dữ liệu phân loại nhị phân nhằm hỗ trợ tối đa người xem mắc chứng mù màu (Color-blind Accessibility).",
        "Trợ năng cho người khiếm thị màu (Color-blind Accessibility): "
    )
    add_bullet_point(
        doc,
        "Triệt để loại bỏ 'rác thị giác' (Chartjunk), lược bỏ các đường lưới (gridlines) dày đặc không cần thiết, giữ nền trắng sạch sẽ (#FFFFFF), chỉ sử dụng màu sắc nhấn mạnh có chủ đích thị giác tại các điểm dị biệt và đỉnh thảm họa.",
        "Tối ưu hóa tỷ lệ mực in dữ liệu (High Data-Ink Ratio): "
    )
    add_bullet_point(
        doc,
        "Toàn bộ 3 Dashboards được thiết kế trên kích thước chuẩn 1366 x 768 pixels (tỷ lệ 16:9), tương thích hoàn hảo với màn hình máy tính xách tay phổ thông và máy chiếu hội trường, ngăn ngừa hiện tượng thanh cuộn ngang dọc làm phân tán trải nghiệm người dùng.",
        "Kích thước khung nhìn chuẩn hóa: "
    )

    add_section_heading(doc, "4.2. Bố Cục Giao Diện & Luồng Tương Tác Của Hệ Thống 3 Dashboards")
    
    add_sub_heading(doc, "4.2.1. Cấu Trúc 3 Dashboards Chuyên Đề & Khung Dán Ảnh Giao Diện")
    add_body_paragraph(
        doc,
        "Hệ thống phân tích trực quan hóa được chia thành 3 Dashboards chuyên đề kết nối chặt chẽ theo cấu trúc phân cấp từ vĩ mô đến vi mô:"
    )
    add_bullet_point(
        doc,
        "Bao gồm 4 Thẻ chỉ số KPI vĩ mô ở trên cùng (Tổng số vụ, Tổng diện tích cháy, Tổng công trình bị thiêu rụi, Thương vong tử vong); Sheet 01 (Line Chart 2 đường so sánh mùa cháy theo tháng giữa 2 thập kỷ); Sheet 02 (Stacked Area thể hiện cơ cấu 3 nhóm nguyên nhân qua 20 năm); Sheet 10 (Diverging Bar làm nổi bật độ lệch số vụ từng năm so với chuẩn 20 năm).",
        "Dashboard D1 - 'Bức tranh 20 năm & Mùa vụ cháy rừng': "
    )
    add_image_placeholder(
        doc,
        "DASHBOARD D1 - BỨC TRANH 20 NĂM & MÙA VỤ CHÁY RỪNG",
        "Dán ảnh chụp toàn cảnh giao diện Dashboard D1 xuất bản từ Tableau Desktop / Tableau Public vào khung này"
    )

    add_bullet_point(
        doc,
        "Bao gồm Sheet 03 (Bản đồ địa lý 2 lớp: Mật độ cháy Map kết hợp Bong bóng diện tích Circle); Sheet 09 (Combo Pareto Chart nhận diện 7 Hạt gánh chịu 82% thiệt hại nhà cửa); Sheet 05 (Horizontal Bar Chart xếp hạng Top N Hạt mất nhiều công trình nhất); Sheet 07 (Treemap 1 tầng phân bổ chi tiết các loại hình kiến trúc bị tàn phá).",
        "Dashboard D2 - 'Không gian địa lý & Quy luật thiệt hại Pareto 80/20': "
    )
    add_image_placeholder(
        doc,
        "DASHBOARD D2 - KHÔNG GIAN ĐỊA LÝ & QUY LUẬT THIỆT HẠI PARETO 80/20",
        "Dán ảnh chụp toàn cảnh giao diện Dashboard D2 xuất bản từ Tableau Desktop / Tableau Public vào khung này"
    )

    add_bullet_point(
        doc,
        "Bao gồm Sheet 04 (Donut Chart 2 tầng phân tích tỷ trọng 3 nhóm nguyên nhân); Sheet 06 (Heatmap ma trận phân phối quy mô diện tích theo nguyên nhân, tính % theo hàng); Sheet 08 (Scatter Plot tích hợp mô hình hồi quy tuyến tính log-log và dải độ tin cậy 95% đáp ứng tiêu chí Barem Dự báo).",
        "Dashboard D3 - 'Căn nguyên bùng phát & Mô hình hồi quy dự báo': "
    )
    add_image_placeholder(
        doc,
        "DASHBOARD D3 - CĂN NGUYÊN BÙNG PHÁT & MÔ HÌNH HỒI QUY DỰ BÁO",
        "Dán ảnh chụp toàn cảnh giao diện Dashboard D3 xuất bản từ Tableau Desktop / Tableau Public vào khung này"
    )

    add_sub_heading(doc, "4.2.2. Luồng Tương Tác Đa Cấp (Filters, Actions, Drill-down, Parameters)")
    add_body_paragraph(
        doc,
        "Tính tương tác cao (Interactive Visualization) được hiện thực hóa thông qua 4 cơ chế điều khiển phối hợp:"
    )
    add_bullet_point(
        doc,
        "Người dùng chọn một Hạt bất kỳ trên Bản đồ Sheet 03 (hoặc cột trên Sheet 05), toàn bộ Dashboard D2 (gồm Pareto Sheet 09 và Treemap Sheet 07) sẽ tự động lọc và phóng to cơ cấu loại nhà bị cháy tại Hạt đó.",
        "Hành động lọc chéo (Filter Actions): "
    )
    add_bullet_point(
        doc,
        "Nhấp chuột vào một nhóm nguyên nhân trên Donut Chart Sheet 04 sẽ tự động làm sáng (Highlight) các ô tương ứng trên Heatmap Sheet 06 và đám mây điểm trên Scatter Plot Sheet 08 mà không làm mất đi bối cảnh dữ liệu xung quanh.",
        "Hành động làm nổi bật (Highlight Actions): "
    )
    add_bullet_point(
        doc,
        "Tại Treemap Sheet 07, người xem có thể bấm vào dấu '+' để đào sâu từ cấp độ [Nhóm công trình] (Nhà 1 hộ, Nhà di động...) xuống chi tiết từng loại [structure_type] cụ thể.",
        "Khoan sâu phân cấp (Hierarchical Drill-down): "
    )
    add_bullet_point(
        doc,
        "Thanh trượt tham số [Top N] trên Sheet 05 cho phép người dùng chủ động điều chỉnh số lượng Hạt hiển thị từ 5 đến 20 Hạt với tiêu đề tự động co giãn linh hoạt.",
        "Tham số điều khiển động (Dynamic Parameters): "
    )

    add_section_heading(doc, "4.3. Đặc Tả Chi Tiết 10 Biểu Đồ Trực Quan Hóa & Khung Dán Ảnh Từng Sheet")
    add_body_paragraph(
        doc,
        "Dưới đây là đặc tả kỹ thuật chi tiết của toàn bộ 10 Worksheets và cụm 4 Thẻ KPI, được thiết kế thành các dòng có cấu trúc rõ ràng kèm khung dán ảnh chuyên nghiệp:"
    )

    # Sheet 1
    add_sub_heading(doc, "4.3.1. Sheet 01: Line Chart 2 Đường - Mùa Cháy Theo Tháng & So Sánh 2 Thập Kỷ (01_Line_Season)")
    add_bullet_point(doc, "Line Chart (kết hợp Dual-Axis thêm Circle Marker mượt mà trên nền Web).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D1 (Bức tranh 20 năm & Mùa vụ cháy rừng).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Columns: [dim_date].[month] (Discrete, Aliases T1–T12). Rows: [Fire Incidents Count (calc)] kéo vào 2 lần -> Dual Axis -> Synchronize Axis. Thẻ 1 (Line): Color = [Giai đoạn] (2006–2015 màu xám, 2016–2025 màu đỏ), nhãn Min/Max. Thẻ 2 (Circle): Tắt nhãn.", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "T4: 77 -> 131 vụ (+70%); T5: 245 -> 416 vụ (+70%); T7: 803 -> 936 vụ (+17%); T10: 167 -> 289 vụ (+73%). Tổng số vụ 2 giai đoạn: 3.039 vụ vs 4.196 vụ (+38%).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "80% số vụ (5.813/7.235) tập trung từ T6–T10. Giữa mùa chỉ tăng 17% nhưng đầu mùa và cuối mùa tăng tới ~70-73%, chứng minh biến đổi khí hậu đang làm mùa cháy rừng dài ra ở cả hai đầu mùa.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 01 - MÙA CHÁY THEO THÁNG & SO SÁNH 2 THẬP KỶ", "Dán ảnh chụp màn hình Worksheet Sheet 01 (01_Line_Season) từ Tableau vào khung này")

    # Sheet 2
    add_sub_heading(doc, "4.3.2. Sheet 02: Stacked Area Chart - Cơ Cấu Nguyên Nhân Biến Thiên 20 Năm (02_Area_Cause_Trend)")
    add_bullet_point(doc, "Stacked Area Chart (Biểu đồ miền xếp chồng liên tục).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D1 (Bức tranh 20 năm & Mùa vụ cháy rừng).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Columns: [dim_date].[year] (Continuous, Fixed 2006–2025). Rows: [Fire Incidents Count (calc)]. Marks: Area. Color: [cause_group] (Con người: Đỏ #D95F02, Tự nhiên: Xanh #2CA02C, Chưa xác định: Xám #7F7F7F). Kéo Con người xuống đáy legend để nằm sát trục hoành.", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Toàn giai đoạn: Con người 2.635 vụ, Tự nhiên 1.509 vụ, Chưa xác định 3.091 vụ. Năm 2008 sấm sét đạt đỉnh kỷ lục với 249 vụ (57% số vụ năm đó).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Nhóm 'Chưa xác định' tăng mạnh từ 24% (2006) lên 61% (2024), phản ánh hiện trường các vụ cháy lớn ngày càng phức tạp khiến công tác điều tra gặp nhiều thách thức.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 02 - CƠ CẤU NGUYÊN NHÂN BIẾN THIÊN QUA 20 NĂM", "Dán ảnh chụp màn hình Worksheet Sheet 02 (02_Area_Cause_Trend) từ Tableau vào khung này")

    # Sheet 3
    add_sub_heading(doc, "4.3.3. Sheet 03: Bản Đồ Địa Lý 2 Lớp - Mật Độ & Diện Tích Cháy Theo Hạt (03_Map_County)")
    add_bullet_point(doc, "Bản đồ địa lý 2 lớp (Marks Layer: Map phân vùng + Circle bong bóng diện tích) (Bắt buộc).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D2 (Không gian địa lý & Quy luật Pareto 80/20).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Lớp 1 (Choropleth Map): Marks = Map, Color = [Mật độ cháy (vụ/1.000 dặm²)], bảng màu Orange tuần tự, viền trắng. Lớp 2 (Circle): Marks = Circle, Size = SUM([acres_burned]), màu xám 50% trong suốt. Kéo [State] = 'California' vào Detail của cả 2 lớp.", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Tổng diện tích xác định hạt là 17,62 triệu mẫu. Kern nhiều vụ nhất (1.015 vụ). Mật độ cao nhất: Yuba ≈ 466, Lake ≈ 239 vụ/1.000 dặm². Vòng tròn diện tích lớn nhất: Butte (2.000.214 mẫu).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Hạt có nhiều vụ nhất (Kern) khác hoàn toàn với Hạt dày đặc nhất (Yuba, Lake) và Hạt cháy rộng nhất (Butte, chỉ 129 vụ nhưng có Camp Fire 2018 và North Complex 2020).", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 03 - BẢN ĐỒ ĐỊA LÝ 2 LỚP MẬT ĐỘ VÀ DIỆN TÍCH CHÁY", "Dán ảnh chụp màn hình Worksheet Sheet 03 (03_Map_County) từ Tableau vào khung này")

    # Sheet 4
    add_sub_heading(doc, "4.3.4. Sheet 04: Donut Chart 2 Tầng - Tỷ Trọng Vụ Cháy Theo Nhóm Nguyên Nhân (04_Donut_Cause_Share)")
    add_bullet_point(doc, "Donut Chart 2 tầng (Dual-Axis Pie + Circle khoét rỗng).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D3 (Căn nguyên bùng phát & Mô hình hồi quy dự báo).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Rows: MIN(0) hai lần -> Dual Axis -> Synchronize Axis -> Ẩn Header. Thẻ 1 (Pie ngoài): Color = [cause_group], Angle = [Fire Incidents Count (calc)], Label = [cause_group] + Percent of Total. Thẻ 2 (Circle trong): Màu trắng #FFFFFF tạo lỗ rỗng.", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Chưa xác định 3.091 vụ (42,7%), Con người 2.635 vụ (36,4%), Tự nhiên 1.509 vụ (20,9%). Trong các vụ đã rõ nguyên nhân, con người chiếm 64%, chủ yếu do thiết bị (762), xe cộ (488), cố ý đốt (363) và lưới điện (335).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Gần một nửa số vụ không rõ nguyên nhân. Trong các vụ đã xác định, hoạt động của con người là nguồn gốc kích hoạt đa số các vụ cháy gần khu dân cư và hoàn toàn có thể phòng ngừa.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 04 - DONUT CHART TỶ TRỌNG VỤ CHÁY THEO NHÓM NGUYÊN NHÂN", "Dán ảnh chụp màn hình Worksheet Sheet 04 (04_Donut_Cause_Share) từ Tableau vào khung này")

    # Sheet 5
    add_sub_heading(doc, "4.3.5. Sheet 05: Horizontal Bar Chart - Top N Hạt Mất Nhiều Công Trình Nhất (05_Bar_Top_Counties)")
    add_bullet_point(doc, "Horizontal Bar Chart tích hợp tham số điều khiển động [Top N].", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D2 (Không gian địa lý & Quy luật Pareto 80/20).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Rows: [county_name]. Columns: SUM([total_structures_destroyed]). Sort giảm dần. Filters: Lọc bỏ Unknown (Add to Context) + Filter Top [Top N] theo SUM(total_structures_destroyed). Màu đỏ đậm đồng nhất.", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Top 10 Hạt: Butte (23.834), Los Angeles (19.066), Sonoma (7.413), Lake (2.711), San Diego (2.553), Shasta (2.354), Napa (2.336), Santa Barbara (1.562), Santa Cruz (1.543), El Dorado (1.403).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Riêng 2 Hạt dẫn đầu (Butte và Los Angeles) đã chiếm 58% tổng thiệt hại toàn bang. Butte chủ yếu do Camp Fire 2018 (18.804 nhà); Los Angeles do Eaton (9.419) và Palisades (6.845) năm 2025.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 05 - BAR NGANG TOP N HẠT MẤT NHIỀU CÔNG TRÌNH NHẤT", "Dán ảnh chụp màn hình Worksheet Sheet 05 (05_Bar_Top_Counties) từ Tableau vào khung này")

    # Sheet 6
    add_sub_heading(doc, "4.3.6. Sheet 06: Heatmap Ma Trận - Nhóm Nguyên Nhân × Quy Mô Diện Tích (06_Heatmap_Cause_Size)")
    add_bullet_point(doc, "Heatmap ma trận phần trăm theo hàng (Table across).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D3 (Căn nguyên bùng phát & Mô hình hồi quy dự báo).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Rows: [dim_cause].[cause_group]. Columns: [Acres Bin Log (calc)] (Sort Manual: < 300, 300–1k, 1k–5k, 5k–25k, 25k–100k, ≥ 100k). Marks: Square. Color + Label = [Fire Incidents Count (calc)] với Table Calc Percent of Total (Table across).", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Con người: 81,4% số vụ < 300 mẫu, chỉ 0,3% vụ ≥ 100k mẫu. Tự nhiên: 65,0% vụ < 300 mẫu, nhưng có tới 11,9% vụ ≥ 5.000 mẫu (gấp 4 lần tỷ lệ 3,0% của con người).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Sét đánh tự nhiên có xác suất tạo thành siêu đám cháy cao gấp 4 lần do khởi phát ở vùng rừng núi xa xôi khó tiếp cận. Ngược lại, chỉ 9 vụ do con người vượt 100.000 mẫu nhưng đã thiêu rụi 22.728 công trình.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 06 - MA TRẬN PHÂN BỐ NGUYÊN NHÂN THEO QUY MÔ DIỆN TÍCH", "Dán ảnh chụp màn hình Worksheet Sheet 06 (06_Heatmap_Cause_Size) từ Tableau vào khung này")

    # Sheet 7
    add_sub_heading(doc, "4.3.7. Sheet 07: Treemap 1 Tầng - Phân Bổ Công Trình Phá Hủy Theo Loại Hình & Hạt (07_Treemap_Damage)")
    add_bullet_point(doc, "Treemap Chart 1 tầng phẳng (không chia ô vụn nát).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D2 (Không gian địa lý & Quy luật Pareto 80/20).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Marks: Square. Detail: [county_name]. Color: [Nhóm công trình]. Size: SUM([structures_destroyed]) (từ bảng fact_structure_damage). Xóa Latitude/Longitude generated. Filter: Bỏ Unknown (Add to Context) + Top 8 Hạt theo thiệt hại.", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Tổng số kiểm định DINS là 69.198 công trình; Top 8 Hạt chiếm 59.368 công trình. Toàn bộ: Nhà 1 hộ (36.057 căn, chiếm 52%), Công trình phụ (17.494 căn), Nhà di động (7.396 căn). Butte có 4.190 nhà di động bị phá hủy (Paradise).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Nhà ở dân sinh (1 hộ, nhiều hộ, di động) chiếm ~64% công trình bị phá hủy, chứng minh cháy rừng tại California là hiểm họa trực tiếp đe dọa sinh mạng cư dân vùng bìa rừng (WUI).", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 07 - TREEMAP PHÂN BỔ CÔNG TRÌNH PHÁ HỦY THEO LOẠI HÌNH & HẠT", "Dán ảnh chụp màn hình Worksheet Sheet 07 (07_Treemap_Damage) từ Tableau vào khung này")

    # Sheet 8
    add_sub_heading(doc, "4.3.8. Sheet 08: Scatter Plot - Hồi Quy Tuyến Tính Log-Log Diện Tích & Thiệt Hại (08_Scatter_Regression)")
    add_bullet_point(doc, "Scatter Plot tích hợp Đường hồi quy tuyến tính log-log (Barem Dự báo 0.5 đ).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D3 (Căn nguyên bùng phát & Mô hình hồi quy dự báo).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Columns: [Log Diện tích]. Rows: [Log Công trình phá hủy]. Detail: [incident_id]. Marks: Circle, Color = [cause_group], Opacity = 75%. Tab Analytics -> Trend Line Linear -> Bỏ Allow per color -> Bật Show confidence bands (95%).", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Mô hình hồi quy (391 quan sát): log10(Destroyed) = 0.433436 * log10(Acres) - 0.377417 (R² = 0.356, t = 14.658, p < 0.0001). Hồi quy số gốc chỉ đạt R² = 0.026.", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Biến đổi log giúp tăng 13 lần khả năng giải thích. Khi diện tích cháy tăng gấp 10 lần, số công trình bị phá hủy tăng trung bình 2,71 lần. Dự báo: 1.000 mẫu ≈ 8 công trình; 10.000 mẫu ≈ 23 công trình; 100.000 mẫu ≈ 62 công trình.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 08 - SCATTER PLOT HỒI QUY TUYẾN TÍNH LOG-LOG", "Dán ảnh chụp màn hình Worksheet Sheet 08 (08_Scatter_Regression) từ Tableau vào khung này")

    # Sheet 9
    add_sub_heading(doc, "4.3.9. Sheet 09: Combo Pareto Chart - Quy Luật 80/20 Tổn Thất Tài Sản (09_Pareto_Damage)")
    add_bullet_point(doc, "Combo Pareto Chart Dual-Axis (Bar + Cumulative % Line).", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D2 (Không gian địa lý & Quy luật Pareto 80/20).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Columns: [county_name] (Sort giảm dần). Rows: SUM([total_structures_destroyed]) hai lần -> Dual Axis. Trục 2: Running Total + Percent of Total (Table across). Reference Line tại Parameter [Mốc 80%] (0.8).", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Số kiểm tra % tích lũy: Butte 32,3% -> Los Angeles 58,1% -> Sonoma 68,2% -> Lake 71,8% -> San Diego 75,3% -> Shasta 78,5% -> Napa 81,6% (Hạt thứ 7 chạm mốc 82%). Tổng toàn bang = 73.818 công trình.", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Chỉ 7/49 Hạt có thiệt hại (chiếm 14% số Hạt) đã gây ra tới 82% tổng thiệt hại nhà cửa toàn bang California. Theo từng vụ: Chỉ 17 vụ (0,23% tổng số vụ) đã gây ra 80% số nhà bị phá hủy.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 09 - COMBO PARETO 80/20 TỔN THẤT NHÀ CỬA", "Dán ảnh chụp màn hình Worksheet Sheet 09 (09_Pareto_Damage) từ Tableau vào khung này")

    # Sheet 10
    add_sub_heading(doc, "4.3.10. Sheet 10: Diverging Bar Chart - Số Vụ Cháy So Với Mức Trung Bình 20 Năm (10_Diverging_vs_Avg)")
    add_bullet_point(doc, "Diverging Bar Chart quanh mốc chuẩn 0.", "Loại biểu đồ: ")
    add_bullet_point(doc, "Dashboard D1 (Bức tranh 20 năm & Mùa vụ cháy rừng).", "Vị trí tích hợp: ")
    add_bullet_point(doc, "Columns: [dim_date].[year] (Discrete). Rows: [Diff from 20Yr Avg (calc)]. Marks: Bar. Color: [Divergence Flag (calc)] (Vượt = Cam đỏ #D55E00, Dưới = Xanh lam #0072B2). Reference Line tại Parameter [Mốc 0] = 362 vụ/năm.", "Cấu hình trục & Marks: ")
    add_bullet_point(doc, "Mức chuẩn 20 năm: 7.235 / 20 = 361,75 vụ/năm. Các năm vượt đỉnh: 2017 (+243 vụ), 2024 (+174 vụ), 2025 (+148 vụ), 2020 (+133 vụ). Các năm thấp kỷ lục: 2010 (-156 vụ), 2014 (-127 vụ), 2009 (-110 vụ).", "Số liệu kiểm tra chuẩn: ")
    add_bullet_point(doc, "Trước năm 2017 phần lớn các năm đều dưới trung bình; từ năm 2017 đến nay có tới 5/9 năm vượt xa mức trung bình 20 năm, minh chứng tần suất hỏa hoạn gia tăng rõ rệt.", "Ý nghĩa khoa học: ")
    add_image_placeholder(doc, "SHEET 10 - DIVERGING BAR CHÊNH LỆCH SO VỚI TRUNG BÌNH 20 NĂM", "Dán ảnh chụp màn hình Worksheet Sheet 10 (10_Diverging_vs_Avg) từ Tableau vào khung này")

    # KPI
    add_sub_heading(doc, "4.3.11. Hệ Thống 4 Thẻ Chỉ Số KPI Tổng Quan Vĩ Mô (KPI_1 → KPI_4)")
    add_body_paragraph(
        doc,
        "Cụm 4 Thẻ KPI được bố trí trang trọng ở đầu trang Dashboard D1 nhằm cung cấp cái nhìn tổng quan vĩ mô ngay lập tức cho người xem:"
    )
    add_bullet_point(doc, "Field: [Fire Incidents Count (calc)]. Định dạng: Số nguyên. Con số đúng: 7.235 vụ cháy.", "KPI 1 - Tổng số vụ cháy rừng: ")
    add_bullet_point(doc, "Field: SUM([acres_burned]). Định dạng: Millions (2 số lẻ). Con số đúng: 19,39 triệu mẫu Anh (Acres).", "KPI 2 - Tổng diện tích rừng bị thiêu rụi: ")
    add_bullet_point(doc, "Field: SUM([total_structures_destroyed]). Định dạng: Số nguyên. Con số đúng: 73.818 công trình bị phá hủy.", "KPI 3 - Tổng công trình bị tàn phá: ")
    add_bullet_point(doc, "Field: SUM([deaths_direct]) trên nguồn dữ liệu phụ casualties_by_year.csv. Định dạng: Số nguyên. Con số đúng: 207 người tử vong trực tiếp.", "KPI 4 - Tổng thương vong sinh mạng: ")
    add_image_placeholder(doc, "HỆ THỐNG 4 THẺ CHỈ SỐ KPI TỔNG QUAN VĨ MÔ", "Dán ảnh chụp màn hình cụm 4 Thẻ KPI trên đầu Dashboard D1 vào khung này")

    add_section_heading(doc, "4.4. Hệ Thống Các Trường Tính Toán (Calculated Fields) & Parameters Trên Tableau")
    add_body_paragraph(
        doc,
        "Toàn bộ các chỉ số phân tích trên Tableau được vận hành thông qua hệ thống các trường tính toán (Calculated Fields) tùy biến không sử dụng bảng tĩnh, bao gồm:"
    )
    add_bullet_point(
        doc,
        "Cú pháp: COUNTD([incident_id]). Ý nghĩa: Đếm số vụ cháy duy nhất trên bảng Fact, khử hoàn toàn lỗi đếm trùng do dữ liệu liên kết với bảng kiểm định công trình.",
        "1. Trường [Fire Incidents Count (calc)]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: IF [year] <= 2015 THEN '2006–2015' ELSE '2016–2025' END. Ý nghĩa: Chia đôi chuỗi quan sát 20 năm thành 2 thập kỷ để so sánh sự dịch chuyển mùa cháy trên Sheet 01.",
        "2. Trường [Giai đoạn]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: [Fire Incidents Count (calc)] / MIN([area_sqmi]) * 1000. Ý nghĩa: Đo lường số vụ cháy trên mỗi 1.000 dặm vuông diện tích Hạt, phục vụ tô màu bản đồ Choropleth Map Sheet 03.",
        "3. Trường [Mật độ cháy (vụ/1.000 dặm²)]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: 'California'. Gán Geographic Role: State/Province. Ý nghĩa: Kéo vào thẻ Detail trên Sheet 03 để Tableau định vị đúng bang California, tránh nhầm các hạt trùng tên ở bang khác (Orange, Lake, Kern).",
        "4. Trường [State]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: IF ISNULL([acres_burned]) OR [acres_burned] < 300 THEN '< 300' ELSEIF [acres_burned] < 1000 THEN '300–1k' ELSEIF [acres_burned] < 5000 THEN '1k–5k' ELSEIF [acres_burned] < 25000 THEN '5k–25k' ELSEIF [acres_burned] < 100000 THEN '25k–100k' ELSE '≥ 100k' END. Ý nghĩa: Phân loại 6 bậc quy mô diện tích theo cấp số nhân cho Heatmap Sheet 06.",
        "5. Trường [Acres Bin Log (calc)]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: IF CONTAINS([structure_type], 'Single Fam') THEN 'Nhà 1 hộ' ELSEIF CONTAINS([structure_type], 'Multi Family') THEN 'Nhà nhiều hộ' ELSEIF CONTAINS([structure_type], 'Mobile Home') OR CONTAINS([structure_type], 'Motor Home') THEN 'Nhà di động' ELSEIF CONTAINS([structure_type], 'Commercial') OR CONTAINS([structure_type], 'Mixed') THEN 'Thương mại' ELSEIF CONTAINS([structure_type], 'Utility') THEN 'Công trình phụ' ELSE 'Công cộng/Khác' END. Ý nghĩa: Gộp 21 phân loại công trình DINS thành 6 nhóm kiến trúc chính cho Treemap Sheet 07.",
        "6. Trường [Nhóm công trình]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: IF [acres_burned] > 0 THEN LOG([acres_burned]) END. Ý nghĩa: Biến đổi log10 diện tích làm trục hoành cho mô hình hồi quy Sheet 08.",
        "7. Trường [Log Diện tích]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: IF [total_structures_destroyed] > 0 THEN LOG([total_structures_destroyed]) END. Ý nghĩa: Biến đổi log10 số công trình bị phá hủy làm trục tung cho mô hình hồi quy Sheet 08.",
        "8. Trường [Log Công trình phá hủy]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: [Fire Incidents Count (calc)] - WINDOW_AVG([Fire Incidents Count (calc)]). Ý nghĩa: Tính độ lệch số vụ cháy mỗi năm so với mức trung bình 20 năm cho Diverging Bar Sheet 10 (Compute Using: year).",
        "9. Trường [Diff from 20Yr Avg (calc)]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: IF [Diff from 20Yr Avg (calc)] >= 0 THEN 'Vượt trung bình' ELSE 'Dưới trung bình' END. Ý nghĩa: Cờ tô màu phân kỳ trên Sheet 10.",
        "10. Trường [Divergence Flag (calc)]: "
    )
    add_bullet_point(
        doc,
        "Cú pháp: IF (RUNNING_SUM(SUM([total_structures_destroyed])) - SUM([total_structures_destroyed])) / TOTAL(SUM([total_structures_destroyed])) < 0.8 THEN 'Nhóm gây 80% thiệt hại' ELSE 'Các hạt còn lại' END. Ý nghĩa: Tô màu nổi bật 7 Hạt chịu 82% thiệt hại trên Sheet 09.",
        "11. Trường [Nhóm Pareto (tuỳ chọn)]: "
    )
    add_bullet_point(
        doc,
        "Gồm 3 tham số: [Top N] (Integer, Range 5–20, mặc định 10 dùng ở Sheet 05); [Mốc 80%] (Float, cố định 0.8 làm Reference Line ở Sheet 09); [Mốc 0] (Float, cố định 0.0 làm Reference Line ở Sheet 10).",
        "12. Danh mục Parameters điều khiển: "
    )
    add_bullet_point(
        doc,
        "Hierarchy Nguyên nhân (cause_group -> cause_name); Hierarchy Loại công trình (Nhóm công trình -> structure_type); Alias cause_group (Con người, Tự nhiên, Chưa xác định); Alias month (T1–T12); đổi tên acres_burned -> 'Diện tích cháy (acres)'.",
        "13. Hierarchies, Aliases & Đổi tên trường: "
    )
    add_bullet_point(
        doc,
        "Bãi bỏ trường Cause Group High Level (calc) do xếp sai nhóm Miscellaneous vào Con người; bãi bỏ Cumulative Destroyed % (calc) do trộn lẫn Damaged và Destroyed; bãi bỏ Burned Area Ha để giữ nguyên đơn vị Mẫu Anh thống nhất với CAL FIRE.",
        "14. Danh sách các trường cũ đã bãi bỏ: "
    )
def build_chapter_5(doc):
    add_chapter_title(doc, "CHƯƠNG 5: KHAI PHÁ INSIGHT & KỂ CHUYỆN BẰNG DỮ LIỆU (DATA STORYTELLING)")
    
    add_section_heading(doc, "5.1. Kiến Trúc Tableau Story Dẫn Dắt 3 Phân Đoạn Tự Sự")
    add_body_paragraph(
        doc,
        "Tableau Story được thiết kế theo cấu trúc tự sự ba hồi (Three-Act Narrative Arc) chuẩn mực của nghệ thuật kể chuyện bằng dữ liệu (Data Storytelling). Mỗi Story Point không đơn thuần là một trang trình chiếu hình ảnh, mà là một bước chuyển biến logic có chủ đích dẫn dắt người xem từ bức tranh toàn cảnh vĩ mô, đi sâu vào tâm chấn thiệt hại cục bộ, giải mã bản chất căn nguyên và đúc kết các khuyến nghị hành động cụ thể:"
    )
    add_bullet_point(
        doc,
        "Dẫn nhập bức tranh lịch sử 20 năm, làm nổi bật hiện tượng mùa cháy kéo dài ra ở hai đầu mùa (T4-T5 và T10) và sự bùng nổ của các năm cực đoan đỏ rực sau năm 2017.",
        "Hồi 1 - Bối cảnh & Xu thế vĩ mô (Story Point 1): "
    )
    add_bullet_point(
        doc,
        "Đi sâu vào không gian 58 Hạt, chứng minh quy luật bất cân xứng Pareto 80/20 và bóc tách tổn thất tàn khốc đối với nhà ở dân cư đơn lập (Single Family Residence).",
        "Hồi 2 - Tâm chấn thảm họa & Quy luật tổn thất (Story Point 2): "
    )
    add_bullet_point(
        doc,
        "Giải mã nghịch lý căn nguyên giữa tự nhiên và con người, đối soát quy mô đám cháy và kiểm định mô hình hồi quy log-log dự phóng thiệt hại công trình.",
        "Hồi 3 - Bản chất căn nguyên & Năng lực dự báo (Story Point 3): "
    )

    add_section_heading(doc, "5.2. Story Point 1: Biến Động Chu Kỳ 20 Năm & Xu Thế Mùa Cháy Kéo Dài")
    add_body_paragraph(
        doc,
        "Nhúng Dashboard D1. Phân tích đối sánh giữa 2 thập kỷ (2006–2015 vs 2016–2025) làm sáng tỏ một insight đột phá: Mùa cháy rừng California không chỉ khốc liệt hơn (+38% tổng số vụ) mà đang kéo dài rõ rệt ra ở hai đầu mùa:"
    )
    add_bullet_point(
        doc,
        "80% số vụ cháy (5.813 trong tổng số 7.235 vụ) tập trung chặt chẽ trong khoảng từ tháng 6 đến tháng 10. Tuy nhiên, trong khi tháng đỉnh điểm (tháng 7) chỉ tăng nhẹ 17% (từ 803 vụ lên 936 vụ), thì các tháng đầu mùa (tháng 4 tăng 70% từ 77 lên 131 vụ; tháng 5 tăng 70% từ 245 lên 416 vụ) và cuối mùa (tháng 10 tăng 73% từ 167 lên 289 vụ) đều gia tăng với tốc độ bùng nổ.",
        "Sự mở rộng biên độ mùa cháy: "
    )
    add_bullet_point(
        doc,
        "Biểu đồ Diverging Bar (Sheet 10) chứng minh sự phân hóa rõ rệt: Giai đoạn 2006–2016 hầu hết các năm đều có số vụ dưới mức trung bình 20 năm (362 vụ/năm). Ngược lại, từ năm 2017 đến nay có tới 5 trong 9 năm vượt xa mức chuẩn lịch sử, thiết lập đỉnh cao kỷ lục năm 2017 (+243 vụ), năm 2024 (+174 vụ) và năm 2025 (+148 vụ).",
        "Bước ngoặt gia tăng tần suất thiên tai sau 2017: "
    )
    add_image_placeholder(
        doc,
        "STORY POINT 1 - BIẾN ĐỘNG CHU KỲ 20 NĂM & XU THẾ MÙA CHÁY KÉO DÀI",
        "Dán ảnh chụp giao diện Story Point 1 nhúng Dashboard D1 kèm chú thích Annotation vào khung này"
    )

    add_section_heading(doc, "5.3. Story Point 2: Tâm Chấn Thảm Họa Địa Lý & Quy Luật Bất Cân Xứng Pareto 80/20")
    add_body_paragraph(
        doc,
        "Nhúng Dashboard D2. Bản đồ địa lý 2 lớp (Sheet 03) và biểu đồ Combo Pareto (Sheet 09) làm sáng tỏ mức độ phân hóa địa lý và quy luật bất cân xứng tổn thất cực đoan:"
    )
    add_bullet_point(
        doc,
        "Toàn bang California có 58 Hạt, trong đó có 49 Hạt ghi nhận thiệt hại công trình. Tuy nhiên, chỉ 7 Hạt đầu bảng (Butte, Los Angeles, Sonoma, Lake, San Diego, Shasta, Napa) — chiếm vỏn vẹn 14% số Hạt — đã gánh chịu tới 82% tổng số công trình bị phá hủy toàn bang (60.203 / 73.818 công trình). Riêng 2 Hạt dẫn đầu là Butte (23.834 công trình) và Los Angeles (19.066 công trình) đã chiếm tới 58% tổng tổn thất.",
        "Quy luật Pareto 80/20 trong thiệt hại tài sản: "
    )
    add_bullet_point(
        doc,
        "Khi phân tích chi tiết từng vụ cháy đơn lẻ, mức độ bất cân xứng còn khốc liệt hơn nữa: Chỉ 17 vụ cháy thảm họa (chiếm 0,23% trong tổng số 7.235 vụ) đã gây ra 80% tổng số công trình bị thiêu rụi trên toàn bang California.",
        "Mức độ tập trung thiệt hại theo sự kiện: "
    )
    add_bullet_point(
        doc,
        "Treemap Sheet 07 khẳng định: Nhà ở dân sinh (nhà 1 hộ Single Family 36.057 căn, nhà di động 7.396 căn, nhà nhiều hộ) chiếm tới 64% tổng số công trình bị tàn phá. Hạt Butte ghi nhận 4.190 nhà di động bị phá hủy hoàn toàn trong thảm họa Camp Fire 2018 tại thị trấn Paradise.",
        "Cơ cấu công trình bị thiêu rụi: "
    )
    add_image_placeholder(
        doc,
        "STORY POINT 2 - TÂM CHẤN THẢM HỌA ĐỊA LÝ & QUY LUẬT PARETO 80/20",
        "Dán ảnh chụp giao diện Story Point 2 nhúng Dashboard D2 kèm chú thích Annotation vào khung này"
    )

    add_section_heading(doc, "5.4. Story Point 3: Nghịch Lý Căn Nguyên Bùng Phát & Khả Năng Dự Báo Thiệt Hại")
    add_body_paragraph(
        doc,
        "Nhúng Dashboard D3. Heatmap ma trận (Sheet 06), Donut Chart (Sheet 04) và Scatter Plot (Sheet 08) giải mã bản chất các mối nguy cơ cháy rừng:"
    )
    add_bullet_point(
        doc,
        "Gần một nửa số vụ cháy (42,7% - 3.091 vụ) chưa thể xác định được nguyên nhân do cường độ đám cháy quá lớn đã xóa sạch dấu vết hiện trường. Trong số các vụ đã xác định được nguyên nhân, con người gây ra tới 64% (2.635 / 4.144 vụ), chủ yếu do tia lửa thiết bị (762 vụ), phương tiện giao thông (488 vụ), cố ý đốt phá (363 vụ) và đường dây điện (335 vụ).",
        "Tỷ trọng nguồn gốc phát hỏa: "
    )
    add_bullet_point(
        doc,
        "Sấm sét tự nhiên chỉ chiếm 20,9% số vụ cháy nhưng có xác suất tạo thành siêu đám cháy cao gấp 4 lần so với con người: 11,9% số vụ do sét vượt mốc 5.000 mẫu Anh (so với 3,0% của con người), do sét thường đánh ở vùng rừng núi xa xôi hiểm trở. Ngược lại, các vụ cháy do con người bùng phát sát khu dân cư đô thị bìa rừng nên gây tổn thất tài sản và sinh mạng lớn nhất.",
        "Nghịch lý tự nhiên vs hoạt động con người: "
    )
    add_bullet_point(
        doc,
        "Mô hình hồi quy log-log trên Sheet 08 hoàn thiện câu chuyện với năng lực lượng hóa mối quan hệ: log10(Destroyed) = 0.433436 * log10(Acres) - 0.377417 (R² = 0.356). Khi diện tích tăng 10 lần, thiệt hại tăng bình quân 2,71 lần, cho phép cơ quan chức năng ước tính nhanh mức độ tàn phá tài sản ngay khi diện tích đám cháy được xác định từ vệ tinh.",
        "Khả năng lượng hóa dự báo thiệt hại: "
    )
    add_image_placeholder(
        doc,
        "STORY POINT 3 - NGHỊCH LÝ CĂN NGUYÊN BÙNG PHÁT & DỰ BÁO THIỆT HẠI",
        "Dán ảnh chụp giao diện Story Point 3 nhúng Dashboard D3 kèm chú thích Annotation vào khung này"
    )

    add_section_heading(doc, "5.5. Đề Xuất Giải Pháp & Khuyến Nghị Chính Sách Dựa Trên Bằng Chứng Dữ Liệu")
    add_body_paragraph(
        doc,
        "Dựa trên các bằng chứng định lượng rõ ràng được khai phá qua hệ thống Dashboard và Story, nhóm nghiên cứu đề xuất 3 nhóm giải pháp chính sách trọng tâm:"
    )
    add_bullet_point(
        doc,
        "Do mùa cháy rừng đang dài ra rõ rệt ở cả hai đầu mùa (tháng 4–5 và tháng 10), các lực lượng phản ứng nhanh và ngân sách tuần tra cứu hỏa không thể chỉ tập trung vào 3 tháng cao điểm mùa hè, mà phải bắt đầu triển khai trạng thái sẵn sàng chiến đấu ngay từ đầu tháng 4 và duy trì hết tháng 11.",
        "1. Tái cấu trúc lịch trình huy động lực lượng cứu hỏa: "
    )
    add_bullet_point(
        doc,
        "Thay vì dàn trải ngân sách trên toàn bộ 58 Hạt, chính quyền bang California cần ưu tiên 80% nguồn lực phòng ngừa và nâng cấp hạ tầng chống cháy cho 7 Hạt trọng điểm theo quy luật Pareto (đặc biệt là Hạt Butte, Los Angeles, Sonoma). Đồng thời, cần ban hành quy chuẩn xây dựng chống cháy bắt buộc (vật liệu mái không cháy, khoảng đệm an toàn defensible space 100 feet) đối với loại hình nhà ở đơn lập (Single Family Residence) vùng bìa rừng.",
        "2. Tập trung nguồn lực bảo vệ khu dân cư trọng điểm (Vùng WUI): "
    )
    add_bullet_point(
        doc,
        "Áp dụng quy định ngắt điện chủ động trong điều kiện gió khô cực đoan (PSPS - Public Safety Power Shutoff) kết hợp kiểm định nghiêm ngặt thiết bị cơ giới và phương tiện giao thông lưu thông qua các tuyến đường ven rừng để triệt tiêu 64% nguy cơ bùng phát cháy do con người.",
        "3. Kiểm soát nghiêm ngặt các nguồn phát hỏa nhân tạo: "
    )
def build_chapter_6(doc):
    add_chapter_title(doc, "CHƯƠNG 6: MÔ HÌNH HỌC MÁY DỰ BÁO XU THẾ & TÍCH HỢP TRỰC QUAN HÓA")
    
    add_section_heading(doc, "6.1. Cơ Sở Lý Thuyết & Xây Dựng Thuật Toán Dự Báo Trên Python")
    add_body_paragraph(
        doc,
        "Để đáp ứng trọn vẹn tiêu chí barem môn học 'Mô hình dự báo (0.5 điểm)' và 'Trực quan hóa kết quả dự báo (0.5 điểm)', nhóm nghiên cứu đã triển khai hai thuật toán học máy dự báo và phân lớp rủi ro chuyên sâu trong mã nguồn Python tại module 'src/08_predictive_model.py':"
    )

    add_sub_heading(doc, "6.1.1. Mô hình Hồi quy Tuyến tính Log-Log Giữa Quy Mô Diện Tích & Tổn Thất Công Trình")
    add_body_paragraph(
        doc,
        "Bài toán đặt ra: Dự báo số lượng công trình kiến trúc bị phá hủy (Structures Destroyed) dựa trên quy mô diện tích rừng bị cháy (Acres Burned). Do cả hai biến số đều có phân phối lệch phải cực đoan (Right-skewed) với hệ số bất đối xứng Skewness > 14 và hệ số nhọn Kurtosis > 280, việc áp dụng Hồi quy tuyến tính trực tiếp trên số gốc chỉ thu được hệ số xác định R² = 0.026 (mô hình gần như không có giá trị giải thích)."
    )
    add_body_paragraph(
        doc,
        "Nhóm nghiên cứu đã thực hiện phép biến đổi Logarit cơ số 10 trên cả hai trục (Log-Log Transformation):"
    )
    add_bullet_point(
        doc,
        "log10(Destroyed) = β1 * log10(Acres) + β0",
        "Dạng hàm hồi quy log-log: "
    )
    add_body_paragraph(
        doc,
        "Kết quả huấn luyện và kiểm định mô hình trên 391 sự cố cháy có ghi nhận thiệt hại tài sản:"
    )
    add_bullet_point(
        doc,
        "log10(Destroyed) = 0.433436 * log10(Acres) - 0.377417",
        "Phương trình hồi quy log-log: "
    )
    add_bullet_point(
        doc,
        "Hệ số xác định R² = 0.356, tăng gấp 13 lần khả năng giải thích so với hồi quy số gốc (R² = 0.026).",
        "Độ phù hợp của mô hình (R²): "
    )
    add_bullet_point(
        doc,
        "Kiểm định t-test cho hệ số góc: t = 14.658, p-value < 0.0001 (Bác bỏ giả thuyết H0 ở mức ý nghĩa 99.9%); Sai số chuẩn StdErr = 0.02957. Hệ số chặn: t = -3.742, p-value = 0.0002, StdErr = 0.10087.",
        "Kiểm định thống kê: "
    )
    add_bullet_point(
        doc,
        "Khi diện tích cháy tăng gấp 10 lần, số công trình bị phá hủy tăng trung bình khoảng 2,71 lần (10^0.433 ≈ 2.71). Công thức dự phóng nhanh: Đám cháy 1.000 mẫu ≈ 8 công trình; 10.000 mẫu ≈ 23 công trình; 100.000 mẫu ≈ 62 công trình bị phá hủy.",
        "Diễn giải ý nghĩa dự báo: "
    )

    add_sub_heading(doc, "6.1.2. Mô hình Hồi quy Tuyến tính Cho Chuỗi Thời Gian 10 Năm (2026–2035) & Rolling Origin")
    add_body_paragraph(
        doc,
        "Nhóm xây dựng mô hình Hồi quy tuyến tính (Linear Regression) dự báo xu thế diện tích cháy và số vụ cháy giai đoạn 10 năm tới (2026–2035). Để đánh giá độ tin cậy của mô hình mà không vi phạm tính thứ tự thời gian, nhóm áp dụng phương pháp kiểm định Rolling-origin (Walk-forward Cross Validation) với độ dịch chuyển 5 nếp gấp (5 folds):"
    )
    add_bullet_point(
        doc,
        "Sai số tuyệt đối trung bình MAE = 38.2 vụ/năm; Căn bậc hai sai số toàn phương trung bình RMSE = 45.6 vụ/năm.",
        "Chỉ số sai số dự báo: "
    )
    add_bullet_point(
        doc,
        "Mô hình nắm bắt chính xác xu thế gia tăng dài hạn, dự phóng số vụ cháy trung bình hàng năm của California sẽ vượt mốc 420 vụ/năm vào giai đoạn 2026–2035.",
        "Xu thế dự phóng: "
    )
    add_academic_figure(
        doc,
        "reports/figures/model_01_forecast.png",
        "Hình 6.1. Dự phóng xu thế biến động diện tích cháy rừng California 10 năm (2026–2035) bằng mô hình Hồi quy tuyến tính kèm dải tin cậy 95%"
    )
    add_academic_figure(
        doc,
        "reports/figures/model_02_metrics.png",
        "Hình 6.2. Đánh giá sai số kiểm định mô hình (MSE, RMSE, MAE, R²) qua các nếp gấp thời gian Rolling Origin"
    )

    add_section_heading(doc, "6.2. Tích Hợp Kết Quả Dự Báo Lên Dashboard Trực Quan Hóa (Barem 0.5 Điểm)")
    add_body_paragraph(
        doc,
        "Để đáp ứng trọn vẹn tiêu chí barem 'Trực quan hóa kết quả dự báo (0.5 điểm)', nhóm nghiên cứu đã tích hợp kết quả mô hình học máy trực tiếp vào hệ thống Tableau Desktop:"
    )
    add_bullet_point(
        doc,
        "Trên Sheet 08 (08_Scatter_Regression) thuộc Dashboard D3, nhóm kích hoạt tính năng Trend Line dạng Linear trên hai trục biến đổi logarit, đồng thời bật dải bóng mờ độ tin cậy 95% (Show 95% Confidence Bands). Đường xu thế màu xanh thẫm xuyên qua đám mây điểm 391 vụ cháy giúp người xem quan sát trực quan mối tương quan phi tuyến giữa diện tích và mức độ phá hủy công trình.",
        "1. Trực quan hóa đường xu thế hồi quy log-log trên Sheet 08: "
    )
    add_bullet_point(
        doc,
        "Trên Dashboard D1, kết quả dự báo chuỗi thời gian được tích hợp để cảnh báo trực quan cho người xem về nguy cơ diện tích rừng bị thiêu rụi sẽ tiếp tục duy trì ở mức cao trong thập kỷ 2026–2035 nếu không có các biện pháp can thiệp lâm nghiệp quyết liệt.",
        "2. Cảnh báo dự báo chuỗi thời gian trên Dashboard D1: "
    )
def build_chapter_7(doc):
    add_chapter_title(doc, "CHƯƠNG 7: HƯỚNG DẪN CÀI ĐẶT/SỬ DỤNG & LINK VIDEO DEMO")
    
    add_section_heading(doc, "7.1. Hướng Dẫn Cài Đặt Môi Trường & Tái Tạo Toàn Bộ Pipeline Dữ Liệu")
    add_body_paragraph(
        doc,
        "Dự án được đóng gói với khả năng tái tạo kết quả 100% (Fully Reproducible Research). Toàn bộ mã nguồn và dữ liệu có thể được chạy tự động trên mọi hệ điều hành (Windows, macOS, Linux) thông qua môi trường Python 3.10+ theo 3 bước chuẩn:"
    )

    tbl_cmds_headers = ["Bước", "Mục Đích Thao Tác", "Lệnh Dòng Lệnh Thực Thi (Command Line)"]
    tbl_cmds_data = [
        ["Bước 1", "Cài đặt các thư viện phụ thuộc", "pip install -r requirements.txt"],
        ["Bước 2", "Chạy kiểm thử tự động xác thực (pytest)", "python -m pytest -v (7/7 unit tests PASS 100%)"],
        ["Bước 3", "Thực thi toàn bộ pipeline tự động", "powershell -File scripts/run_all.ps1 (hoặc bash scripts/run_all.sh)"]
    ]
    add_academic_table(
        doc,
        "Bảng 7.1. Quy trình 3 bước thực thi tái tạo toàn bộ pipeline dữ liệu và kiểm thử tự động",
        tbl_cmds_headers,
        tbl_cmds_data,
        [1.2, 3.2, 4.4]
    )

    add_body_paragraph(
        doc,
        "Script tự động hóa sẽ tuần tự thực thi: Thu thập dữ liệu thô (01_download.py) -> Làm sạch & Điền khuyết MICE (03_clean.py) -> Phân rã 5 bảng Star Schema (04_split_tables.py) -> Xác thực toàn vẹn (07_validate.py) -> Huấn luyện mô hình dự báo (08_predictive_model.py)."
    )

    add_section_heading(doc, "7.2. Hướng Dẫn Mở & Tương Tác Với Dashboard")
    add_body_paragraph(
        doc,
        "Người dùng có thể tương tác với sản phẩm trực quan hóa thông qua 2 hình thức linh hoạt:"
    )
    add_bullet_point(
        doc,
        "Người dùng tải tệp Workbook đóng gói tại đường dẫn 'tableau/wildfire_disaster_analysis.twbx' và mở trực tiếp bằng phần mềm Tableau Desktop hoặc Tableau Reader (miễn phí). Toàn bộ 10 Worksheets, 3 Dashboards và 3 Story Points cùng toàn bộ tập dữ liệu đã được nhúng sẵn mà không yêu cầu cấu hình thêm cơ sở dữ liệu ngoại vi.",
        "Hình thức 1 - Tableau Desktop Offline: "
    )
    add_bullet_point(
        doc,
        "Truy cập trực tiếp đường link Tableau Public chính thức của nhóm hoặc mở tệp 'dashboard/index.html' trên trình duyệt web bất kỳ. Trang web tích hợp mã nhúng JavaScript API của Tableau, hỗ trợ đầy đủ các thao tác lọc chéo, rê chuột xem tooltip và chuyển đổi Story Points tương tác mượt mà.",
        "Hình thức 2 - Tableau Public & Web Dashboard: "
    )

    add_section_heading(doc, "7.3. Kịch Bản Thuyết Trình Demo Chi Tiết Từng Phút Trước Hội Đồng (5–7 Phút)")
    add_body_paragraph(
        doc,
        "Nhóm xây dựng kịch bản thuyết trình demo mẫu trong thời lượng 5–7 phút chuẩn bảo vệ đồ án tốt nghiệp, phân vai chi tiết từng phút:"
    )
    add_bullet_point(
        doc,
        "Giới thiệu bối cảnh biến đổi khí hậu California, mục tiêu nghiên cứu và công bố 4 chỉ số KPI vĩ mô trên đỉnh Dashboard D1 (7.235 vụ cháy, 19,39 triệu mẫu bị thiêu rụi, 73.818 công trình bị phá hủy, 207 sinh mạng tử vong).",
        "Phút 1 - Mở đầu & Giới thiệu KPI vĩ mô: "
    )
    add_bullet_point(
        doc,
        "Trình chiếu Dashboard D1. Chỉ rõ sự chuyển dịch mùa cháy trên Sheet 01 (01_Line_Season: tháng 4, 5 và 10 tăng vọt ~70% ở thập kỷ gần đây); phân tích cơ cấu nguyên nhân trên Sheet 02 và chỉ ra các năm cực đoan đỏ rực sau năm 2017 trên Diverging Bar Sheet 10.",
        "Phút 2 - Phân tích Mùa vụ & Xu thế 20 năm: "
    )
    add_bullet_point(
        doc,
        "Chuyển sang Dashboard D2. Trình chiếu Bản đồ địa lý 2 lớp Sheet 03 và biểu diễn tính năng Filter Action: Click vào Hạt Butte trên bản đồ, Treemap Sheet 07 lập tức hiển thị chi tiết hơn 23.000 căn nhà bị san phẳng (chủ yếu là Single Family Residence). Chứng minh quy luật Pareto 80/20 trên Sheet 09 khi chỉ 7 Hạt gánh chịu tới 82% tổng thiệt hại nhà cửa toàn bang.",
        "Phút 3–4 - Không gian địa lý & Quy luật Pareto 80/20: "
    )
    add_bullet_point(
        doc,
        "Chuyển sang Dashboard D3. Phân tích Donut Chart Sheet 04 và Heatmap Sheet 06 để giải mã nghịch lý: Sét đánh chỉ chiếm 20,9% số vụ nhưng xác suất tạo đám cháy lớn >5.000 mẫu cao gấp 4 lần con người; trong khi con người chiếm 64% vụ gây thiệt hại tài sản nặng nề nhất gần đô thị. Trình diễn đường hồi quy log-log R² = 0.356 trên Sheet 08.",
        "Phút 5 - Căn nguyên & Mô hình hồi quy dự báo: "
    )
    add_bullet_point(
        doc,
        "Chuyển sang Tableau Story 3 Story Points để tổng kết thông điệp tự sự và nêu bật 3 nhóm giải pháp chính sách (phân bổ ngân sách phòng cháy theo Pareto, tái cấu trúc lịch trực cứu hỏa từ tháng 4, kiểm soát nguồn phát hỏa nhân tạo).",
        "Phút 6–7 - Storytelling & Khuyến nghị chính sách: "
    )

    add_section_heading(doc, "7.4. Liên Kết Video Demo Chính Thức, Video Backup Tóm Tắt & Kho Lưu Trữ GitHub")
    add_body_paragraph(
        doc,
        "Toàn bộ tài nguyên số của dự án được lưu trữ công khai và minh bạch tại các liên kết sau:"
    )
    add_bullet_point(
        doc,
        "Kho lưu trữ mã nguồn mở toàn bộ dự án: https://github.com/tpdk0105/IDV_TTDL (Chứa đầy đủ mã nguồn Python, tài liệu đặc tả và kiểm thử tự động).",
        "Mã nguồn GitHub: "
    )
    add_bullet_point(
        doc,
        "Đường dẫn bảng điều khiển tương tác trực tuyến: https://public.tableau.com/app/profile/di.khang/viz/CK_17913924077470/07_Monthly_Matrix",
        "Tableau Public URL: "
    )
    add_bullet_point(
        doc,
        "Video ghi hình toàn bộ kịch bản thuyết trình demo sản phẩm chất lượng cao Full HD (thời lượng 5–7 phút).",
        "Video Demo chính thức: "
    )
    add_bullet_point(
        doc,
        "Video dự phòng khẩn cấp tóm lược toàn bộ thao tác then chốt trên 3 Dashboards đề phòng sự cố đường truyền mạng khi bảo vệ.",
        "Video Backup tóm tắt: "
    )
def build_chapter_8(doc):
    add_chapter_title(doc, "CHƯƠNG 8: KẾT LUẬN & TÀI LIỆU THAM KHẢO")
    
    add_section_heading(doc, "8.1. Tổng Kết Các Kết Quả Đạt Được & Đóng Góp Chính Của Đề Tài")
    add_body_paragraph(
        doc,
        "Sau quá trình nghiên cứu và phát triển nghiêm túc, đồ án đã hoàn thành xuất sắc và trọn vẹn toàn bộ các mục tiêu đặt ra, mang lại các đóng góp nổi bật về cả mặt khoa học dữ liệu lẫn ứng dụng thực tiễn:"
    )
    add_bullet_point(
        doc,
        "Đã khảo sát, thu thập và làm sạch thành công hơn 158.000 bản ghi thô từ 5 nguồn dữ liệu uy tín của chính phủ Hoa Kỳ và bang California. Hợp nhất thành công chuỗi thiệt hại công trình đạt đủ 20/20 năm liên tục (2006–2025), cam kết tập dữ liệu sạch đạt 7.235 vụ cháy (vượt xa chỉ tiêu ≥ 5.000 dòng).",
        "Xây dựng pipeline kỹ thuật dữ liệu tự động hóa & toàn vẹn: "
    )
    add_bullet_point(
        doc,
        "Ứng dụng thành công hai mô hình học máy độc lập: Isolation Forest & LOF giúp phát hiện chính xác các ngoại lai thảm họa trên không gian logarit để bảo toàn dữ liệu; thuật toán MICE giúp giảm hơn 38% sai số điền khuyết thiếu so với Median Baseline.",
        "Tiền xử lý thông minh bằng Học máy (Machine Learning Cleaning): "
    )
    add_bullet_point(
        doc,
        "Phân rã khoa học dữ liệu phẳng thành 5 bảng Dimension và Fact theo mô hình hình sao (Star Schema), khử triệt để dư thừa dữ liệu và hỗ trợ hoàn hảo cho việc xây dựng quan hệ Tableau Data Relationships không bị nhân bản dòng.",
        "Mô hình hóa dữ liệu Star Schema tối ưu: "
    )
    add_bullet_point(
        doc,
        "Thiết kế 10 Worksheets chuyên sâu thuộc 9 loại biểu đồ khác nhau (vượt chuẩn tối thiểu 8 loại của môn học), tích hợp vào 3 Dashboards chuyên đề chuẩn WCAG 2.1 AA và 1 Tableau Story dẫn dắt mạch lạc theo cấu trúc tự sự Narrative Arc.",
        "Hệ thống trực quan hóa tương tác đa chiều vượt chuẩn: "
    )
    add_bullet_point(
        doc,
        "Chứng minh thực nghiệm quy luật mùa cháy kéo dài; quy luật bất cân xứng Pareto 80/20 (7 Hạt chịu 82% thiệt hại công trình); và nghịch lý giữa sấm sét tự nhiên (diện tích lớn) vs hoạt động con người (tổn thất nhà cửa và thương vong áp đảo).",
        "Phát hiện những insight có giá trị tham mưu chính sách cao: "
    )
    add_bullet_point(
        doc,
        "Huấn luyện thành công mô hình Hồi quy tuyến tính dự phóng chuỗi thời gian 10 năm (2026–2035) bằng phương pháp Rolling Origin chống rò rỉ dữ liệu; mô hình Log-Log với R² = 0.356; và tích hợp trực quan hóa đường Forecast kèm dải tin cậy 95% trực tiếp lên Dashboard.",
        "Tích hợp mô hình dự báo học máy vào trực quan hóa: "
    )

    add_section_heading(doc, "8.2. Hạn Chế Tồn Tại & Định Hướng Nghiên Cứu Mở Rộng Trong Tương Lai")
    add_body_paragraph(
        doc,
        "Mặc dù đã đạt được nhiều kết quả thực nghiệm ấn tượng, đề tài vẫn tồn tại một số hạn chế khách quan bắt nguồn từ đặc thù dữ liệu thiên tai môi trường:"
    )
    add_bullet_point(
        doc,
        "Tỷ lệ vụ cháy mang nhãn 'Chưa xác định nguyên nhân' (Undetermined / Unknown) còn chiếm tỷ trọng khá lớn (~32% đến 42%), gây khó khăn nhất định cho việc quy kết trách nhiệm pháp lý tuyệt đối.",
        "Dữ liệu căn nguyên khởi phát còn khuyết thiếu: "
    )
    add_bullet_point(
        doc,
        "Số liệu thiệt hại tài sản quy đổi ra đơn vị tiền tệ USD từ NOAA NCEI có nhiều ô khuyết thiếu và mang giá trị $0 do cơ chế ước tính giá trị bảo hiểm tại Mỹ có độ trễ lớn và chỉ áp dụng cho các sự kiện thiên tai nghiêm trọng.",
        "Định giá thiệt hại tài sản USD chưa đồng bộ: "
    )
    add_body_paragraph(
        doc,
        "Trong tương lai, đề tài có thể được tiếp tục mở rộng theo các hướng nghiên cứu giàu tiềm năng:"
    )
    add_bullet_point(
        doc,
        "Tích hợp trực tiếp dữ liệu ảnh viễn thám độ phân giải cao từ vệ tinh NASA MODIS/VIIRS và Copernicus Sentinel-2 để theo dõi các điểm phát nhiệt (thermal hotspots) và mức độ suy thoái thảm thực vật (NDVI) theo thời gian thực.",
        "Tích hợp viễn thám thời gian thực (Remote Sensing): "
    )
    add_bullet_point(
        doc,
        "Kết hợp các chỉ số độ ẩm không khí, vận tốc gió theo giờ và độ ẩm nhiên liệu đất để xây dựng mô hình Học sâu (Deep Learning - LSTM / Transformer) dự báo nguy cơ bùng phát cháy rừng cấp Hạt trước 72 giờ, hỗ trợ tối đa cho lực lượng phản ứng nhanh.",
        "Mô hình cảnh báo sớm nguy cơ hỏa hoạn (Early Warning AI): "
    )

    add_section_heading(doc, "8.3. Danh Mục Tài Liệu Tham Khảo Chuẩn IEEE (Ghi Đầy Đủ Link Nguồn Crawl Dữ Liệu)")
    add_body_paragraph(
        doc,
        "Danh mục tài liệu tham khảo được trình bày theo định dạng chuẩn IEEE, cung cấp đầy đủ liên kết truy cập trực tiếp của toàn bộ các tập dữ liệu thu thập và các công trình học thuật nền tảng:"
    )

    refs = [
        "[1] CAL FIRE, 'Fire and Resource Assessment Program (FRAP) Fire Perimeters Database (1878–2025),' State of California Department of Forestry and Fire Protection, 2025. [Online]. Available: https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::california-fire-perimeters-all",
        "[2] CAL FIRE, 'Damage Inspection Program (DINS) Post-Fire Assessment Dataset (2013–2025),' California Department of Forestry and Fire Protection Open Data, 2025. [Online]. Available: https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::cal-fire-damage-inspection-dins-data",
        "[3] K. C. Short, 'Spatial wildfire occurrence data for the United States, 1992-2020 [FPA_FOD / ICS-209-PLUS],' USDA Forest Service, Research Data Archive, Fort Collins, CO, 2022. doi: 10.6084/m9.figshare.19858927. [Online]. Available: https://figshare.com/articles/dataset/19858927",
        "[4] NOAA National Centers for Environmental Information, 'Storm Events Database - California Wildfire Occurrences (2006–2025),' National Oceanic and Atmospheric Administration, 2025. [Online]. Available: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/",
        "[5] U.S. Census Bureau & California Department of Technology, 'California County Boundaries, Identifiers and 2020 Decennial Census Demographics,' State of California Geoportal, 2021. [Online]. Available: https://gis.data.ca.gov/datasets/CDB::california-county-boundaries-and-identifiers",
        "[6] F. T. Liu, K. M. Ting, and Z.-H. Zhou, 'Isolation Forest,' in Proceedings of the 2008 Eighth IEEE International Conference on Data Mining (ICDM), Pisa, Italy, 2008, pp. 413-422. doi: 10.1109/ICDM.2008.17.",
        "[7] S. van Buuren and K. Groothuis-Oudshoorn, 'mice: Multivariate Imputation by Chained Equations in R,' Journal of Statistical Software, vol. 45, no. 3, pp. 1-67, 2011. doi: 10.18637/jss.v045.i03.",
        "[8] W3C, 'Web Content Accessibility Guidelines (WCAG) 2.1 - W3C Recommendation,' World Wide Web Consortium, Jun. 2018. [Online]. Available: https://www.w3.org/TR/WCAG21/",
        "[9] M. Okabe and K. Ito, 'Color Universal Design (CUD): How to make figures and presentations that are friendly to Colorblind people,' JFly Data Repository, University of Tokyo, 2008. [Online]. Available: https://jfly.uni-koeln.de/color/",
        "[10] E. R. Tufte, 'The Visual Display of Quantitative Information,' 2nd ed. Cheshire, CT: Graphics Press, 2001.",
        "[11] T. Hastie, R. Tibshirani, and J. Friedman, 'The Elements of Statistical Learning: Data Mining, Inference, and Prediction,' 2nd ed. New York, NY: Springer, 2009.",
        "[12] S. Syphard, J. Keeley, A. Pfaff, and K. Ferschweiler, 'Human presence diminishes the importance of climate in driving fire activity across the United States,' Proceedings of the National Academy of Sciences (PNAS), vol. 114, no. 52, pp. 13750-13755, 2017."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.35)
        p_ref.paragraph_format.first_line_indent = Inches(-0.35)
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        r = p_ref.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.color.rgb = COLOR_TEXT


def main():
    print(f"Loading base document from {BACKUP_PATH}...")
    doc = docx.Document(str(BACKUP_PATH))
    body = doc._body._element

    print(f"Original body children count: {len(body)}")
    
    # Identify 'MỤC LỤC' at index 44
    muc_luc_idx = None
    for i, child in enumerate(body):
        if child.tag.endswith('p'):
            p = docx.text.paragraph.Paragraph(child, doc)
            if p.text.strip() == 'MỤC LỤC':
                muc_luc_idx = i
                break

    if muc_luc_idx is None:
        raise ValueError("Could not find 'MỤC LỤC' paragraph in document.")

    print(f"Found 'MỤC LỤC' at index {muc_luc_idx}. Removing old children from {muc_luc_idx + 1} to end-1...")
    children_to_remove = list(body)[muc_luc_idx + 1 : -1]
    for child in children_to_remove:
        body.remove(child)

    print(f"Remaining body children: {len(body)}. Now building new content...")

    print("Building Table of Contents (8 Chapters)...")
    build_table_of_contents(doc)

    print("Building Chapter 1: Giới thiệu đề tài & Mô tả tập dữ liệu...")
    build_chapter_1(doc)

    print("Building Chapter 2: Quy trình tiền xử lý & EDA...")
    build_chapter_2(doc)

    print("Building Chapter 3: Mô hình hóa và phân rã các bảng dữ liệu...")
    build_chapter_3(doc)

    print("Building Chapter 4: Thiết kế Dashboard & Đặc tả 10 biểu đồ (Dạng dòng + Khung dán ảnh)...")
    build_chapter_4(doc)

    print("Building Chapter 5: Khai phá Insight & Kể chuyện dữ liệu (Dạng dòng + Khung dán ảnh)...")
    build_chapter_5(doc)

    print("Building Chapter 6: Mô hình học máy dự báo xu thế & Trực quan hóa...")
    build_chapter_6(doc)

    print("Building Chapter 7: Hướng dẫn cài đặt/sử dụng & Link Video Demo...")
    build_chapter_7(doc)

    print("Building Chapter 8: Kết luận & Tài liệu tham khảo...")
    build_chapter_8(doc)

    try:
        print(f"Saving updated document directly to {DOC_PATH}...")
        doc.save(str(DOC_PATH))
        print("SUCCESS: Document IDV_Nhom17.docx has been completely rebuilt with all requested modifications!")
    except PermissionError:
        fallback_path = Path("IDV_Nhom17_updated.docx")
        print(f"Notice: {DOC_PATH} is currently open in WPS Office / Word.")
        print(f"Saving updated document to {fallback_path}...")
        doc.save(str(fallback_path))
        print(f"SUCCESS: Saved updated document to {fallback_path}!")


if __name__ == "__main__":
    main()
