from datetime import datetime


def now_iso():
    return datetime.now().isoformat(timespec='milliseconds')


def timedelta(close_date, create_date):
    return (
        datetime.fromisoformat(close_date) -
        datetime.fromisoformat(create_date)
    )
