from roocs_utils.utils.time_utils import AnyCalendarDateTime
from roocs_utils.utils.time_utils import str_to_AnyCalendarDateTime


def test_AnyCalendarDateTime():
    d = AnyCalendarDateTime(1997, 4, 9, 0, 0, 0)
    assert d.value == "1997-04-09T00:00:00"


def test_str_to_AnyCalendarDateTime():
    d = str_to_AnyCalendarDateTime("1999-01-31")
    d.sub_day()
    assert d.value.startswith("1999-01-30")

    d.add_day()
    d.add_day()
    assert d.value.startswith("1999-02-01")

    d = str_to_AnyCalendarDateTime("1999-01-33")
    d.sub_day()
    d.sub_day()
    assert d.value.startswith("1999-01-31")

    d = str_to_AnyCalendarDateTime("1999-01-01T12:13:14")
    d.sub_day()
    assert d.value == "1998-12-31T12:13:14"


def test_irregular_datetimes():
    # looks like no year
    d = str_to_AnyCalendarDateTime("01-02")
    #  first value is taken as the year
    assert d.value == "1-02-01T00:00:00"

    # month is 00
    d = str_to_AnyCalendarDateTime("1999-00-33")
    assert d.value == "1999-00-33T00:00:00"

    d.add_day()
    assert d.value == "1999-01-01T00:00:00"

    # month is 00
    d = str_to_AnyCalendarDateTime("1999-00-33")
    assert d.value == "1999-00-33T00:00:00"

    d.sub_day()
    d.sub_day()
    assert d.value == "1998-12-31T00:00:00"
