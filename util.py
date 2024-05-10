from datetime import timedelta
from math import ceil


def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - timedelta(days=next_month.day)


def events_in_month(cal, date_in_month):
    start = date_in_month.floor("month")
    end = date_in_month.ceil("month")
    return [ev for ev in cal.timeline.overlapping(start, end)]


def waking_hours(event):
    if event.duration < timedelta(hours=8):
        return event.duration
    num_days = ceil(event.duration / timedelta(days=1))
    return event.duration - timedelta(hours=8 * num_days)


def total_waking_hours(events):
    total = timedelta(hours=0)
    for ev in events:
        total += waking_hours(ev)
    return total
