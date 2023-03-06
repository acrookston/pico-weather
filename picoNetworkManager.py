import network, urequests
from networkManager import  NetworkManager, NetworkStatus

class PicoNetworkManager(NetworkManager):
    def __init__(self, logger):
        self.logger = logger
        self.start()

    def start(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self, ssid, password):
        self.wlan.connect(ssid, password)

    def wifiStatus(self):
        self.logger.debug("WLAN: {}", self.wlan.isconnected())

    def httpPost(self, host, path, content_type, content, user_agent="RPi", port=80):
        try:
            headers = {
                'Content-Type': content_type,
                'User-Agent': user_agent
                }
            request_url = "http://" + host + ":" + port + path
            self.logger.info("POST: {} Body: {}", request_url, content)
            response = urequests.post(request_url, headers = headers, data = content)
            self.logResponse(response)
            return response
        except Exception as error:
            self.logger.exc(error, "POST error")

    def httpGet(self, host, path, user_agent="RPi", port=80):
        try:
            request_url = "http://" + host + ":" + port + path
            self.logger.info("GET: {}", request_url)
            response = urequests.get(request_url)
            self.logResponse(response)
            return response
        except Exception as error:
            self.logger.exc(error, "GET error")

    def logResponse(self, response):
        if response is None:
            return
        self.logger.debug("Response code: {}, headers: {}, body: {}", response.status_code, response.headers, response.text)

    def stop():
        self.wlan = None

# {'encoding': 'utf-8', 'reason': b'No Content', 'headers': {'Date': 'Thu, 02 Mar 2023 11:35:14 GMT', 'Content-Type': 'application/json', 'Request-Id': '4c6bb5ed-b8ee-11ed-8234-b827eb278810', 'X-Influxdb-Build': 'OSS', 'X-Request-Id': '4c6bb5ed-b8ee-11ed-8234-b827eb278810', 'X-Influxdb-Version': '1.8.10'}, 'status_code': 204, 'raw': <socket state=4 timeout=-1 incoming=0 off=0>, '_cached': None}

