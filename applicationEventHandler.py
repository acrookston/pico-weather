from runLoop import Events, Operation
import machine

class ApplicationEventHandler(Operation):
    def __init__(self, logger):
        super().__init__("applicationEventHandler", False)
        self.logger = logger

    def handleEvent(self, runLoop, event, args):
        if event is Events.BUTTON_LONG_PRESSED:
            self.logger.warning("MACHINE RESET FROM BUTTON LONG PRESS")
            machine.reset()