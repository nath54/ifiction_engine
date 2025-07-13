#
from typing import Any
#
from datetime import date
import calendar


#
def get_days_in_current_month(year: int, month: int) -> int:
    """
    Returns the number of days in the current month.

    Returns:
        int: The number of days in the current month.
    """

    # calendar.monthrange returns a tuple: (weekday of first day, number of days in month)
    # We are interested in the second element (number of days)
    #
    num_days: int
    #
    _, num_days = calendar.monthrange(year, month + 1)

    #
    return num_days


#
def get_day_of_week(year: int, month: int, day: int) -> str:
    """
    Returns the day of the week for a given date.

    Args:
        year (int): The year.
        month (int): The month number (1-12).
        day (int): The day number (1-31).

    Returns:
        str: The full name of the day of the week (e.g., "Monday").
                Returns an error message if the date is invalid.
    """

    #
    try:
        #
        d: date = date(year, month + 1, day + 1)
        #
        return d.strftime('%A')

    #
    except Exception as _e:
        #
        return "Monday"

#
MONTH_NAMES: list[str] = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

#
DAY_NAMES: list[str] = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


#
class GameTime:

    #
    def __init__(
        self,
        year: int = 0,
        month: int = 0,
        day: int = 0,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> None:

        #
        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hour: int = hour
        self.minute: int = minute
        self.second: int = second
        #
        self.regule()

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "second": self.second
        }

    #
    def __str__(self) -> str:
        #
        return f"Year {self.year}, {MONTH_NAMES[self.month]}, {get_day_of_week(year=self.year, month=self.month, day=self.day)} {self.day + 1} - {self.hour:02}:{self.minute:02}:{self.second:02}"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()

    #
    def __hash__(self) -> int:
        #
        return hash( self.__str__() )

    #
    def regule_month(self) -> None:
        #
        while self.month < 0:
            #
            self.month += 12
            self.year -= 1
        #
        while self.month >= 12:
            #
            self.month -= 12
            self.year += 1

    #
    def regule_days(self) -> None:
        #
        while self.day < 0:
            #
            self.month -= 1
            self.day += get_days_in_current_month(year=self.year, month=self.month)
            #
            self.regule_month()
        #
        while self.day > get_days_in_current_month(year=self.year, month=self.month):
            #
            self.month += 1
            self.day -= get_days_in_current_month(year=self.year, month=self.month)
            #
            self.regule_month()

    #
    def regule_hours(self) -> None:
        #
        while self.hour < 0:
            #
            self.hour += 24
            self.day -= 1
            #
            self.regule_days()
        #
        while self.hour >= 24:
            #
            self.hour -= 24
            self.day += 1
            #
            self.regule_days()

    #
    def regule_minutes(self) -> None:
        #
        while self.minute < 0:
            #
            self.minute += 60
            self.hour -= 1
            #
            self.regule_hours()
        #
        while self.minute >= 60:
            #
            self.minute -= 60
            self.hour += 1
            #
            self.regule_hours()

    #
    def regule_seconds(self) -> None:
        #
        while self.second < 0:
            #
            self.second += 60
            self.minute -= 1
            #
            self.regule_minutes()
        #
        while self.second >= 24:
            #
            self.second -= 60
            self.minute += 1
            #
            self.regule_minutes()

    #
    def regule(self) -> None:
        #
        self.regule_month()
        self.regule_days()
        self.regule_hours()
        self.regule_minutes()
        self.regule_seconds()

    #
    def duplicate(self) -> "GameTime":
        #
        return GameTime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second)

    #
    def to_tuple(self) -> tuple[int, int, int, int, int, int]:
        #
        return (self.year, self.month, self.day, self.hour, self.minute, self.second)

    #
    def __add__(self, d: Any) -> Any:
        #
        if not isinstance(d, GameTime):
            #
            return GameTime()

        #
        self.second += d.second
        self.minute += d.minute
        self.hour += d.hour
        self.day += d.day
        self.month += d.month
        self.year += d.year
        #
        self.regule()
        #
        return self

    #
    def __sub__(self, d: Any) -> Any:
        #
        if not isinstance(d, GameTime):
            #
            return GameTime()

        #
        self.second -= d.second
        self.minute -= d.minute
        self.hour -= d.hour
        self.day -= d.day
        self.month -= d.month
        self.year -= d.year
        #
        self.regule()
        #
        return self

    #
    def __eq__(self, d: Any) -> bool:
        #
        if not isinstance(d, GameTime):
            #
            return False
        #
        return  self.second == d.second and \
                self.minute == d.minute and \
                self.hour == d.hour and \
                self.day == d.day and \
                self.month == d.month and \
                self.year == d.year

    #
    def __ne__(self, d: Any) -> bool:
        #
        if not isinstance(d, GameTime):
            #
            return False
        #
        return not self.__eq__(d)

    #
    def __gt__(self, d: Any) -> bool:
        #
        if not isinstance(d, GameTime):
            #
            return False
        #
        return self.to_tuple() > d.to_tuple()

    #
    def __gte__(self, d: Any) -> bool:
        #
        if not isinstance(d, GameTime):
            #
            return False
        #
        return self.to_tuple() >= d.to_tuple()

    #
    def __lt__(self, d: Any) -> bool:
        #
        if not isinstance(d, GameTime):
            #
            return False
        #
        return self.to_tuple() < d.to_tuple()

    #
    def __lte__(self, d: Any) -> bool:
        #
        if not isinstance(d, GameTime):
            #
            return False
        #
        return self.to_tuple() <= d.to_tuple()

    #
    def __mul__(self, factor: Any) -> "GameTime":
        #
        if not isinstance(factor, int) and not isinstance(factor, float):
            #
            return GameTime()
        #
        self.second = int( self.second * factor )
        self.minute = int( self.minute * factor )
        self.hour = int( self.hour * factor )
        self.day = int( self.day * factor )
        self.month = int( self.month * factor )
        self.year = int( self.year * factor )
        #
        self.regule()
        #
        return self

    #
    def __div__(self, factor: Any) -> "GameTime":
        #
        if (not isinstance(factor, int) and not isinstance(factor, float)) or factor == 0:
            #
            return GameTime()
        #
        self.second = int( self.second / factor )
        self.minute = int( self.minute / factor )
        self.hour = int( self.hour / factor )
        self.day = int( self.day / factor )
        self.month = int( self.month / factor )
        self.year = int( self.year / factor )
        #
        self.regule()
        #
        return self

