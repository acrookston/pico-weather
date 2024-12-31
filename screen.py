from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from font import FontWriter, Orientation
from runLoop import Operation, Events, EventArgs
from config import Config
import time

class ViewModel:
    datetime = None
    temperature = None
    humidity = None
    error = None

class Screen(Operation):
    logger = None
    i2c = None
    display = None
    fontWriter = None
    orientation = Orientation.LANDSCAPE
    displayTurnedOnAt = None

    def __init__(self, logger, orientation=Orientation.LANDSCAPE):
        super().__init__("screen", scheduled=True, tickIntervalMs=5000)
        self.i2c = I2C(0,
                       scl=Pin(Config.GPIO_PIN_DISPLAY_SCL),
                       sda=Pin(Config.GPIO_PIN_DISPLAY_SDA),
                       freq=200000)
        self.display = SSD1306_I2C(Config.DISPLAY_WIDTH,
                                   Config.DISPLAY_HEIGHT,
                                   self.i2c)
        self.displayOn()
        self.display.contrast(0x00)
        self.fontWriter = FontWriter(self.display, orientation)
        self.orientation = orientation

        self.logger = logger
        self.model = ViewModel()

    def execute(self, runLoop):
        self.update()

    def handleEvent(self, runLoop, event, args):
        if event is Events.UPDATE_SCREEN:
            self.update()
        elif event is Events.WEATHER_READING:
            self.model.temperature = args["temperature"]
            self.model.humidity = args["humidity"]
            self.update()
        elif event is Events.UPDATE_TIME:
            self.model.datetime = args[EventArgs.TIME].datetime()
            self.update()
        elif event is Events.IR_SENSOR_TRIGGERED:
            self.displayOn()
        elif event is Events.BUTTON_PRESSED:
            if self.displayTurnedOnAt is not None:
                self.displayOff()
            else:
                self.displayOn()

    def displayOn(self):
        self.display.poweron()
        self.displayTurnedOnAt = time.ticks_ms()

    def displayOff(self):
        self.display.poweroff()
        self.displayTurnedOnAt = None

    def update(self):
        self.logger.debug("Update Screen with model: {}", self.model)

        self.display.fill(0)
        if self.model.datetime != None:
            timestring = str("%02d:%02d" %  (self.model.datetime[4:6]))
            self.fontWriter.write(timestring, 20, 0, 13)

        if self.model.temperature != None:
            temperatureText = str("{:0.1f}".format(self.model.temperature) + "°")
            self.fontWriter.write(temperatureText, 20, 0, 38)

        if self.model.humidity != None:
            humidityText = str("{:0.1f}".format(self.model.humidity) + "%")
            self.fontWriter.write(humidityText, 20, 0, 63)

        self.display.show()

        if Config.ENABLE_SCREEN_SLEEP:
            if self.displayTurnedOnAt is not None:
                screenTime = time.ticks_diff(time.ticks_ms(), self.displayTurnedOnAt)
                self.logger.debug("SCREEN MEASURE: {}", screenTime)
                if screenTime > Config.SCREEN_SLEEP_TIMEOUT_MS:
                    self.displayOff()
