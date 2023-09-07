from utils import format_fixed_slow_zone, format_new_slow_zone, format_updated_slow_zone
import logging

def send_new_slow_zone_dry(sz):
    for line in sz:
        for z in line:
            output = format_new_slow_zone(z)
            logging.info('\n' + output)

def send_fixed_slow_zone_dry(sz):
    for line in sz:
        for z in line:
            output = format_fixed_slow_zone(z)
            logging.info('\n' + output)

def send_updated_slow_zone_dry(sz):
    for line in sz:
        for z in line:
            output = format_updated_slow_zone(z)
            logging.info('\n' + output)
