import re

import numpy as np


def to_isoformat(tm):
    """
    Returns an ISO 8601 string from a time object (of different types).

    :param tm: Time object
    :return: (str) ISO 8601 time string
    """
    if type(tm) == np.datetime64:
        return str(tm).split(".")[0]
    else:
        return tm.isoformat()


class AnyCalendarDateTime:
    """
    A class to represent a datetime that could be of any calendar.

    Has the ability to add and subtract a day from the input based on MAX_DAY, MIN_DAY, MAX_MONTH and MIN_MONTH
    """

    # MAX_DAY: the maximum number of days in any month in any of the calendars supported by cftime
    MAX_DAY = 31
    MIN_DAY = 1
    MAX_MONTH = 12
    MIN_MONTH = 1

    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return (
            f"{self.year}-{self.month:02d}-{self.day:02d}"
            f"T{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        )

    def add_day(self):
        """
        Add a day to the input datetime.
        """
        self.day += 1

        if self.day > self.MAX_DAY:
            self.month += 1
            self.day = 1

        if self.month > self.MAX_MONTH:
            self.year += 1
            self.month = self.MIN_MONTH

    def sub_day(self, n=1):
        """
        Subtract a day to the input datetime.
        """
        self.day -= 1

        if self.day < self.MIN_DAY:
            self.month -= 1
            self.day = self.MAX_DAY

        if self.month < self.MIN_MONTH:
            self.year -= 1
            self.month = self.MAX_MONTH


def str_to_AnyCalendarDateTime(dt):
    """
    Takes a string representing date/time and returns a DateTimeAnyTime object.
    String formats should start with Year and go through to Second, but you
    can miss out anything from month onwards.

    :param dt: string representing a date/time [string]
    :return: AnyCalendarDateTime object
    """
    if len(dt) < 1:
        raise Exception(
            "Must provide at least the year as argument to create date time."
        )

    # Start with most common pattern
    regex = re.compile(r"^(\d+)-(\d+)-(\d+)[T ](\d+):(\d+):(\d+)$")
    match = regex.match(dt)

    if match:
        items = match.groups()
    else:
        # Try a more complex split and build of the time string
        defaults = [-1, 1, 1, 0, 0, 0]
        components = re.split("[- T:]", dt)

        # Build a list of time components
        items = components + defaults[len(components) :]

    return AnyCalendarDateTime(*[int(i) for i in items])
