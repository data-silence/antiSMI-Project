from datetime import datetime, timedelta
from enum import Enum


class TimePart(Enum):
    NIGHT = 0  # 00:00 - 07:59 | Ночь
    MORNING = 1  # 08:00 - 12:59 | Утро
    AFTERNOON = 2  # 13:00 - 17:59 | День
    EVENING = 3  # 18:00 - 21:59 | Вечер
    LATE_NIGHT = 4  # 22:00 - 23:59 | Поздний вечер


class ServiceMode(Enum):
    WHOLE = 'whole'  # Полный режим | Whole mode
    LAST24 = 'last24'  # Последние 24 часа | Last 24 hours
    PRECISION = 'precision'  # Точный режим | Precision mode
    DIGEST = 'digest'  # Режим дайджеста | Digest mode


class NewsTimeManager:
    """
    Менеджер временных интервалов для новостных сервисов.

    Time interval manager for news services.
    """

    def __init__(self, mode: ServiceMode, start_date: datetime = None, end_date: datetime = None):
        """
        Инициализация менеджера временных интервалов.

        Initialize the time interval manager.

        :param mode: Режим работы | Operation mode
        :param start_date: Начальная дата (опционально) | Start date (optional)
        :param end_date: Конечная дата (опционально) | End date (optional)
        """
        self.mode = mode
        self.start_date = start_date
        self.end_date = end_date

    def get_time_range(self) -> tuple[datetime, datetime]:
        """
        Получить временной интервал в зависимости от режима работы.

        Get the time interval based on the operation mode.

        :return: Кортеж из начальной и конечной даты | Tuple of start and end datetime
        """
        now = datetime.now().replace(tzinfo=None)

        match self.mode:
            case ServiceMode.WHOLE:
                return self._get_whole_range()
            case ServiceMode.LAST24:
                return self._get_last24_range(now)
            case ServiceMode.PRECISION:
                return self._get_precision_range(now)
            case ServiceMode.DIGEST:
                return self._get_digest_range(now)
            case _:
                raise ValueError("Неизвестный режим работы | Unknown operation mode")

    def _get_whole_range(self) -> tuple[datetime, datetime]:
        """
        Получить временной интервал для режима WHOLE.

        Get the time interval for WHOLE mode.

        :return: Кортеж из начальной и конечной даты | Tuple of start and end datetime
        """
        if not self.start_date:
            raise ValueError(
                "Для режима WHOLE необходимо указать начальную дату | Start date is required for WHOLE mode")

        start = datetime.combine(self.start_date, datetime.min.time())
        if self.end_date:
            end = datetime.combine(self.end_date, datetime.max.time())
        else:
            end = datetime.combine(self.start_date, datetime.max.time())

        return start.replace(tzinfo=None), end.replace(tzinfo=None, microsecond=0)

    def _get_last24_range(self, now: datetime) -> tuple[datetime, datetime]:
        """
        Получить временной интервал для режима LAST24.

        Get the time interval for LAST24 mode.

        :param now: Текущее время | Current time
        :return: Кортеж из начальной и конечной даты | Tuple of start and end datetime
        """
        end = now.replace(minute=0, second=0, microsecond=0)
        start = end - timedelta(hours=24)
        return start, end

    def _get_precision_range(self, now: datetime) -> tuple[datetime, datetime]:
        """
        Получить временной интервал для режима PRECISION.

        Get the time interval for PRECISION mode.

        :param now: Текущее время | Current time
        :return: Кортеж из начальной и конечной даты | Tuple of start and end datetime
        """
        time_part = self._get_time_part(now)
        end = now.replace(second=0, microsecond=0)

        match time_part:
            case TimePart.NIGHT | TimePart.MORNING:
                start = (now - timedelta(days=1)).replace(hour=21, minute=56, second=0, microsecond=0)
            case TimePart.AFTERNOON:
                start = now.replace(hour=8, minute=56, second=0, microsecond=0)
            case TimePart.EVENING:
                start = now.replace(hour=12, minute=56, second=0, microsecond=0)
            case TimePart.LATE_NIGHT:
                start = now.replace(hour=17, minute=56, second=0, microsecond=0)

        return start, end

    def _get_digest_range(self, now: datetime) -> tuple[datetime, datetime]:
        """
        Получить временной интервал для режима DIGEST.

        Get the time interval for DIGEST mode.

        :param now: Текущее время | Current time
        :return: Кортеж из начальной и конечной даты | Tuple of start and end datetime
        """
        time_part = self._get_time_part(now)

        match time_part:
            case TimePart.NIGHT:
                start = (now - timedelta(days=1)).replace(hour=17, minute=56, second=0, microsecond=0)
                end = (now - timedelta(days=1)).replace(hour=21, minute=55, second=59, microsecond=0)
            case TimePart.MORNING:
                start = (now - timedelta(days=1)).replace(hour=21, minute=56, second=0, microsecond=0)
                end = now.replace(hour=8, minute=55, second=59, microsecond=0)
            case TimePart.AFTERNOON:
                start = now.replace(hour=8, minute=56, second=0, microsecond=0)
                end = now.replace(hour=12, minute=55, second=59, microsecond=0)
            case TimePart.EVENING:
                start = now.replace(hour=12, minute=56, second=0, microsecond=0)
                end = now.replace(hour=17, minute=55, second=59, microsecond=0)
            case TimePart.LATE_NIGHT:
                start = now.replace(hour=17, minute=56, second=0, microsecond=0)
                end = now.replace(hour=21, minute=55, second=59, microsecond=0)

        return start, end

    def _get_time_part(self, now: datetime) -> TimePart:
        """
        Определить часть дня на основе текущего времени.

        Determine the part of the day based on the current time.

        :param now: Текущее время | Current time
        :return: Часть дня | Part of the day
        """
        hour = now.hour
        if 0 <= hour < 8:
            return TimePart.NIGHT
        elif 8 <= hour < 13:
            return TimePart.MORNING
        elif 13 <= hour < 18:
            return TimePart.AFTERNOON
        elif 18 <= hour < 22:
            return TimePart.EVENING
        else:
            return TimePart.LATE_NIGHT