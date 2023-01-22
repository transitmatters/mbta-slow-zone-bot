from datetime import datetime, timedelta
import json
import operator
from itertools import groupby
import logging

line_emoji_map = {"Red": "🔴", "Green": "🟢", "Blue": "🔵", "Orange": "🟠"}


with open("stations.json", "r") as myfile:
    data = myfile.read()

stations = json.loads(data)


def id_to_stop(line, id):
    for s in stations[line]["stations"]:
        if str(id) in s["stops"]["0"] or str(id) in s["stops"]["1"]:
            return s["stop_name"]


def get_stop_pair(slow_zone):
    return id_to_stop(slow_zone["color"], slow_zone["fr_id"]) + " → " + id_to_stop(slow_zone["color"], slow_zone["to_id"])


def get_zone_date_length(sz):
    d1 = datetime.strptime(sz["start"], "%Y-%m-%dT%H:%M:%SZ")
    d2 = datetime.strptime(sz["end"], "%Y-%m-%dT%H:%M:%SZ")
    return abs((d2 - d1).days)


def format_line_slow_zone(slow_zone):
    ret = ""
    ret += get_stop_pair(slow_zone) + "\n"
    ret += "⏳ " + str(get_zone_date_length(slow_zone)) + " days "
    ret += "📈  " + str(round(slow_zone["delay"], 1)) + "s "
    ret += (
        "⬆️  " + str(round(slow_zone["delay"] / slow_zone["baseline"] * 100, 2)) + "%"
    )
    return ret


def format_time(t):
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")


def chunks(lines, n):
    for i in range(0, len(lines), n):
        yield lines[i: i + n]


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
        output_map[i] += line_emoji_map[line[0]["color"]] + " " + line[0]["color"] + " " + "Line\n---------------------\n"
        for slow_zone in line:
            output_map[i] += format_line_slow_zone(slow_zone) + "\n\n"
        output_map[i] += "\n\n"

    # Filter out empty strings
    return filter(None, output_map)


def format_new_slow_zone(z):
    output = ""
    output += "⚠️ New Slow Zone ⚠️\n"
    output += "---------------------\n"
    output += format_line_slow_zone(z)
    return output


def format_fixed_slow_zone(z):
    output = ""
    output += "✅ Fixed Slow Zone 🎉\n"
    output += "---------------------\n"
    output += format_line_slow_zone(z)
    return output
