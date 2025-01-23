from datetime import datetime as dt


def get_timedelta(timestamp):
    return str(dt.fromtimestamp(timestamp) - dt.fromtimestamp(0))
