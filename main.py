from machine import Pin, RTC, UART
from dht import DHT22
from esp8266 import ESP8266, ESP8266Timeout
from dateTimeParser import ISO8601StringParser
from runLoop import RunLoop
from screen import Screen
from logManager import LogManager
import time, sys, os, logger

WIFI_SSID = ""
WIFI_PASSWORD = ""

TIME_SERVER = "192.168.50.31"
TIME_PORT = "80"
TIME_PATH = "/time.php"

INFLUX_SERVER = "192.168.50.31"
INFLUX_PORT = "8086"
INFLUX_USERNAME = ""
INFLUX_PASSWORD = ""
INFLUX_DATABASE = ""

WEATHER_LOCATION = "test"

ERROR_WIFI = "WIFI ERR"
ERROR_GATEWAY = "GTW ERR"

TIME_STATUS_UNSET = 0
TIME_STATUS_SET = 1
TIME_STATUS_ERROR = 2

class Application:
    temperature = None
    humidity = None
    lastMeasurement = None
    runLoop = None
    rtc = None
    wifi = 0
    error = None
    timeStatus = TIME_STATUS_UNSET
    sensorPin = None

    def __init__(self, location, sensorPin=2):
        self.sensorPin = sensorPin
        self.location = location
        self.rtc = RTC()
        self.logManager = LogManager()
        self.logger = self.logManager.logger
        #self.led = machine.Pin(25, Pin.OUT)
        self.esp01 = ESP8266(logger=self.logger)
        self.runLoop = RunLoop(1000, logger=self.logger)
        self.screen = Screen()

    def updateScreen(self):
        self.logger.info("updateScreen")
        self.screen.temperature = self.temperature
        self.screen.humidity = self.humidity
        if self.timeStatus is TIME_STATUS_SET:
            self.screen.datetime = self.rtc.datetime()
        self.screen.update()

    def start(self):
        try:
            self.startRunLoop()
        except Exception as error:
            self.logger.exc(error, "Application exception")
            raise error

    def startRunLoop(self):
        self.runLoop.add("logs", 60000, self.purgeLogFiles)
        self.runLoop.add("wifi", 15000, self.checkWifi)
        self.runLoop.add("weather", 15000, self.measureWeather)
        self.runLoop.add("ntp", 10000, self.updateTime)
        self.runLoop.add("display", 5000, self.updateScreen)
        self.runLoop.start()
        self.running = True

    def purgeLogFiles(self):
        self.logManager.purgeLogFiles()

    def checkWifi(self):
        status = self.esp01.wifiStatus()
        if status[0] == ESP8266.WIFI_CONNECTED:
            return
        elif status[0] == ESP8266.WIFI_NO_ACCESS_POINT:
            self.esp01.wifiConnect(WIFI_SSID, WIFI_PASSWORD)

    def updateTime(self):
        result = self.esp01.httpGet(TIME_SERVER, TIME_PATH, port=TIME_PORT)
        if result != None:
            try:
                parser = ISO8601StringParser(result.body)
                self.rtc.datetime(parser.datetime())
                self.timeStatus = TIME_STATUS_SET
                self.updateScreen()
                return True
            except:
                self.timeStatus = TIME_STATUS_ERROR
                return False
        else:
            return False

    def logWeather(self):
        if self.lastMeasurement != None:
            timestring="%04d-%02d-%02d %02d:%02d:%02d"%(self.lastMeasurement[0:3] + self.lastMeasurement[4:7])
            self.logger.info("Time: {} Temperature: {:.2f}°C Humidity: {:.2f}%", timestring, self.temperature, self.humidity)
        else:
            self.logger.info("Time: unknown Temperature: {:.2f}°C Humidity: {:.2f}%", self.temperature, self.humidity)

    def measureWeather(self):
        self.logger.info("measureWeather")
        try:
            self.sensor = DHT22(Pin(self.sensorPin))
            self.sensor.measure()
            self.temperature = self.sensor.temperature()
            self.humidity = self.sensor.humidity()
            if self.rtc != None:
                self.lastMeasurement = self.rtc.datetime()
            self.updateScreen()
            self.postWeather()
            self.logWeather()
        except Exception as error:
            self.logger.exc(error, "Weather error")

    def postWeather(self):
        if (self.temperature == None or self.humidity == None):
            self.logger.info("POST: NO MEASUREMENTS")
            return
        body = "weather,location={},temp={} hum={}".format(self.location, self.temperature, self.humidity)
        self.postMetrics(body)

    def postMetrics(self, body):
        path = "/api/v2/write?u={}&p={}&bucket={}".format(INFLUX_USERNAME, INFLUX_PASSWORD, INFLUX_DATABASE)
        try:
            httpResult = self.esp01.httpPost(INFLUX_SERVER, path, "plain/text", body, port=INFLUX_PORT)
            if httpResult != None:
                self.logger.debug("HTTP Code:", httpResult.code)
        except ESP8266Timeout:
            self.logger.info("RESTART - ESP8266Timeout")
            self.esp01.stop()
            machine.reset()

Application("test").start()
