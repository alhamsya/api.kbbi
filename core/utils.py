from datetime import datetime
import pytz


def validate_int(param) -> bool:
    try:
        val = int(param)
        if val < 1:
            return False
        return True
    except ValueError:
        return False


def validate_int_between(param, smallest, biggest) -> bool:
    try:
        if int(smallest) <= int(param) <= int(biggest):
            return True
        return False
    except ValueError:
        return False


def get_now(region='ID', date_only=False):
    region.upper()
    tz = {
        'ID': 'Asia/Jakarta',
        'VN': 'Asia/Ho_Chi_Minh',
        'TW': 'Asia/Taipei',
        'TH': 'Asia/Bangkok',
        'BR': 'America/Sao_Paulo',
        'SG': 'Asia/Singapore',
        'US': 'America/Chicago',
        'RU': 'Europe/Moscow',
        'EUROPE': 'Europe/Amsterdam',
        'SAC': 'America/Sao_Paulo',
        'IND': 'Asia/Kolkata',
    }
    if date_only:
        return dt_to_str(datetime.now(pytz.timezone(tz[region])).date(), True)
    return dt_to_str(datetime.now(pytz.timezone(tz[region])))


def dt_to_str(dt: datetime, date_only=False):
    if date_only:
        return dt.strftime("%Y-%m-%d")
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def str_to_dt(dt: str, with_seconds=True):
    if with_seconds:
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
    return datetime.strptime(dt, '%Y-%m-%d').date()
