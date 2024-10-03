from datetime import (
    datetime as dt,
    timedelta
)
from typing import Optional


class CheckMinute(object):
    """
    Class for checking the minute and calculating the current and next hour.
    """

    @classmethod
    def calc_minute(cls, curMinute: int) -> dt:
        """
        Method for calculating minutes per hour.
        ----------------------------------------
        :type curMinute: int
        :param curMinute: any minute.

        :rtype: datetime
        :returns: datetime(year, month, day, hour, minute, second).
        """
        curMinute = dt.now().replace(
            minute=curMinute,
            second=0,
            microsecond=0
        )
        if curMinute.minute <= dt.now().minute:
            curMinute = curMinute + timedelta(minutes=60)
        return curMinute

    def __init__(self, minute: int) -> None:
        """
        CheckMinute constructor object for calculating time.
        ----------------------------------------------------
        :type minute: int
        :param minute: any minute.

        :type self.dTime: datetime
        :param self.dTime: сalculate datetime(\
            year, month, day, hour, minute, second).
        """
        if minute is None or minute < 0:
            minute = dt.now().minute
        if minute > 60:
            raise ValueError(
                f"Error. The minute='{minute}' is incorrect ("
                "'minute' must be in 0..60)"
            )
        elif minute == 60:
            minute = 0

        self.dTime = self.calc_minute(minute)


class CheckHour(object):
    """
    Class for checking the hours and calculating the current and next day.
    """

    @classmethod
    def calc_hour(
        cls,
        curHour: int,
        curMinute: int
    ) -> dt:
        """
        Method for calculating hours in a day.
        --------------------------------------
        :type curHour: int
        :param curHour: any hour.

        :type curMinute: int
        :param curMinute: any minute.

        :rtype: datetime
        :returns: datetime(year, month, day, hour, minute, second).
        """
        curHour = dt.now().replace(
            hour=curHour,
            minute=curMinute,
            second=0,
            microsecond=0
        )
        if curHour.time() < dt.now().time():
            curHour = curHour + timedelta(hours=24)
        return curHour

    def __init__(
        self,
        hour: int,
        minute: int
    ) -> None:
        """
        CheckHour constructor object for calculating time.
        --------------------------------------------------
        :type hour: int
        :param hour: any hour.

        :type minute: int
        :param minute: any minute.

        :type self.dTime: datetime
        :param self.dTime: сalculate datetime(\
            year, month, day, hour, minute, second).
        """
        if hour is None or hour < 0:
            hour = dt.now().hour
        if hour > 24:
            raise ValueError(
                f"Error. The hour='{hour}' is incorrect ("
                "'hour' must be in 0..24)"
            )
        elif hour == 24:
            hour = 0

        self.dTime = self.calc_hour(
            hour,
            CheckMinute(minute).dTime.minute
        )


class CheckDays(object):
    """
    Class for checking the days and calculating the current and next month.
    """

    @staticmethod
    def calc_day_in_month(year: int, month: int) -> int:
        """
        Method for checking the number of days in a month.
        --------------------------------------------------
        :type year: int
        :param year: any year.

        :type month: int
        :param month: any month.

        :rtype: int
        :returns: number of days in the current month.
        """
        next_month = month % 12 + 1
        next_year = year + month // 12
        totalDay = (
            dt(next_year, next_month, 1) - dt(year, month, 1)
        ).days
        return totalDay

    @classmethod
    def calc_day(
        cls,
        curDay: int,
        curHour: int,
        curMinute: int
    ) -> dt:
        """
        Method for calculating the days of the month.
        ---------------------------------------------
        :type curDay: int
        :param curDay: any days.

        :type curHour: int
        :param curHour: any hour.

        :type curMinute: int
        :param curMinute: any minute.

        :rtype: datetime
        :returns: datetime(year, month, day, hour, minute, second).
        """
        countDayCurMonth = cls.calc_day_in_month(
            dt.now().year,
            dt.now().month
        )
        if curDay > countDayCurMonth:
            curDay = (
                dt.now() + timedelta(days=curDay)
            ).replace(
                day=curDay,
                hour=curHour,
                minute=curMinute,
                second=0,
                microsecond=0
            )
            return curDay

        curDay = dt.now().replace(
            day=curDay,
            hour=curHour,
            minute=curMinute,
            second=0,
            microsecond=0
        )
        if curDay.timestamp() < dt.now().timestamp():
            curDay = curDay + timedelta(days=countDayCurMonth)

        return curDay

    def __init__(
        self,
        day: int,
        hour: int,
        minute: int
    ) -> None:
        """
        CheckDays constructor object for calculating date and time.
        -----------------------------------------------------------
        :type day: int
        :param day: any day.

        :type hour: int
        :param hour: any hour.

        :type minute: int
        :param minute: any minute.

        :type self.dTime: datetime
        :param self.dTime: сalculate datetime(\
            year, month, day, hour, minute, second).
        """
        if day is None or day < 0:
            day = dt.now().day
        if day == 0 or day > 31:
            raise ValueError(
                f"Error. The day='{day}' is incorrect ("
                "'day' must be in 1..31)"
            )
        self.dTime = self.calc_day(
            day,
            CheckHour(hour, minute).dTime.hour,
            CheckMinute(minute).dTime.minute
        )


class CheckMonth(object):
    """
    Class for checking the month and calculating the current and next year.
    """

    @classmethod
    def calc_month(
        cls,
        curMonth: int,
        curDay: int,
        curHour: int,
        curMinute: int,
        checkDay: Optional[CheckDays] = None
    ) -> dt:
        """
        Method of calculation by months of the year.
        --------------------------------------------
        :type curMonth: int
        :param curMonth: any month.

        :type curDay: int
        :param curDay: any days.

        :type curHour: int
        :param curHour: any hour.

        :type curMinute: int
        :param curMinute: any minute.

        :type checkDay: CheckDays
        :param checkDay: checking days in the current or next month.

        :rtype: datetime
        :returns: datetime(year, month, day, hour, minute, second).
        """
        year = dt.now().year
        countDayCurMonth = checkDay(year, curMonth)  # Current year
        if curDay > countDayCurMonth:
            curMonth += 1
            curDay -= countDayCurMonth

        cursorMonth = dt(
            year=year,
            month=curMonth,
            day=curDay,
            hour=curHour,
            minute=curMinute,
            second=0,
            microsecond=0
        )

        if cursorMonth.timestamp() < dt.now().timestamp():
            year += 1
            countDayCurMonth = checkDay(year, curMonth)  # Next year
            if curDay > countDayCurMonth:
                curMonth += 1
                curDay -= countDayCurMonth
            cursorMonth = cursorMonth.replace(
                year=year,
                month=curMonth,
                day=curDay
            )
        return cursorMonth

    def __init__(
        self,
        month: int,
        day: int,
        hour: int,
        minute: int
    ) -> None:
        """
        CheckMonth constructor object for calculating date and time.
        ------------------------------------------------------------
        :type month: int
        :param month: any month.

        :type day: int
        :param day: any day.

        :type hour: int
        :param hour: any hour.

        :type minute: int
        :param minute: any minute.

        :type self.dTime: datetime
        :param self.dTime: сalculate datetime(\
            year, month, day, hour, minute, second).
        """
        if month is None or month < 0:
            month = dt.now().month
        if month == 0 or month > 12:
            raise ValueError(
                f"Error. The month='{month}' is incorrect ("
                "'month' must be in 1..12)"
            )
        self.dTime = self.calc_month(
            month,
            day,
            CheckHour(hour, minute).dTime.hour,
            CheckMinute(minute).dTime.minute,
            CheckDays(day, hour, minute).calc_day_in_month
        )


class AddPlanTask(object):
    """Сlass date and time scheduled tasks."""

    def __init__(
        self,
        month: int = None,
        day: int = None,
        hour: int = None,
        minute: int = None
    ) -> None:
        """
        AddPlanTask constructor object for obtaining the planned date and time.
        -----------------------------------------------------------------------
        args:
            month: int - current range of months [0..12] in the year.
            day: int - current range of days [0..31] in month.
            hour: int - current range [0..60] in day.
            minute: int - current range [0..60] in hour.
        """
        self.mo = month
        self.d = day
        self.h = hour
        self.m = minute

    def current_datetime(self) -> dt:
        """
        Method for obtaining the planning date and time.
        ------------------------------------------------
        @returns: datetime(year, month, day, hour, minute, second).
        """
        if self.mo is not None:
            return CheckMonth(
                self.mo,
                self.d,
                self.h,
                self.m
            ).dTime
        elif self.d is not None:
            return CheckDays(
                self.d,
                self.h,
                self.m
            ).dTime
        elif self.h is not None:
            return CheckHour(
                self.h,
                self.m
            ).dTime
        elif self.m is not None:
            return CheckMinute(self.m).dTime
        else:
            return (
                dt.now() + timedelta(minutes=1)
            ).replace(
                second=0,
                microsecond=0
            )


class AddIntervalTask(object):
    """Class date and time intervals of scheduled tasks."""

    def __init__(
        self,
        month: int | float = None,
        day: int | float = None,
        hour: int | float = None,
        minute: int | float = None
    ) -> None:
        """
        AddIntervalTask constructor object to get the interval date and time.
        ---------------------------------------------------------------------
        args:
            month: int | float - range of numbers [0..n or 0.1..n] months \
                of the year.
            day: int | float - range of numbers [0..n or 0.1..n] days \
                in a month.
            hour: int | float - number range [0..n or 0.1..n] hour per day.
            minute: int - number range [0..n] minutes in hour.
            minute: float - range of numbers [0,1..n] seconds in minutes.
        """
        self.mo = month
        self.d = day
        self.h = hour
        self.m = minute
        self.initDtime = dt.now()

    @property
    def calc_minute(self) -> dt:
        """
        Method calculation minutes.
        ---------------------------
        @returns: datetime(year, month, day, hour, minute, second).
        """
        if self.m is None or self.m < 0:
            self.m = 0

        if isinstance(self.m, int):
            self.m = (self.initDtime + timedelta(
                minutes=self.m
            )).replace(second=0)
        elif isinstance(self.m, float):
            self.m = self.initDtime + timedelta(
                seconds=self.m
            )
        return self.m.replace(
            microsecond=0
        )

    @property
    def calc_hour(self) -> dt:
        """
        Method calculation hour.
        ---------------------------
        @returns: datetime(year, month, day, hour, minute, second).
        """
        if self.h is None or self.h < 0:
            self.h = 0
        self.m = self.calc_minute

        self.h = self.initDtime + timedelta(
            hours=self.h
        )
        return self.h.replace(
            minute=self.m.minute,
            second=self.m.second,
            microsecond=0
        )

    @property
    def calc_days(self) -> dt:
        """
        Method calculation day.
        ---------------------------
        @returns: datetime(year, month, day, hour, minute, second).
        """
        if self.d is None or self.d < 0:
            self.d = 0
        self.h = self.calc_hour

        self.d = self.initDtime + timedelta(
            days=self.d
        )

        return self.d.replace(
            hour=self.h.hour,
            minute=self.h.minute,
            second=self.h.second,
            microsecond=0
        )

    @property
    def calc_month(self) -> dt:
        """
        Method calculation month.
        ---------------------------
        @returns: datetime(year, month, day, hour, minute, second).
        """
        if self.mo is None or self.mo < 0:
            self.mo = 0

        self.initDtime = self.calc_days
        self.mo = self.initDtime + timedelta(
            days=self.mo * 30.4375
        )
        return self.mo

    def current_datetime(self) -> dt:
        """
        Method for obtaining date and time intervals.
        ---------------------------------------------
        @returns: datetime(year, month, day, hour, minute, second).
        """
        if self.mo is not None:
            return self.calc_month
        elif self.d is not None:
            return self.calc_days
        elif self.h is not None:
            return self.calc_hour
        elif self.m is not None:
            return self.calc_minute
        else:
            return (
                dt.now() + timedelta(minutes=1)
            ).replace(
                second=0,
                microsecond=0
            )
