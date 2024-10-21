from datetime import datetime, timedelta


def get_time_period(user_start: datetime.date, user_end: datetime.date = None,
                    date_part: int = None, mode: str = None) -> tuple:
    """
    Helps to convert dates to datetime objects for handlers usage.
    It has two modes: when the exact period of the last tranche of recent news is required,
    or when just all the news of the day is required
    """

    # 1. Determining the correct day depending on the query conditions:
    one_day = timedelta(days=1)

    handler_start = datetime(year=user_start.year, month=user_start.month, day=user_start.day, hour=00, minute=00)

    # If the end date has been transferred [for Timemachine Service]
    if user_end is None:
        handler_end = handler_start.replace(hour=23, minute=59)
    else:
        handler_end = datetime(year=user_end.year, month=user_end.month, day=user_end.day, hour=23, minute=59)

    # When news in the current time period has not been received -> it is necessary to use the news of the previous day
    if date_part == 0:
        handler_start = handler_start - one_day
        handler_end = handler_end - one_day
    if date_part == 1:
        handler_start = handler_start - one_day

    # 2. Determining the correct time depending on mode and date_part
    match mode:
        case 'precision':
            if date_part == 0:
                handler_start = handler_start.replace(hour=20, minute=56)
                handler_end = handler_end.replace(hour=22, minute=55)
            if date_part == 1:
                handler_start = handler_start.replace(hour=22, minute=56)
                handler_end = handler_end.replace(hour=8, minute=55)
            if date_part == 2:
                handler_start = handler_start.replace(hour=8, minute=56)
                handler_end = handler_end.replace(hour=12, minute=55)
            if date_part == 3:
                handler_start = handler_start.replace(hour=12, minute=56)
                handler_end = handler_end.replace(hour=16, minute=55)
            if date_part == 4:
                handler_start = handler_start.replace(hour=16, minute=56)
                handler_end = handler_end.replace(hour=20, minute=55)
            return handler_start, handler_end
        case _:
            return handler_start, handler_end
