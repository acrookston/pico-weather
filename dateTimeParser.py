from machine import RTC

class DateTimeParser:
    year = 0
    month = 0
    day = 0
    dayOfWeek = 0
    hour = 0
    minute = 0
    second = 0
    microsecond = 0

    def datetime(self):
        return (self.year, self.month, self.day, self.dayOfWeek, self.hour, self.minute, self.second, self.microsecond)

    def rtc(self):
        rtc = RTC()
        rtc.datetime(self.datetime())
        return rtc

class ISO8601StringParser(DateTimeParser):
    # Handles ISO 8601 format. E.G.: 2023-01-22T14:53:48+01:00
    def __init__(self, string):
        try:
            parts = string.split("T")
            dateParts = parts[0].split("-")
            timeParts = parts[1].split("+")
            time = timeParts[0].split(":")
            self.year = int(dateParts[0])
            self.month = int(dateParts[1])
            self.day = int(dateParts[2])
            self.hour = int(time[0])
            self.minute = int(time[1])
            self.second = int(time[2])
        except Exception as e:
            raise RuntimeError(f'Could not parse ISO8601 date string {string}') from e
                

class RTCStringParser(DateTimeParser):
    # Handles comma-separated format. E.G.: 2022,05,11,0,12,14,23,000000
    def __init__(self, string):
        try:
            rtcstring = string.split(',')
            (self.year, self.month, self.day, self.dayOfWeek, self.hour, self.minute, self.second, self.microsecond) = map(lambda x: int(x), rtcstring)
        except Exception as e:
            raise RuntimeError(f'Could not parse RTC date string {string}') from e
