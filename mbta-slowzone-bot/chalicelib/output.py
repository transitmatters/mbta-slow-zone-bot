from datetime import datetime, timedelta, date
import json
import operator
from itertools import groupby
import logging

line_emoji_map = {"Red": "🔴", "Green": "🟢", "Blue": "🔵", "Orange": "🟠"}

with open("stations.json", "r") as data_file:
    stations = json.load(data_file)


def id_to_stop(line, id):
    """takes in a line and id
    returns the name of the stop the id is present in, if it exists
    """
    for s in stations[line]["stations"]:
        if str(id) in s["stops"]["0"] or str(id) in s["stops"]["1"]:
            return s["stop_name"]


def get_stop_pair(sz):
    """takes in a slow zone
    returns a formatted string with the line color emoji and two stop names
    """
    return (
        line_emoji_map[sz["color"]]
        + " "
        + id_to_stop(sz["color"], sz["fr_id"])
        + " → "
        + id_to_stop(sz["color"], sz["to_id"])
    )


def get_zone_date_length(sz):
    """takes in a slow zone
    returns the number of days the slow zone was active
    """
    d1 = datetime.strptime(sz["start"], "%Y-%m-%dT%H:%M:%S")
    d2 = datetime.strptime(sz["end"], "%Y-%m-%dT%H:%M:%S")
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


def format_percent_change(latest, previous):
    ret = ""
    percent_change = (latest - previous) / previous * 100.0
    ret += "⬆️ " if percent_change < 0 else "⬇️ "
    ret += str(abs(round(percent_change, 2))) + " %\n"
    return ret


def format_updated_slow_zone_details(sz):
    ret = ""
    ret += get_stop_pair(sz) + "\n"
    ret += "⏳ " + str(round(sz["latest_delay"], 1)) + "s "
    ret += "-> " + str(round(sz["previous_delay"], 1)) + "s "
    ret += format_percent_change(sz["latest_delay"], sz["previous_delay"])
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


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float("inf")


def generate_updated_slow_zones(sz, date):
    today_slow_zones = filter(
        lambda s: format_time(s["end"]).ctime() == (date - timedelta(days=1)).ctime(),
        sz,
    )
    sorted_slow_zones = sorted(today_slow_zones, key=operator.itemgetter("color"))

    significant_changed_slow_zones = filter(
        # Check for NaN in case of shuttling
        lambda s: s["latest_delay"] is not None and s["previous_delay"] is not None
        # Check for a >= 10% change
        and get_change(s["latest_delay"], s["previous_delay"]) >= 10
        # Check for 10 second minumum change
        and abs(s["latest_delay"] - s["previous_delay"]) >= 10,
        sorted_slow_zones,
    )

    return list(significant_changed_slow_zones)


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
    """takes in a slow zone
    returns a data dashboard link to said slow zone
    """
    color = sz["color"].lower()
    stop1 = sz["fr_id"]
    stop2 = sz["to_id"]
    start = (datetime.strptime(sz["start"], "%Y-%m-%dT%H:%M:%S") - timedelta(days=14)).strftime("%Y-%m-%d")
    end = date.today().strftime("%Y-%m-%d")
    link = f"https://dashboard.transitmatters.org/{color}/trips/multi/?from={stop1}&to={stop2}&startDate={start}&endDate={end}"
    logging.debug(f"Generated Data Dashboard link: {link}")
    return link


def format_new_slow_zone(sz):
    output = ""
    output += "⚠️ New Slow Zone ⚠️\n"
    output += "---------------------\n"
    output += format_new_line_slow_zone(sz) + "\n"
    output += f"Check it out in our Data Dashboard: {generate_data_dashboard_link(sz)}"
    return output


def format_fixed_slow_zone(sz):
    output = ""
    output += "✅ Fixed Slow Zone 🎉\n"
    output += "---------------------\n"
    output += format_line_slow_zone(sz) + "\n"
    output += f"Check it out in our Data Dashboard: {generate_data_dashboard_link(sz)}"
    return output


def format_updated_slow_zone(sz):
    output = ""
    output += "🚨 Updated Slow Zone \n"
    output += "---------------------\n"
    output += format_updated_slow_zone_details(sz) + "\n"
    output += f"Check it out in our Data Dashboard: {generate_data_dashboard_link(sz)}"
    return output
