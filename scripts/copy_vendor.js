/**
 * Script copy thư viện ECharts từ node_modules vào dashboard/js/vendor/
 * Phục vụ chạy offline và độc lập không cần phụ thuộc CDN
 */
const fs = require('fs');
const path = require('path');

const src = path.join(__dirname, '..', 'node_modules', 'echarts', 'dist', 'echarts.min.js');
const destDir = path.join(__dirname, '..', 'dashboard', 'js', 'vendor');
const dest = path.join(destDir, 'echarts.min.js');

if (!fs.existsSync(destDir)) {
  fs.mkdirSync(destDir, { recursive: true });
}

if (fs.existsSync(src)) {
  fs.copyFileSync(src, dest);
  console.log('Successfully copied echarts.min.js to dashboard/js/vendor/');
} else {
  console.log('node_modules/echarts not found. Run "npm install" first.');
}
