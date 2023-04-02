import time

class Events:
    UPDATE_SCREEN = 0
    WEATHER_READING = 1
    UPDATE_TIME = 2
    POST_METRICS = 3
    BUTTON_PRESSED = 4
    BUTTON_LONG_PRESSED = 5

class EventArgs:
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    TIME = "time"
    MEASURED_AT = "measured_at"
    METRICS = "metrics"

class Operation:
    identifier = None
    lastTickMs = 0
    scheduled = False
    tickIntervalMs = None

    def __init__(self, identifier, scheduled=False, tickIntervalMs=None):
        self.identifier = identifier
        self.scheduled = scheduled
        self.tickIntervalMs = tickIntervalMs

    def execute(self, runLoop):
        pass

    def handleEvent(self, runLoop, event, args=None):
        pass

class CallbackOperation(Operation):
    def __init__(self, identifier, tickIntervalMs, callback):
        super().__init__(identifier, scheduled=True, tickIntervalMs=tickIntervalMs)
        self.callback = callback

    def execute(self, runLoop):
        self.callback(runLoop)

class RunLoop:
    operations = []
    running = False
    sleepIntervalMs = 5000

    def __init__(self, sleepIntervalMs=5000, logger=None):
        self.sleepIntervalMs = sleepIntervalMs
        self.logger = logger

    def add(self, operation):
        self.operations.append(operation)

    def remove(self, operation):
        for ix in range(len(self.operations)):
            if self.operations[ix].identifier is operation.identifier:
                del self.operations[ix]
                return

    def fireEvent(self, event, args=None):
        self.logger.info("Event fired: {}, args: {}", event, args)
        for operation in self.operations:
            try:
                operation.handleEvent(self, event, args=args)
            except Exception as error:
                self.logger.exc(error, "Error handling event {} in {}", event, operation.identifier)


    def runOperations(self):
        for ix in range(len(self.operations)):
            operation = self.operations[ix]
            if operation.scheduled and time.ticks_diff(operation.lastTickMs, time.ticks_ms()) <= 0:
                try:
                    operation.execute(self)
                except Exception as error:
                    self.logger.exc(error, "Error executing operation {}", operation.identifier)
                operation.lastTickMs = time.ticks_add(time.ticks_ms(), operation.tickIntervalMs)

    def start(self):
        self.running = True
        while self.running:
            tickStart = time.ticks_ms()
            self.runOperations()
            executionTime = time.ticks_diff(time.ticks_ms(), tickStart)
            sleepMs = self.sleepIntervalMs - executionTime
            self.logger.debug("RunLoop sleep/interval/delta/start ms: {}, {}, {}, {}", sleepMs, self.sleepIntervalMs, executionTime, tickStart)
            if sleepMs < 10:
                sleepMs = 10
            time.sleep_ms(sleepMs)

    def stop(self):
        self.running = False