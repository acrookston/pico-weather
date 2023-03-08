from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from font import FontWriter
from runLoop import Operation, Events, EventArgs

DISPLAY_WIDTH  = 128
DISPLAY_HEIGHT = 64
DISPLAY_SCL = 5
DISPLAY_SDA = 4

class ViewModel:
    datetime = None
    temperature = None
    humidity = None
    error = None

class Screen(Operation):
    logger = None

    def __init__(self, logger):
        super().__init__("screen", scheduled=True, tickIntervalMs=5000)
        self.i2c = I2C(0, scl=Pin(DISPLAY_SCL), sda=Pin(DISPLAY_SDA), freq=200000)
        self.display = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, self.i2c)
        self.display.contrast(0x00)
        self.fontWriter = FontWriter(self.display)

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

    def update(self):
        self.logger.debug("Update Screen with model: {}", self.model)

        self.display.fill(0)

        if self.model.datetime != None:
            timestring = str("%02d:%02d" %  (self.model.datetime[4:6]))
            self.fontWriter.write(timestring, 20, 2, 6)

        if self.model.temperature != None:
            temperatureText = str("{:0.1f}".format(self.model.temperature) + "°")
            self.fontWriter.write(temperatureText, 12, 80, 2)

        if self.model.humidity != None:
            humidityText = str("{:0.1f}".format(self.model.humidity) + "%")
            self.fontWriter.write(humidityText, 12, 80, 18)

        self.display.show()
