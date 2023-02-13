from logger  import Logger, Formatter, StreamHandler, FileHandler, ERROR
import sys,  os

MAX_LOG_SIZE = 500_000

class LogManager:
    logger = None
    formatter = None
    applicationLogger = None
    errorLogger = None
    applicationLogName = "application.log"
    errorLogName = "error.log"

    def __init__(self):
        self.logger = Logger("application-logger")
        self.formatter = Formatter(style="{")
        sh = StreamHandler(stream=sys.stdout)
        sh.formatter = self.formatter
        self.logger.addHandler(sh)
        self.applicationLogger = FileHandler(self.applicationLogName)
        self.applicationLogger.formatter = self.formatter
        self.logger.addHandler(self.applicationLogger)
        self.errorLogger = FileHandler(self.errorLogName, level=ERROR)
        self.errorLogger.formatter = self.formatter
        self.logger.addHandler(self.errorLogger)

    def purgeLogFiles(self):
        # (32768, 0, 0, 0, 0, 0, 358115, 1676245004, 1676245004, 1676245004)
        for handler in (self.applicationLogger, self.errorLogger):
            try:
                stats = os.stat(handler.filename)
                if stats[6] > MAX_LOG_SIZE:
                    handler.close()
                    os.remove(handler.filename)
                    self.logger.info("Purged file: {} size: {}", handler.filename, stats[6])
            except OSError as error:
                self.logger.exc(error, "Log file check error {}", handler.filename)
