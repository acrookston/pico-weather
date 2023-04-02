from runLoop import Operation
from logger import Logger, Formatter, StreamHandler, FileHandler, ERROR
import sys, os, time

MAX_LOG_SIZE = 100_000

class LogManager(Operation):
    logger = None
    formatter = None
    applicationLogger = None
    errorLogger = None
    applicationLogName = "application.log"
    errorLogName = "error.log"
    maxLogSize = MAX_LOG_SIZE
    minFreeSpace = MAX_LOG_SIZE

    def __init__(self, maxLogSize=MAX_LOG_SIZE, minFreeStorage=MAX_LOG_SIZE):
        super().__init__("logManager", True, 30_000)
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
        self.maxLogSize = maxLogSize
        self.minFreeSpace = minFreeStorage

    def freeSpace(self):
        try:
            # statvfs output: (4096, 4096, 212, 67, 67, 0, 0, 0, 0, 255)
            stats = os.statvfs('//')
            return stats[0] * stats[3] # / 1048576
        except OSError:
            return -1

    def purgeLogFiles(self):
        freeSpace = self.freeSpace()
        underAllowedSpace = freeSpace < self.minFreeSpace
        self.logger.info("System storage free space: {}. Min free allowed: {}", freeSpace, self.minFreeSpace)
        removedFiles = False
        # os.stat output: (32768, 0, 0, 0, 0, 0, 358115, 1676245004, 1676245004, 1676245004)
        for handler in (self.applicationLogger, self.errorLogger):
            try:
                stats = os.stat(handler.filename)
                if underAllowedSpace or stats[6] > self.maxLogSize:
                    handler.close()
                    os.remove(handler.filename)
                    time.sleep(0.1)
                    self.logger.info("Purged file: {} size: {}", handler.filename, stats[6])
                    removedFiles = True
            except OSError as error:
                self.logger.exc(error, "Log file check error {}", handler.filename)
        if removedFiles:
            self.logger.info("System storage free space: {}. Min free allowed: {}", self.freeSpace(), self.minFreeSpace)

    # Operation
    def execute(self, runLoop):
        self.purgeLogFiles()