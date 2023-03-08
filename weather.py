from runLoop import Operation, Events, EventArgs
from config import Config
from machine import Pin
from dht import DHT22

class WeatherLogger(Operation):
    def __init__(self, logger):
        super().__init__("weatherLogger", scheduled=False)
        self.logger = logger

    def handleEvent(self, runLoop, event, args):
        if event is Events.WEATHER_READING:
            temperature = args[EventArgs.TEMPERATURE]
            humidity = args[EventArgs.HUMIDITY]
            measuredAt = args[EventArgs.MEASURED_AT]
            self.logWeather(temperature, humidity, measuredAt)

    def logWeather(self, temperature, humidity, measuredAt):
        if measuredAt != None:
            timestring="%04d-%02d-%02d %02d:%02d:%02d"%(measuredAt[0:3] + measuredAt[4:7])
            self.logger.info("Time: {} Temperature: {:.2f}°C Humidity: {:.2f}%", timestring, temperature, humidity)
        else:
            self.logger.info("Time: unknown Temperature: {:.2f}°C Humidity: {:.2f}%", temperature, humidity)

class WeatherChecker(Operation):
    logger = None
    sensor = None
    temperature = None
    humidity = None
    rtc = None

    def __init__(self, logger):
        super().__init__("weatherChecker", scheduled=True, tickIntervalMs=15000)
        self.logger = logger

    def execute(self, runLoop):
        self.measure(runLoop)

    def handleEvent(self, runLoop, event, args):
        if event is Events.UPDATE_TIME:
            self.rtc = args[EventArgs.TIME]

    def measure(self, runLoop):
        self.logger.info("measureWeather")
        try:
            self.sensor = DHT22(Pin(Config.GPIO_PIN_DHT_22_DATA))
            self.sensor.measure()
            self.temperature = self.sensor.temperature()
            self.humidity = self.sensor.humidity()
            # if self.rtc != None:
                # self.lastMeasurement = self.rtc.datetime()
            args = {
                EventArgs.TEMPERATURE: self.temperature,
                EventArgs.HUMIDITY: self.humidity
                }
            if self.rtc is not None:
                args[EventArgs.MEASURED_AT] = self.rtc.datetime()
            runLoop.fireEvent(Events.WEATHER_READING, args)

            metric_args = [("tmp", self.temperature), ("hum", self.humidity)]
            runLoop.fireEvent(Events.POST_METRICS, {EventArgs.METRICS: metric_args})
        except Exception as error:
            self.logger.exc(error, "Weather error")