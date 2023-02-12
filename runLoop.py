import time

class RunLoop:
    operations = []
    running = False
    sleepIntervalMs = 5000

    def __init__(self, sleepIntervalMs=5000, logger=None):
        self.sleepIntervalMs = sleepIntervalMs
        self.logger = logger

    def add(self, identifier, tickIntervalMs, callback):
        self.operations.append([identifier, 0, tickIntervalMs, callback])

    def remove(self, identifer):
        for ix in range(len(self.operations)):
            if self.timers[ix][0] == identifier:
                del self.timers[ix]
                return

    def runOperations(self):
        for ix in range(len(self.operations)):
            operation = self.operations[ix]
            if time.ticks_diff(operation[1], time.ticks_ms()) <= 0:
                operation[3]()
                operation[1] = time.ticks_add(time.ticks_ms(), operation[2])
                self.operations[ix] = operation

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
