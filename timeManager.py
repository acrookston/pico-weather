from machine import RTC
from dateTimeParser import ISO8601StringParser
from runLoop import Events, EventArgs, Operation
from config import Config

class TimeStatus:
    UNSET = 0
    SET = 1
    ERROR = 2


class TimeManager(Operation):
    logger = None
    networkManager = None
    rtc = RTC()
    timeStatus = TimeStatus.UNSET

    def __init__(self, networkManager, logger):
        super().__init__("timeManager", True, 10_000)
        self.logger = logger
        self.networkManager = networkManager

    def execute(self, runLoop):
        self.fetchTime(runLoop)

    def handleEvent(self, runLoop, event, args):
        pass

    def fetchTime(self, runLoop):
        result = self.networkManager.httpGet(Config.TIME_SERVER, Config.TIME_PATH, port=Config.TIME_PORT)
        if result != None:
            try:
                parser = ISO8601StringParser(result.text)
                self.rtc.datetime(parser.datetime())
                self.timeStatus = TimeStatus.SET
                runLoop.fireEvent(Events.UPDATE_TIME, { EventArgs.TIME: self.rtc })
            except:
                self.timeStatus = TimeStatus.ERROR
