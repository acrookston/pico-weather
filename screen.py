from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from font import FontWriter

DISPLAY_WIDTH  = 128
DISPLAY_HEIGHT = 64
DISPLAY_SCL = 5
DISPLAY_SDA = 4

class Screen:
    datetime = None
    temperature = None
    humidity = None
    error = None

    def __init__(self):
        self.i2c = I2C(0, scl=Pin(DISPLAY_SCL), sda=Pin(DISPLAY_SDA), freq=200000)
        self.display = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, self.i2c)
        self.display.contrast(0x00)
        self.fontWriter = FontWriter(self.display)

    def update(self):
        self.display.fill(0)

        if self.datetime != None:
            timestring = str("%02d:%02d" %  (self.datetime[4:6]))
            self.fontWriter.write(timestring, 20, 2, 6)

        if self.temperature != None:
            temperatureText = str("{:0.1f}".format(self.temperature) + "°")
            self.fontWriter.write(temperatureText, 12, 80, 2)

        if self.humidity != None:
            humidityText = str("{:0.1f}".format(self.humidity) + "%")
            self.fontWriter.write(humidityText, 12, 80, 18)

        self.display.show()
