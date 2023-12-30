from datetime import datetime
import pytz

def convert_unixtime(unixtime):
    unixtime = int(unixtime)
    utc_datetime = datetime.utcfromtimestamp(unixtime)
    utc_timezone = pytz.timezone('UTC')
    utc_datetime = utc_timezone.localize(utc_datetime)
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    return utc_datetime.astimezone(vn_timezone).strftime("%d/%m/%Y %H:%M")