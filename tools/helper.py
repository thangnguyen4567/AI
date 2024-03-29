from datetime import datetime
import pytz
import logging
import os

def convert_unixtime(unixtime):
    unixtime = int(unixtime)
    utc_datetime = datetime.utcfromtimestamp(unixtime)
    utc_timezone = pytz.timezone('UTC')
    utc_datetime = utc_timezone.localize(utc_datetime)
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    return utc_datetime.astimezone(vn_timezone).strftime("%d/%m/%Y %H:%M")

def logging_data(info):
    log_file_path = os.path.join('logs', 'get_table.log')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s \n %(message)s')
    string_log = ''
    for value in info:
        string_log +=value + '\n'
    logging.info(string_log)
        