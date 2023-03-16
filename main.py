from runLoop import RunLoop, CallbackOperation
from screen import Screen
from font import Orientation
from timeManager import TimeManager
from logManager import LogManager
from picoNetworkManager import PicoNetworkManager
from metricsUploader import MetricsUploader
from weather import WeatherChecker, WeatherLogger
from esp8266 import ESP8266
from config import Config

class Application:
    runLoop = None
    networkManager = None

    def __init__(self):
        self.logManager = LogManager()
        self.logger = self.logManager.logger
        #self.led = machine.Pin(25, Pin.OUT)
        self.networkManager = self.createNetworkManager(self.logger)
        self.runLoop = RunLoop(1000, logger=self.logger)
        self.runLoop.add(self.logManager)
        self.runLoop.add(CallbackOperation("wifi", 15000, self.checkWifi))
        self.runLoop.add(Screen(logger=self.logger, orientation=Orientation.PORTRAIT))
        self.runLoop.add(TimeManager(self.networkManager, self.logger))
        self.runLoop.add(MetricsUploader(self.logger, self.networkManager))
        self.runLoop.add(WeatherLogger(self.logger))
        self.runLoop.add(WeatherChecker(self.logger))

    def createNetworkManager(self, logger):
        if Config.NETWORK_CHIP == "pico":
            return PicoNetworkManager(logger)
        elif Config.NETWORK_CHIP == "esp":
            return ESP8266(logger)

    def start(self):
        try:
            self.runLoop.start()
        except Exception as error:
            self.logger.exc(error, "Application exception")
            raise error

    def checkWifi(self, runLoop):
        self.networkManager.connect(Config.WIFI_SSID, Config.WIFI_PASSWORD)
        status = self.networkManager.wifiStatus()

Application().start()
