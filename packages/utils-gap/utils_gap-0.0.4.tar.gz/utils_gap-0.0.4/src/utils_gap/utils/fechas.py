from datetime import datetime

def to_tmsp(date):
    return int(date.timestamp()) * 1000

def from_pd_date(date):
    tmsp = to_tmsp(date)
    return datetime.fromtimestamp(int(tmsp/1000))