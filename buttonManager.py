from runLoop import Events, EventArgs, Operation
from config import Config
from machine import Pin
import time

class ButtonManager(Operation):
    debounceMS = 50
    longPressMS = 5000

    # Private:
    runLoop = None
    lastTrigger = None
    sense = None
    state = None
    startPressTicks = None
    endPressTicks = None

    def __init__(self, logger):
        super().__init__("buttonManager", True, 60_000)
        self.logger = logger
        self.pin = Pin(Config.GPIO_PIN_BUTTON, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.interruptionHandler)
        self.sense = self.pin.value()
        self.state = self.rawstate()

    def interruptionHandler(self, pin):
        if self.lastTrigger is None:
            self.lastTrigger = time.ticks_ms()
            self.checkState(pin)
        diff = time.ticks_diff(time.ticks_ms(), self.lastTrigger)
        if diff > self.debounceMS:
            self.checkState(pin)

    def checkState(self, pin):
        state = self.rawstate()
        # State has changed: act on it now.
        if state != self.state:
            self.logger.info("BUTTON STATE CHANGED")
            self.state = state
            if state is True:
                # Button is pressed, start measuring
                self.startPressTicks = time.ticks_ms()
                self.endPressTicks = None
            elif state is False:
                # Button is released, stop measuring
                self.endPressTicks = time.ticks_ms()
                totalPressTime = time.ticks_diff(self.endPressTicks, self.startPressTicks)
                self.logger.debug("BUTTON PRESSED MS: {}", totalPressTime)
                if totalPressTime > self.longPressMS:
                    self.runLoop.fireEvent(Events.BUTTON_LONG_PRESSED)
                else:
                    self.runLoop.fireEvent(Events.BUTTON_PRESSED)

    # Current non-debounced logical button state: True == pressed
    def rawstate(self):
        return bool(self.pin.value() ^ self.sense)

    def execute(self, runLoop):
        self.runLoop = runLoop

    def handleEvent(self, runLoop, event, args):
        pass