# NX Log to Chart Converter

## 概述

這個程式將NX log匯出的HTML數據轉換為可視化圖表，旨在幫助用戶分析網路問題。透過散點圖和其他圖表，您可以輕鬆識別和診斷設備故障。

## 功能

- **散點圖分析**：識別長時間出現的問題點。
- **斷線事件統計**：顯示不同時間點的斷線次數。
- **簡單易用的UI**：直觀的使用者介面，方便操作。

## 使用案例

在一個宿舍中，當所有攝影機同時斷線時，我們利用這個程式進行分析，最終確認了整座建築的電力異常，並發現某些樓層的UPS也有問題。

![示例圖表][]## 安裝1. 從GitHub下載程式碼。2. 確保您的系統上已安裝必要的依賴項。3. 使用以下命令運行程式：   ```bash   python nx_log_to_chart.py   ```## 使用方法1. 匯出NX log為HTML格式。2. 將HTML文件作為輸入，運行程式。3. 生成的圖表將保存在指定的輸出目錄。![操作步驟][]## 貢獻歡迎任何形式的貢獻！請提出問題、發送拉取請求，或分享您的想法。## 未來展望隨著NX 6.0的推出，預計將有更多AI功能。我們希望能夠進一步擴展圖表功能，以支持Premium License用戶。## 聯繫如有問題或建議，請聯繫 [your-email@example.com](mailto:your-email@example.com)。---感謝您使用NX Log to Chart Converter！希望這個工具能幫助您更有效地進行故障排除。
