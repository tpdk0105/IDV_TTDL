/**
 * Module: dashboard/js/palette.js
 * Người phụ trách: Thành viên 3 (Kỹ sư Dashboard & Trực quan hóa)
 * Mục đích: Xuất các bảng màu chuẩn hóa (Okabe-Ito, OrRd, RdBu) dùng chung cho toàn bộ 12 biểu đồ.
 * Tuân thủ nghiêm ngặt docs/COLOR_GUIDE.md và chuẩn khả năng tiếp cận WCAG 2.1 AA.
 */

const PALETTE = {
  // 1. Bảng màu phân loại cố định theo loại thảm họa (Disaster Types)
  disasters: {
    Wildfire: "#D55E00", // Đỏ cam cháy (Trọng tâm)
    Flood: "#0072B2", // Xanh dương đậm
    Storm: "#56B4E9", // Xanh da trời
    Drought: "#E69F00", // Vàng cam đất
    Earthquake: "#CC79A7", // Hồng tím sẫm
    Volcano: "#F0E442", // Vàng chanh
    ExtremeTemperature: "#882255", // Đỏ rượu
    Other: "#7F7F7F", // Xám trung tính
  },

  // 2. Bảng màu phân loại cố định theo châu lục (Continents)
  continents: {
    Americas: "#E69F00",
    Asia: "#56B4E9",
    Europe: "#009E73",
    Africa: "#F0E442",
    Oceania: "#0072B2",
    Other: "#999999",
  },

  // 3. Bảng màu phân loại cố định theo nhóm nguyên nhân cháy (Causes)
  causes: {
    Natural: "#56B4E9", // Tự nhiên (Sét)
    Human: "#D55E00", // Con người
    Unknown: "#999999", // Không rõ
  },

  // 4. Bảng màu tuần tự (Sequential Palettes)
  sequential: {
    // OrRd (Dùng cho Cháy rừng, Thiệt hại, Mật độ)
    orRd: [
      "#FFF5EB",
      "#FEE6CE",
      "#FDD0A2",
      "#FDAE6B",
      "#FD8D3C",
      "#F16913",
      "#D94801",
      "#8C2D04",
    ],
    // YlOrRd (Dùng cho Heatmap nhiệt độ/mùa cháy)
    ylOrRd: [
      "#FFFFCC",
      "#FFEDA0",
      "#FED976",
      "#FEB24C",
      "#FD8D3C",
      "#FC4E2A",
      "#E31A1C",
      "#BD0026",
      "#800026",
    ],
    // Blues (Dùng cho Thảm họa chung, Lũ lụt)
    blues: [
      "#EFF3FF",
      "#C6DBEF",
      "#9ECAE1",
      "#6BAED6",
      "#4292C6",
      "#2171B5",
      "#084594",
    ],
  },

  // 5. Bảng màu phân kỳ (Diverging Palettes - RdBu, tâm tại mốc 0)
  diverging: {
    rdBu: {
      negExtreme: "#2166AC",
      negModerate: "#4393C3",
      negMild: "#92C5DE",
      neutral: "#F7F7F7",
      posMild: "#F4A582",
      posModerate: "#D6604D",
      posExtreme: "#B2182B",
    },
  },

  // 6. Cấu hình màu sắc giao diện Light / Dark
  theme: {
    light: {
      background: "#ffffff",
      textPrimary: "#0f172a",
      textSecondary: "#475569",
      gridLine: "#f1f5f9",
      tooltipBg: "rgba(255, 255, 255, 0.95)",
    },
    dark: {
      background: "#1e293b",
      textPrimary: "#f8fafc",
      textSecondary: "#cbd5e1",
      gridLine: "#334155",
      tooltipBg: "rgba(30, 41, 59, 0.95)",
    },
  },
};

// Đăng ký toàn cục cho trình duyệt
if (typeof window !== "undefined") {
  window.PALETTE = PALETTE;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PALETTE;
}
