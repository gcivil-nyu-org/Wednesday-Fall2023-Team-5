import datetime


def start_date_in_future(std):
    if isinstance(std, datetime.date):
        return std > datetime.date.today()
    else:
        raise TypeError("Arguments must be of type datetime.date")


def end_date_after_start_date(std, end):
    if isinstance(std, datetime.date) and isinstance(end, datetime.date):
        return end > std
    else:
        raise TypeError("Arguments must be of type datetime.date")
