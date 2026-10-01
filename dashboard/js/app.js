/**
 * Module: dashboard/js/app.js
 * Người phụ trách: Thành viên 3 (Kỹ sư Dashboard & Trực quan hóa)
 * Mục đích: Quản trị trạng thái toàn cục (State Management), lắng nghe bộ lọc,
 * điều phối Cross-filtering và kích hoạt vẽ lại 12 biểu đồ.
 */

(function () {
  "use strict";

  // 1. Trạng thái bộ lọc toàn cục (Global Filter State)
  const state = {
    yearMin: 2006,
    yearMax: 2025,
    disasterType: "ALL",
    continent: "ALL",
    rawOnly: false,
    theme: "light",
  };

  // 2. Danh bạ lưu các phiên bản biểu đồ ECharts (Charts Registry)
  const chartsRegistry = {};

  // 3. Khởi tạo ứng dụng khi DOM tải xong
  window.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    initFilters();
    initWindowResize();
    console.log("[IDV Dashboard] Ứng dụng khởi tạo thành công ở Giai đoạn 1.");
  });

  // Chuyển đổi giao diện Sáng / Tối
  function initThemeToggle() {
    const btn = document.getElementById("btn-theme-toggle");
    if (!btn) return;

    btn.addEventListener("click", () => {
      state.theme = state.theme === "light" ? "dark" : "light";
      document.body.className = `theme-${state.theme}`;

      // Resize và cập nhật theme cho các biểu đồ ECharts đã nạp
      Object.values(chartsRegistry).forEach((chartInstance) => {
        if (chartInstance && typeof chartInstance.resize === "function") {
          chartInstance.resize();
        }
      });
    });
  }

  // Khởi tạo các sự kiện bộ lọc
  function initFilters() {
    const yearMinInput = document.getElementById("filter-year-min");
    const yearMaxInput = document.getElementById("filter-year-max");
    const yearDisplay = document.getElementById("year-range-display");
    const typeSelect = document.getElementById("filter-disaster-type");
    const continentSelect = document.getElementById("filter-continent");
    const toggleRaw = document.getElementById("toggle-raw-only");
    const btnReset = document.getElementById("btn-reset-filters");

    // Lắng nghe thanh trượt năm
    const updateYearRange = () => {
      let min = parseInt(yearMinInput.value, 10);
      let max = parseInt(yearMaxInput.value, 10);
      if (min > max) {
        [min, max] = [max, min];
        yearMinInput.value = min;
        yearMaxInput.value = max;
      }
      state.yearMin = min;
      state.yearMax = max;
      if (yearDisplay) yearDisplay.textContent = `${min} - ${max}`;
      notifyFilterChange();
    };

    if (yearMinInput) yearMinInput.addEventListener("input", updateYearRange);
    if (yearMaxInput) yearMaxInput.addEventListener("input", updateYearRange);

    // Lắng nghe loại thảm họa
    if (typeSelect) {
      typeSelect.addEventListener("change", (e) => {
        state.disasterType = e.target.value;
        notifyFilterChange();
      });
    }

    // Lắng nghe chọn châu lục
    if (continentSelect) {
      continentSelect.addEventListener("change", (e) => {
        state.continent = e.target.value;
        notifyFilterChange();
      });
    }

    // Lắng nghe công tắc dữ liệu gốc ML
    if (toggleRaw) {
      toggleRaw.addEventListener("change", (e) => {
        state.rawOnly = e.target.checked;
        notifyFilterChange();
      });
    }

    // Nút Reset bộ lọc
    if (btnReset) {
      btnReset.addEventListener("click", () => {
        if (yearMinInput) yearMinInput.value = 2006;
        if (yearMaxInput) yearMaxInput.value = 2025;
        if (yearDisplay) yearDisplay.textContent = "2006 - 2025";
        if (typeSelect) typeSelect.value = "ALL";
        if (continentSelect) continentSelect.value = "ALL";
        if (toggleRaw) toggleRaw.checked = false;

        state.yearMin = 2006;
        state.yearMax = 2025;
        state.disasterType = "ALL";
        state.continent = "ALL";
        state.rawOnly = false;

        notifyFilterChange();
      });
    }
  }

  // Thông báo tới tất cả các biểu đồ khi bộ lọc thay đổi
  function notifyFilterChange() {
    console.log("[Filter State Changed]:", state);
    window.dispatchEvent(
      new CustomEvent("dashboard:filterChange", { detail: state })
    );
  }

  // Tự động resize toàn bộ biểu đồ khi co giãn cửa sổ
  function initWindowResize() {
    window.addEventListener("resize", () => {
      Object.values(chartsRegistry).forEach((chartInstance) => {
        if (chartInstance && typeof chartInstance.resize === "function") {
          chartInstance.resize();
        }
      });
    });
  }

  // Xuất API toàn cục để các mô-đun biểu đồ đăng ký (Chart Registry API)
  window.DashboardApp = {
    getState: () => ({ ...state }),
    registerChart: (chartId, instance) => {
      chartsRegistry[chartId] = instance;
    },
    getChart: (chartId) => chartsRegistry[chartId],
    updateKPIs: (data) => {
      if (!data) return;
      if (document.getElementById("kpi-total-events"))
        document.getElementById("kpi-total-events").textContent =
          data.totalEvents || "--";
      if (document.getElementById("kpi-total-damage"))
        document.getElementById("kpi-total-damage").textContent =
          data.totalDamage || "--";
      if (document.getElementById("kpi-total-burned-area"))
        document.getElementById("kpi-total-burned-area").textContent =
          data.totalBurnedArea || "--";
      if (document.getElementById("kpi-total-deaths"))
        document.getElementById("kpi-total-deaths").textContent =
          data.totalDeaths || "--";
    },
  };
})();
