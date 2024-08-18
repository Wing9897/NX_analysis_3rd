# NX Log to Chart Converter

## README.md
- en [English](README_en.md)

## 概述

這個程式將NX log匯出的HTML數據轉換為可視化圖表，其中的用途是可以幫助用戶分析網路問題。透過散點圖和其他圖表，您可以輕鬆識別和診斷設備故障。而且更可以把其他Log的信息製成圖表。

## 功能

- **基於source的發生次數的棒形圖分析**：顯示某來源的觸發次數。
- **基於時間的發生次數的棒形圖分析**：顯示某時間點的觸發次數。
- **觸發時間的散點圖分析**：以散點時間軸顯示log事件發生情況。
- **簡單易用的工具**：容易上手，方便操作。
- **友好的圖表顯示**：可以任意放大縮小圖表。

## 具體操作

**1 :Export network issue logs to html**
![image](picture/network2.png)
![image](picture/export_html.gif)

**2 :Generate charts**
![image](picture/generate_charts.gif)
![image](picture/charts.png)

**3 :Common reasons for network camera disconnection**
![image](picture/network.png)

**4 :Ask chatgpt a question**
![image](picture/chatgpt.png)


## 使用案例

1.我曾經在一座大樓中，當所有攝影機同時斷線時，我利用這個程式進行分析，最終確認了整座建築的電力異常，並發現某些樓層的UPS也有問題。

2.可以利用在人流統計表,利用簡單的generic event 功能，把source設定為樓層號碼，然後把整個generic event log 匯出成html再使用我的程式就可以得到人流量圖表。
![image](picture/people_count.png)

