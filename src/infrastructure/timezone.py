from enum import Enum


class TimeZone(str, Enum):
    UTC_N12 = "Pacific/Auckland"
    UTC_N11 = "Pacific/Midway"
    UTC_N10 = "Pacific/Honolulu"
    UTC_N9 = "America/Anchorage"
    UTC_N8 = "America/Los_Angeles"
    UTC_N7 = "America/Dawson"
    UTC_N6 = "America/El_Salvador"
    UTC_N5 = "America/Jamaica"
    UTC_N4 = "America/Antigua"
    UTC_N3 = "America/Buenos_Aires"
    UTC_N2 = "Atlantic/South_Georgia"
    UTC_N1 = "Atlantic/Cape_Verde"

    UTC_0 = "Europe/London"

    UTC_P1 = "Europe/Paris"
    UTC_P2 = "Europe/Athens"
    UTC_P3 = "Europe/Moscow"
    UTC_P4 = "Asia/Dubai"
    UTC_P5 = "Asia/Karachi"
    UTC_P6 = "Asia/Dhaka"
    UTC_P7 = "Asia/Bangkok"
    UTC_P8 = "Asia/Singapore"
    UTC_P9 = "Asia/Seoul"
    UTC_P10 = "Australia/Brisbane"
    UTC_P11 = "Pacific/Guadalcanal"
    UTC_P12 = "Pacific/Auckland"
