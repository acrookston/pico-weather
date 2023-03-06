class Config:
    # WIFI information
    WIFI_SSID = "[WIFI NAME]"
    WIFI_PASSWORD = "[WIFI PASSWORD]"

    # The name this station should be reporting metrics as
    WEATHER_LOCATION = ""

    # Address to the gateway server
    TIME_SERVER = "192.168.1.1"
    TIME_PORT = "80"
    TIME_PATH = "/time.php"

    # Address to the influx server
    # Probably same server as gatewa
    INFLUX_SERVER = "192.168.1.1"
    INFLUX_PORT = "8086"
    INFLUX_USERNAME = ""
    INFLUX_PASSWORD = ""
    INFLUX_DATABASE = ""

    # Not really configs, should be move
    ERROR_WIFI = "WIFI ERR"
    ERROR_GATEWAY = "GTW ERR"

    TIME_STATUS_UNSET = 0
    TIME_STATUS_SET = 1
    TIME_STATUS_ERROR = 2