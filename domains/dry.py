from utils import format_fixed_slow_zone, format_new_slow_zone, format_updated_slow_zone
import logging
import sys


def send_new_slow_zone_dry(sz):
    for line in sz:
        logging.debug(f"line {line} in slow zone {sz}")
        for z in line:
            logging.debug(f"z {z} in line {line}")
            try:
                output = format_new_slow_zone(z)
                logging.info("\n" + output)
            except Exception as e:
                logging.error(f"Error formatting output for new slow zone {z}: {e}")
                sys.exit(1)


def send_fixed_slow_zone_dry(sz):
    for line in sz:
        logging.debug(f"line {line} in slow zone {sz}")
        for z in line:
            logging.debug(f"z {z} in line {line}")
            try:
                output = format_fixed_slow_zone(z)
                logging.info("\n" + output)
            except Exception as e:
                logging.error(f"Error formatting output for fixed slow zone {z}: {e}")
                sys.exit(1)


def send_updated_slow_zone_dry(sz):
    for line in sz:
        logging.debug(f"line {line} in slow zone {sz}")
        for z in line:
            logging.debug(f"z {z} in line {line}")
            try:
                output = format_updated_slow_zone(z)
                logging.info("\n" + output)
            except Exception as e:
                logging.error(f"Error formatting output for updated slow zone {z}: {e}")
                sys.exit(1)
