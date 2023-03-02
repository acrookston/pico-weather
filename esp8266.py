import re, time
from machine import UART, Pin
from httpResponse import HttpResponse
from removeNonAscii import RemoveNonAscii
from networkManager import NetworkManager, NetworkStatus, NetworkResponse

class ESP8266Timeout(Exception):
    "ESP8266 Execution Timed Out"
    pass

class ESP8266(NetworkManager):
    # command response codes
    STATUS_OK = "OK\r\n"
    STATUS_ERROR = "ERROR\r\n"
    STATUS_FAIL = "FAIL\r\n"
    STATUS_BUSY = "busy p...\r\n"
    STATUS_ALREADY_CONNECTED = "ALREADY CONNECTED\r\n"

    # wifi connection response codes
    WIFI_CONNECTED = "WIFI CONNECTED\r\n"
    WIFI_GOT_IP = "WIFI GOT IP\r\n"
    WIFI_DISCONNECTED = "WIFI DISCONNECT\r\n"
    WIFI_AP_NOT_FOUND = "WIFI AP NOT FOUND\r\n"
    WIFI_AP_WRONG_PWD = "WIFI AP WRONG PASSWORD\r\n"
    WIFI_NO_ACCESS_POINT = "No AP\r\n"
    WIFI_UNKNOWN = "WIFI UNKNOWN"

    WIFI_MODE_STATION = 1
    WIFI_MODE_ACCESS_POINT = 2
    WIFI_MODE_BOTH = 3

    CIP_STATUS_NO_INIT = 0 # ESP32 station is not initialized.
    CIP_STATUS_NO_WIFI = 1 # ESP32 station is initialized, but not started a Wi-Fi connection yet.
    CIP_STATUS_NO_IP = 2 # ESP32 station is connected to an AP and its IP address is obtained.
    CIP_STATUS_NO_CON = 3 # ESP32 station has created a TCP/SSL transmission.
    CIP_STATUS_DISCONNECTED = 4 # All of the TCP/UDP/SSL connections of the ESP32 station are disconnected.
    CIP_STATUS_NO_AP = 5 # ESP32 station started a Wi-Fi connection, but was not connected to an AP or disconnected from an AP.

    RX_BUFFER = 512

    executeAttempts = 0

    def __init__(self, logger=None, uartPort=0, baudRate=115200, txPin=Pin(0), rxPin=Pin(1), timeout=5, wait=0.2):
        self.uartPort = uartPort
        self.baudRate = baudRate
        self.txPin = txPin
        self.rxPin = rxPin
        self.timeout = timeout
        self.wait = wait
        self.logger = logger
        self.setup()

    def __del__(self):
        self.stop()

    def setup(self):
        self.uart = UART(self.uartPort, baudrate=self.baudRate, tx=self.txPin, rx=self.rxPin, rxbuf=self.RX_BUFFER)
        
    def stop(self):
        self.uart.deinit()
        self.uart = None

    # Private
    def handleUartResponse(self):
        received = bytes()
        incomingData = None
        attempts = (self.timeout / self.wait)
        while True:
            # fetch for as long as there is data to fetch
            while self.uart.any() > 0:
                received += self.uart.read()

            # decode and look for status codes
            if len(received) > 0:
                try:
                    # replace generates less errors than .decode("utf-8")
                    incomingData = str(received)
                    incomingData = incomingData.replace("b'", "")
                    incomingData = incomingData.replace("\\r", "\r")
                    incomingData = incomingData.replace("\\n", "\n")
                    incomingData = incomingData.replace("'", "")
                    incomingData = RemoveNonAscii(incomingData)
                    self.logger.debug("\n--\n{}\n--\n", incomingData)
                except Exception as error:
                    self.logger.exc(error, "Error decoding UART response: {}", received)
                if incomingData != None:
                    if self.STATUS_OK in incomingData:
                        self.logger.debug("STATUS_OK")
                        return incomingData
                    elif self.STATUS_ERROR in incomingData:
                        self.logger.debug("STATUS_ERROR")
                        return incomingData
                    elif self.STATUS_FAIL in incomingData:
                        self.logger.debug("STATUS_FAIL")
                        return incomingData
                    elif self.STATUS_BUSY in incomingData:
                        self.logger.debug("STATUS_BUSY")
                        # ESP still busy, could consider resetting TTL
            self.logger.debug("ESP ATTEMPTS: {}", attempts)
            # count down the attempts until we hit 0
            attempts -= 1
            if attempts <= 0:
                raise ESP8266Timeout
            # wait for next check
            time.sleep(self.wait)
        return incomingData

    # Private
    def execute(self, command, maxRetries=10, attempts=0):
        try:
            response = self.uart.write(command + "\r\n")
            self.logger.debug("AT COMMAND: '{}' WRITE: {}", command, response)
            return self.handleUartResponse()
        except ESP8266Timeout:
            self.stop()
            self.setup()
            attempts += 1
            if attempts > maxRetries:
                self.logger.info("ESP8266Timeout too many attempts")
                raise ESP8266Timeout
            self.logger.info("ESP8266Timeout managed")
            return self.execute(command, maxRetries, attempts)

    def start(self):
        self.execute("AT")
        # Version
        self.execute("AT+GMR")
        # self.execute("AT+CIOBAUD?") # ERROR
        # which mode?
        self.execute('AT+CWMODE?')
        self.execute('ATE1') # Enable command echo
        # wifi state and info
        # self.execute("AT+CWSTATE?") #  ERROR
        # wifi connected?
        self.execute("AT+CWJAP?")
        self.execute("AT+CIFSR")
        self.execute("AT+CIPMUX=0") # enable one tcp/ssl connections
        self.execute("AT+CIPSSLSIZE=2048") # Increase SSL buffer
        self.execute("AT+CIPSTATUS")
        # set STN mode
        #self.execute("AT+CWMODE=1")

    def connectUDP(self, server, port):
        return self.connect("UDP", server, port)

    def connectTCP(self, server, port):
        return self.connect("TCP", server, port)

    def connect(self, protocol, server, port):
        # ERROR: ALREADY CONNECTED
        # ERROR: CLOSED
        # self.execute("AT+CIPSTATE")
        command = 'AT+CIPSTART="' + protocol + '","' + server + '",' + str(port)
        result = self.execute(command)
        if result == None:
            return False
        if self.STATUS_ALREADY_CONNECTED in result:
            self.logger.debug("STATUS_ALREADY_CONNECTED")
            return True
        return self.STATUS_OK in result

    def disconnect(self):
        self.execute("AT+CIPCLOSE")

    def pingChip(self):
        result = self.execute("AT")
        if result == None:
            return False
        return self.STATUS_OK in result

    def listAccessPoints(self):
        self.execute('AT+CWLAP')

    def wifiGetAccessPoints(self):
        self.execute("AT+CWLAP")

    def connect(self, ssid, password):
        self.execute('AT+CWJAP="' + ssid  + '","' + password + '"')

    def wifiDisconnect(self):
        self.execute('AT+CWQAP')

    def wifiStatus(self):
        # Response: +CWJAP:<ssid>,<bssid>,<channel>,<rssi>,<pci_en>,<reconn_interval>,<listen_interval>,<scan_mode>,<pmf>
        # EG: +CWJAP:"WiFi","5c:4c:3b:ac:e4:31",10,-54
        result = self.execute('AT+CWJAP?')
        if result != None and self.WIFI_NO_ACCESS_POINT in result:
            return NetworkStatus(NetworkStatus.WIFI_NO_ACCESS_POINT)
        content = self.getContentForLineStarting(result, "+CWJAP:")
        if content != None:
            wifi = content.split(',')            
            if len(wifi) > 3:
                return NetworkStatus(NetworkStatus.WIFI_CONNECTED,
                                     int(wifi[3]),
                                     wifi[0],
                                     wifi[1].replace('"', ''),
                                     int(wifi[2]))

        return NetworkStatus(NetworkStatus.UNKNOWN)

    def getContentForLineStarting(self, result, start):
        if result == None:
            return None
        lines = result.split("\r\n")
        for line in lines:
            if line.startswith(start):
                parts = line.split(start)
                if len(parts) > 1:
                    return parts[1]
                else:
                    return None
        return None

    def parseResponse(self, header, content):
        # Grab the data from response (remove "IPD:{length}:")
        ipdData = re.compile(header + ":").split(content)
        if len(ipdData) < 2:
            return None
        return HttpResponse(ipdData[1])

    def getVersion(self):
        self.execute('AT+GMR')
        
    def httpPost(self, host, path, content_type, content, user_agent="RPi", port=80):
        request = "POST " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "User-Agent: " + user_agent + "\r\n" + "Content-Type: " + content_type + "\r\n" + "Content-Length: " + str(len(content)) + "\r\n" + "\r\n" + content + "\r\n"
        return self.tcpSipSend(host, port, request)

    def httpGet(self, host, path, user_agent="RPi", port=80):
        request = "GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "User-Agent: " + user_agent + "\r\n" + "\r\n"
        return self.tcpSipSend(host, port, request)

    def tcpSipSend(self, host, port, request):
        if (self.connect("TCP", host, port) == True):
            self.logger.debug("TCP SIPSEND: {}", request)
            command = "AT+CIPSEND=" + str(len(request))
            result = self.execute(command)
            if result != None:
                if ">" in result:
                    response = self.execute(request)
                    self.disconnect()
                    if response != None:
                        # Grab the data from response (remove "IPD,{length}:")
                        ipdData = re.compile("\+IPD,\d+:").split(response)
                        if len(ipdData) < 2:
                            return None
                        return HttpResponse(ipdData[1])
            self.disconnect()
            return None
        return None
