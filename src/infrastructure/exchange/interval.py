from enum import Enum


class Interval(Enum):
    DAY = 'day'
    M1 = 'minute1'
    M3 = 'minute3'
    M5 = 'minute5'
    M10 = 'minute10'
    M15 = 'minute15'
    M30 = 'minute30'
    M60 = 'minute60'
    M240 = 'minute240'
    WEEK = 'week'
    MONTH = 'month'
