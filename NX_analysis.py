from collections import Counter
from bs4 import BeautifulSoup
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Scatter , Line
from pyecharts.commons.utils import JsCode
from datetime import datetime , timedelta
from tqdm import tqdm
import webbrowser

date_formats = [
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%d-%m-%Y %H:%M:%S',
    '%m/%d/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M:%S',
    '%Y/%m/%d %p %I:%M:%S',
    '%d/%m/%Y %p %I:%M:%S',
    '%m/%d/%Y %p %I:%M:%S',
    '%-m/%-d/%Y %I:%M:%S %p',
    '%Y-%m-%d',
    '%d-%m-%Y',
    '%m/%d/%Y',
    '%d/%m/%Y',
    '%Y/%m/%d',
    '%Y-%m-%d %I:%M:%S %p',
    '%d/%m/%Y %I:%M:%S %p',
    '%m/%d/%Y %I:%M:%S %p',
    '%-m/%-d/%Y',
    '%B %d, %Y',
    '%b %d, %Y',
    '%Y.%m.%d',
]

replacements = {
    '上午': 'AM', 
    '下午': 'PM',
    'matin': 'AM',
    'soir': 'PM',  
    'a.m.': 'AM',
    'p.m.': 'PM', 
    'म.पू.': 'AM',
    'म.पूर्व.': 'PM',
    'AM': 'AM',
    'PM': 'PM',        
    'AM': 'AM',
    'PM': 'PM'
}

colors = [
    "#c23531", "#2f4554", "#61a0a8", "#d00000", "#91c7ae", "#749f83", "#ca8622",
    "#bda29a", "#6e7074", "#546570", "#f05b72", "#ef5b9c", "#f47920", "#905a3d",
    "#fab27b", "#2a5caa", "#444693", "#b2d235", "#6d8346", "#ac6767", "#1d953f",
    "#6950a1", "#ff4500", "#ff6347", "#ff8c00", "#ffd700", "#ff1493", "#ff69b4",
    "#00bfff", "#7fff00", "#ff00ff", "#ff7f50", "#dc143c", "#00fa9a", "#00ff7f",
    "#8a2be2", "#ff6347", "#ff4500", "#4682b4", "#ff8c00", "#adff2f", "#ff1493",
    "#32cd32", "#da70d6", "#cd5c5c", "#ffa07a", "#f0e68c", "#b22222", "#5f9ea0",
    "#ff8c00", "#9932cc", "#8b0000", "#ff4500", "#228b22", "#1e90ff", "#ff1493",
    "#ff6347", "#ff7f50", "#ff8c00", "#d2691e", "#cd5c5c", "#4169e1", "#8a2be2",
    "#5f9ea0", "#ffb6c1", "#ff69b4", "#4682b4", "#7fff00", "#ff7f50", "#d3d3d3",
    "#f4a460", "#b8860b", "#ff8c00", "#32cd32", "#ff00ff", "#800080", "#ff4500",
    "#ff6347", "#d2691e", "#ff1493", "#dc143c", "#00fa9a", "#007fff", "#ff6347",
]



def read_html_file():
    """Read HTML file content and return the soup object."""
    filelocation = input("Input your file location: ")
    try:
        with open(filelocation, 'rb') as f:
            html_content = f.read()
            print("\033[92mInitializing, please wait...\033[0m")
        return BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(f"\033[91mError reading file: {e}\033[0m")
        exit()

def standardize_datetime(date_str, formats):
    for world, en in replacements.items():
        date_str = date_str.replace(world, en)
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None  # Return None if no format matches        

def process_ip_data(soup):
    ip_data = []
    try:
        rows = soup.find_all('tr')[1:]
        for row in tqdm(rows, desc="Processing IP data",colour = 'yellow'):
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            ip_data.append(row_data[2])  # 3rd <td> is Source name

        ip_counts = Counter(ip_data)
        floor_counts = {floor: count for floor, count in ip_counts.items()}

        # Create first bar chart for IP addresses
        bar_ip = Bar(init_opts=opts.InitOpts(page_title="Combined"))
        x_axis_ip = list(floor_counts.keys())
        bar_ip.add_xaxis(x_axis_ip)
        bar_ip.add_yaxis("The number of occurrences:", list(floor_counts.values()))
        bar_ip.set_global_opts(
            title_opts=opts.TitleOpts(title="Number of event triggers per source"),
            xaxis_opts=opts.AxisOpts(name="Location/Devices", type_="category", axislabel_opts=opts.LabelOpts(rotate=-30)),
            yaxis_opts=opts.AxisOpts(name="Count"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=[
                opts.DataZoomOpts(type_="slider", xaxis_index=0, range_start=0, range_end=100),
                opts.DataZoomOpts(type_="slider", yaxis_index=0, orient="vertical", range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", xaxis_index=0)
            ],
        )
        
        # Print number of occurrences for IP addresses
        #print("\n\nFrequency of event:\n")
        #for floor, count in sorted(floor_counts.items(), key=lambda x: x[1], reverse=True):
        #    print(f"{floor}:\t{count} count")
        return bar_ip
    except Exception as e:
        print(f"\033[91mError processing IP data: {e}\033[0m")


def group_time_ranges(time_list, range_minutes):
    """按指定的分鐘數進行時間範圍分組"""
    grouped_counts = Counter()
    for time in time_list:
        rounded_time = time - timedelta(minutes=time.minute % range_minutes,
                                        seconds=time.second,
                                        microseconds=time.microsecond)
        grouped_counts[rounded_time] += 1
    return grouped_counts

def process_time_data(soup):
    formats = ['%Y/%m/%d %p %I:%M:%S']

    try:
        rows = soup.find_all('tr')[1:]
        time_data = [row.find_all('td')[0].text.strip() for row in tqdm(rows, desc="Processing time data", colour='red')]

        standardized_times = [t for t in (standardize_datetime(t, formats) for t in time_data) if t]

        range_minutes = 60  
        time_counts = group_time_ranges(standardized_times, range_minutes)

        line_time = Line()
        x_axis_time = sorted(time_counts.keys())
        line_time.add_xaxis([t.strftime('%Y/%m/%d %H:%M:%S') for t in x_axis_time])
        line_time.add_yaxis("The number of occurrences:", [time_counts[t] for t in x_axis_time], is_smooth=True)

        line_time.set_global_opts(
            title_opts=opts.TitleOpts(title="Number of event triggers per hour"),
            xaxis_opts=opts.AxisOpts(
                name="Time",
                type_="category",
                axislabel_opts=opts.LabelOpts(rotate=-30)
            ),
            yaxis_opts=opts.AxisOpts(name="Count"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[
                opts.DataZoomOpts(type_="slider", xaxis_index=0, range_start=0, range_end=100),
                opts.DataZoomOpts(type_="slider", yaxis_index=0, orient="vertical", range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", xaxis_index=0)
            ],
            legend_opts=opts.LegendOpts(is_show=True)
        )

        return line_time

    except Exception as e:
        print(f"\033[91mError processing time data: {e}\033[0m")


def process_scatter_plot(soup):
    # Program 3: Scatter plot for EventLog/Time
    data = []
    dates = []

    try:
        rows = soup.find_all('tr')[1:]
        for row in tqdm(rows, desc="Processing scatter plot data",colour = 'blue'):
            cells = row.find_all('td')
            date_time = cells[0].text.strip()
            source = cells[2].text.strip()
            data.append([date_time, source])
        
        #check data format
        first_date_time = data[0][0] if data else None
        if not first_date_time or not standardize_datetime(first_date_time, date_formats):
            print("\033[91mError: The date format is incorrect.\033[0m")
            exit()  
            

        # Parse dates [0]=data ,[1]=name
        for row in data:
            standardized_date = standardize_datetime(row[0],date_formats)
            dates.append(standardized_date if standardized_date else None)

        # Extract sources and unique sources
        sources = [row[1] for row in data]#name array
        sort_sources = sorted(list(set(sources)))#sort
        source_index = {source: i for i, source in enumerate(sort_sources)}#allocate index
        source_color_map = {source: colors[i % len(colors)] for i, source in enumerate(sort_sources)}#key array

        # Create scatter plot
        scatter = Scatter()

        for source in sort_sources:
            source_dates = [d for d, s in zip(dates, sources) if s == source and d is not None]
            x_data = [d.timestamp() * 1000 for d in source_dates]
            y_data = [source_index[source]] * len(source_dates)

            scatter.add_xaxis(x_data)
            scatter.add_yaxis(
                series_name=source,
                y_axis=y_data,
                symbol_size=10,
                label_opts=opts.LabelOpts(is_show=True),
                itemstyle_opts=opts.ItemStyleOpts(color=source_color_map[source])
            )

        scatter.set_global_opts(
            title_opts=opts.TitleOpts(title="EventLog/Time Scatter"),
            xaxis_opts=opts.AxisOpts(
                type_="time",
                name="Date/Time",
                axislabel_opts=opts.LabelOpts(formatter=JsCode(
                    """
                    function (value) {
                        var date = new Date(value);
                        return date.getFullYear() + '/' +
                               (date.getMonth() + 1).toString().padStart(2, '0') + '/' +
                               date.getDate().toString().padStart(2, '0') + ' ' +
                               date.getHours().toString().padStart(2, '0') + ':' +
                               date.getMinutes().toString().padStart(2, '0') + ':' +
                               date.getSeconds().toString().padStart(2, '0');
                    }
                    """
                )),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="category",
                name="Source number",
                axispointer_opts=opts.AxisPointerOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                formatter=JsCode(
                    """
                    function(params) {
                        var date = new Date(params[0].value[0]);
                        return date.getFullYear() + '/' +
                               (date.getMonth() + 1).toString().padStart(2, '0') + '/' +
                               date.getDate().toString().padStart(2, '0') + ' ' +
                               date.getHours().toString().padStart(2, '0') + ':' +
                               date.getMinutes().toString().padStart(2, '0') + ':' +
                               date.getSeconds().toString().padStart(2, '0') +
                               '<br />' + params[0].seriesName;
                    }
                    """
                )
            ),
            datazoom_opts=[
                opts.DataZoomOpts(type_="slider", xaxis_index=0, pos_bottom="10%", range_start=0, range_end=100),
                opts.DataZoomOpts(type_="slider", yaxis_index=0, orient="vertical", range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", xaxis_index=0)                
            ],
            legend_opts=opts.LegendOpts(
                type_="scroll",
                pos_bottom="0%",
                item_width=20,
                item_height=14,
                textstyle_opts=opts.TextStyleOpts(font_size=12),
            ),
        )
        return scatter
    except Exception as e:
        print(f"\033[91mError processing scatter plot data: {e}\033[0m")

def main():
    # Read and parse HTML
    soup = read_html_file()

    # Generate charts
    scatter = process_scatter_plot(soup)
    bar_ip = process_ip_data(soup)
    bar_time = process_time_data(soup)

    # Create a Page with draggable layout
    try:
        page = Page(layout=Page.DraggablePageLayout)
        page.add(bar_time, bar_ip,scatter)
        page.render("Combined_NXlog_barchart_and_scatter.html", page_title="EventLog/Time Scatter")
        webbrowser.open("Combined_NXlog_barchart_and_scatter.html")
        input("\033[92mFinish! Press 'Enter' to close...\033[0m")
    except Exception as e:
        print(f"\033[91mError rendering charts: {e}\033[0m")

if __name__ == "__main__":
    main()