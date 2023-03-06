class NetworkStatus:
    WIFI_CONNECTED = "WIFI_CONNECTED"
    WIFI_DISCONNECTED = "WIFI_DISCONNECTED"
    WIFI_UNKNOWN = "WIFI_DISCONNECTED"
    WIFI_NO_ACCESS_POINT = "WIFI_NO_ACCESS_POINT"

    status = None
    strength = 0
    ssid = None
    channel = None

    def __init__(self, status=None, strength=None, ssid=None, bssid=None, channel=None):
        self.status = status
        self.strength = strength
        self.ssid = ssid
        self.bssid = bssid
        self.channel = channel

class NetworkResponse:
    text = None
    headers = None

class NetworkManager:
    def connect(self, ssid, password):
        pass

    def wifiStatus(self):
        pass

    def httpPost(self, host, path, content_type, content, user_agent="RPi", port=80):
        pass

    def httpGet(self, host, path, user_agent="RPi", port=80):
        pass

    def stop():
        pass
