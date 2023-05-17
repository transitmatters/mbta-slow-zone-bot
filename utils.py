from datetime import datetime, timedelta
import json
import operator
from itertools import groupby
import logging

line_emoji_map = {"Red": "🔴", "Green": "🟢", "Blue": "🔵", "Orange": "🟠"}

with open("stations.json", "r") as data_file:
    stations = json.load(data_file)


def id_to_stop(line, id):
    ''' takes in a line and id
        returns the name of the stop the id is present in, if it exists
    '''
    for s in stations[line]["stations"]:
        if str(id) in s["stops"]["0"] or str(id) in s["stops"]["1"]:
            return s["stop_name"]


def get_stop_pair(sz):
    ''' takes in a slow zone
        returns a formatted string with the line color emoji and two stop names
    '''
    return (
        line_emoji_map[sz["color"]]
        + " "
        + id_to_stop(sz["color"], sz["fr_id"])
        + " → "
        + id_to_stop(sz["color"], sz["to_id"])
    )


def get_zone_date_length(sz):
    ''' takes in a slow zone
        returns the number of days the slow zone was active
    '''
    d1 = datetime.strptime(sz["start"], "%Y-%m-%dT%H:%M:%SZ")
    d2 = datetime.strptime(sz["end"], "%Y-%m-%dT%H:%M:%SZ")
    return abs((d2 - d1).days) + 1


def format_line_slow_zone(sz):
    ret = ""
    ret += get_stop_pair(sz) + "\n"
    ret += "🗓️ " + str(get_zone_date_length(sz)) + " days "
    ret += "⏳ " + str(round(sz["delay"], 1)) + "s "
    ret += "⬆️ " + str(round(sz["delay"] / sz["baseline"] * 100, 2)) + "%\n"
    return ret


def format_new_line_slow_zone(sz):
    ret = ""
    ret += get_stop_pair(sz) + "\n"
    ret += "⏳ " + str(round(sz["delay"], 1)) + "s "
    ret += "⬆️ " + str(round(sz["delay"] / sz["baseline"] * 100, 2)) + "%\n"
    return ret


def format_time(t):
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S")


def chunks(lines, n):
    for i in range(0, len(lines), n):
        yield lines[i : i + n]


def generate_new_slow_zones_list(sz, date):
    today_slow_zones = filter(
        lambda s: format_time(s["start"]).ctime() == (date - timedelta(days=1)).ctime(),
        sz,
    )
    sorted_slow_zones = sorted(today_slow_zones, key=operator.itemgetter("color"))
    logging.debug(f"sorted_slow_zones: {sorted_slow_zones}")
    outputList = []
    for i, g in groupby(sorted_slow_zones, key=operator.itemgetter("color")):
        outputList.append(list(g))
    return outputList


def generate_grouped_slow_zone_list(sz, date):
    today_slow_zones = filter(
        lambda s: format_time(s["end"]).ctime() == (date - timedelta(days=1)).ctime(),
        sz,
    )
    sorted_slow_zones = sorted(today_slow_zones, key=operator.itemgetter("color"))
    logging.debug(f"sorted_slow_zones: {sorted_slow_zones}")
    outputList = []
    for i, g in groupby(sorted_slow_zones, key=operator.itemgetter("color")):
        outputList.append(list(g))
    return outputList


def generate_post_text_map(g_sz):
    output_map = []
    for i, line in enumerate(g_sz):
        output_map.append("")
        output_map[i] += (
            line_emoji_map[line[0]["color"]] + " " + line[0]["color"] + " " + "Line\n---------------------\n"
        )
        for slow_zone in line:
            output_map[i] += format_line_slow_zone(slow_zone) + "\n\n"
        output_map[i] += "\n\n"

    # Filter out empty strings
    return filter(None, output_map)


def generate_data_dashboard_link(sz):
    ''' takes in a slow zone
        returns a data dashboard link to said slow zone
    '''
    color = sz['color']
    stop1 = sz['fr_id']
    stop2 = sz['to_id']
    start = (datetime.strptime(sz['start'], '%Y-%m-%dT%H:%M:%SZ') - timedelta(days=14)).strftime('%Y-%m-%d')
    end = sz['end'].split('T')[0]
    link = f"https://dashboard.transitmatters.org/rapidtransit?config={color},{stop1},{stop2},{start},{end}"
    logging.debug(f"Generated Data Dashboard link: {link}")
    return link


def format_new_slow_zone(sz):
    output = ""
    output += "⚠️ New Slow Zone ⚠️\n"
    output += "---------------------\n"
    output += format_new_line_slow_zone(sz)
    output += f"Check it out in our Data Dashboard: {generate_data_dashboard_link(sz)}"
    return output


def format_fixed_slow_zone(sz):
    output = ""
    output += "✅ Fixed Slow Zone 🎉\n"
    output += "---------------------\n"
    output += format_line_slow_zone(sz)
    output += f"Check it out in our Data Dashboard: {generate_data_dashboard_link(sz)}"
    return output
