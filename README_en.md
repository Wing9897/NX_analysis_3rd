# NX Log to Chart Converter

## README.md
- zh_TW [繁体中文](README.md)

## Overview

This program converts HTML data exported from NX logs into visual charts, helping users analyze network issues. Through scatter plots and other charts, you can easily identify and diagnose equipment failures, and also visualize information from other logs.

## Features

- **Bar chart analysis based on source occurrence**: Displays the trigger count from a specific source.
- **Bar chart analysis based on time occurrence**: Shows the trigger count at specific time points.
- **Scatter plot analysis of trigger times**: Visualizes log event occurrences on a timeline.
- **User-friendly tool**: Easy to use and navigate.
- **Friendly chart display**: Allows for zooming in and out of charts.

## Instructions

**1: Export network issue logs to HTML**  
![image](picture/network2.png)  
![image](picture/export_html.gif)

**2: Generate charts**  
![image](picture/generate_charts.gif)  
![image](picture/charts.png)

**3: Common reasons for network camera disconnection**  
![image](picture/network.png)
If a network device shows abnormal status in the scatter plot for a long period of time, it may mean that the device has a problem, such as insufficient PoE power supply, abnormal network connection, or wiring error, etc. If multiple devices are disconnected at the same time, it may be a problem at the switch end. If more than one device is offline at the same time, there may be a problem at the switch end. In addition to a scatter plot for troubleshooting, you can use a bar graph of the number of device outages and a line graph of the number of outages per hour.

**4: Ask ChatGPT a question**  
![image](picture/chatgpt.png)

## Use Cases

1. In a building where all cameras lost connection simultaneously, I used this program for analysis and ultimately identified electrical issues throughout the building, discovering problems with the UPS on certain floors.

2. You can use it for foot traffic statistics by setting the source as the floor number in a simple generic event. Export the entire generic event log as HTML, then use my program to generate foot traffic charts.  
![image](picture/people_count.png)
