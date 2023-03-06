import time

class Operation:
    identifier = None
    lastTickMs = 0
    tickIntervalMs = None

    def __init__(self, identifier, tickIntervalMs):
        self.identifier = identifier
        self.tickIntervalMs = tickIntervalMs

    def execute(self):
        pass

class CallbackOperation(Operation):
    def __init__(self, identifier, tickIntervalMs, callback):
        super().__init__(identifier, tickIntervalMs)
        self.callback = callback

    def execute(self):
        self.callback()

class RunLoop:
    operations = []
    running = False
    sleepIntervalMs = 5000

    def __init__(self, sleepIntervalMs=5000, logger=None):
        self.sleepIntervalMs = sleepIntervalMs
        self.logger = logger

    def add(self, operation):
        self.operations.append(operation)
        # self.operations.append([identifier, 0, tickIntervalMs, callback])

    def remove(self, operation):
        for ix in range(len(self.operations)):
            if self.operations[ix].identifier == identifier:
                del self.operations[ix]
                return

    def runOperations(self):
        for ix in range(len(self.operations)):
            operation = self.operations[ix]
            if time.ticks_diff(operation.lastTickMs, time.ticks_ms()) <= 0:
                operation.execute()
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
