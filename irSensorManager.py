from runLoop import Events, EventArgs, Operation
from config import Config
from machine import Pin
import time

class IRSensorManager(Operation):
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
        super().__init__("irSensorManager", True, 1000)
        self.logger = logger
        self.pin = Pin(Config.GPIO_PIN_IR_SENSOR, mode=Pin.IN)
        self.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.interruptionHandler)
        self.sense = self.pin.value()
        self.state = self.rawstate()

    def interruptionHandler(self, pin):
        state = self.rawstate()
        if self.runLoop is not None and state and not self.state:
            self.logger.debug("SENSOR TRIGGERED {}/{}", self.pin.value(), self.rawstate())
            self.runLoop.fireEvent(Events.IR_SENSOR_TRIGGERED)
        self.state = state

    # Current non-debounced logical input state: True == detection, even if input is reversed.
    def rawstate(self):
        if Config.IR_SENSOR_REVERSE_INPUT:
            return not bool(self.pin.value() ^ self.sense)
        else:
            return bool(self.pin.value() ^ self.sense)

    def execute(self, runLoop):
        self.runLoop = runLoop

    def handleEvent(self, runLoop, event, args):
        pass