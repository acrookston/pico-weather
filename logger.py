import utime
import sys
import uio

CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0

_level_dict = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
    NOTSET: "NOT SET",
}

class Logger:
    name = None
    level = NOTSET
    handlers = []

    def __init__(self, name, level=NOTSET):
        self.name = name
        self.level = level

    def _level_str(self, level):
        l = _level_dict.get(level)
        if l is not None:
            return l
        return "LVL%s" % level

    def setLevel(self, level):
        self.level = level

    def isEnabledFor(self, level):
        return level >= self.level

    def log(self, level, msg, *args):
        if self.isEnabledFor(level):
            record = LogRecord(
                self.name, level, None, None, msg, args, None, None, None
            )
            if self.handlers:
                for hdlr in self.handlers:
                    hdlr.emit(record)

    def debug(self, msg, *args):
        self.log(DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(INFO, msg, *args)

    def warning(self, msg, *args):
        self.log(WARNING, msg, *args)

    def error(self, msg, *args):
        self.log(ERROR, msg, *args)

    def critical(self, msg, *args):
        self.log(CRITICAL, msg, *args)

    def exc(self, e, msg, *args):
        buf = uio.StringIO()
        sys.print_exception(e, buf)
        self.log(ERROR, msg + "\n" + buf.getvalue(), *args)

    def exception(self, msg, *args):
        self.exc(sys.exc_info()[1], msg, *args)

    def addHandler(self, hdlr):
        if self.handlers is None:
            self.handlers = []
        self.handlers.append(hdlr)


class Handler:
    def __init__(self):
        self.formatter = Formatter()

    def setFormatter(self, fmt):
        self.formatter = fmt

    def close(self):
        pass

class StreamHandler(Handler):
    def __init__(self, stream=None, level=NOTSET, formatter=None):
        self._stream = stream or sys.stderr
        self.terminator = "\n"
        self.formatter = formatter
        self.level = level

    def emit(self, record):
        if record.levelno >= self.level:
            self._stream.write(self.formatter.format(record) + self.terminator)

    def flush(self):
        pass

class FileHandler(Handler):
    def __init__(self, filename, mode="a", encoding=None, delay=False, level=NOTSET, formatter=None):
        super().__init__()
        self.encoding = encoding
        self.mode = mode
        self.delay = delay
        self.terminator = "\n"
        self.filename = filename
        self.level = level
        self.formatter = formatter

        self._f = None
        if not delay:
            self._f = open(self.filename, self.mode)

    def emit(self, record):
        if record.levelno >= self.level:
            if self._f is None:
                self._f = open(self.filename, self.mode)

            self._f.write(self.formatter.format(record) + self.terminator)

    def close(self):
        if self._f is not None:
            self._f.close()
            self._f = None


class Formatter:
    converter = utime.localtime

    def __init__(self, fmt=None, datefmt=None, style="{"):
        self.fmt = fmt or "{asctime}: {levelname} - {message}"
        self.datefmt = datefmt

        if style not in ("%", "{"):
            raise ValueError("Style must be one of: %, {")

        self.style = style

    def usesTime(self):
        if self.style == "%":
            return "%(asctime)" in self.fmt
        elif self.style == "{":
            return "{asctime" in self.fmt

    def format(self, record):
        # The message attribute of the record is computed using msg % args.
        record.message = record.msg.format(*record.args)

        # If the formatting string contains '(asctime)', formatTime() is called to
        # format the event time.
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        return self.fmt.format(**record.__dict__)

        # If there is exception information, it is formatted using formatException()
        # and appended to the message. The formatted exception information is cached
        # in attribute exc_text.
        if record.exc_info is not None:
            record.exc_text += self.formatException(record.exc_info)
            record.message += "\n" + record.exc_text

        # The record’s attribute dictionary is used as the operand to a string
        # formatting operation.
        if self.style == "%":
            return self.fmt % record.__dict__
        elif self.style == "{":
            return self.fmt.format(**record.__dict__)
        else:
            raise ValueError(
                "Style {0} is not supported by logging.".format(self.style)
            )

    def formatTime(self, record, datefmt=None):
        assert datefmt is None  # datefmt is not supported
        ct = utime.localtime(record.created)
        return "{0}-{1:0>2d}-{2:0>2d} {3:0>2d}:{4:0>2d}:{5:0>2d}".format(*ct)

    def formatException(self, exc_info):
        return exc_info.__str__

class LogRecord:
    def __init__(
        self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None
    ):
        ct = utime.time()
        self.created = ct
        self.msecs = (ct - int(ct)) * 1000
        self.name = name
        self.levelno = level
        self.levelname = _level_dict.get(level, None)
        self.pathname = pathname
        self.lineno = lineno
        self.msg = msg
        self.args = args
        self.exc_info = exc_info
        self.func = func
        self.sinfo = sinfo
