/**
 * Biểu đồ #4: Heatmap Tháng × Năm: Số vụ cháy rừng (Chu kỳ mùa cháy)
 * Người phụ trách: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)
 * Dạng đồ thị: Heatmap (Sequential YlOrRd Palette)
 * Trạng thái: Khung mã nguồn (Giai đoạn 1) - Triển khai chi tiết trong Giai đoạn 4
 */

(function () {
  "use strict";

  const chartDom = document.getElementById("chart-04");
  if (!chartDom) return;

  function initChart() {
    console.log("[Chart-04 | TV1] Khởi tạo ma trận nhiệt Heatmap mùa cháy rừng...");
    // TODO (Giai đoạn 4): Nạp dashboard/data/chart_04_data.json và khởi tạo ECharts
  }

  window.addEventListener("dashboard:filterChange", (e) => {
    // TODO (Giai đoạn 4): Lọc lại dữ liệu và cập nhật ECharts
  });

  window.addEventListener("DOMContentLoaded", initChart);
})();
