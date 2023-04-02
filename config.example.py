# Copy this file to config.py and enter the values
class Config:
    # WIFI information
    WIFI_SSID = "[WIFI NAME]"
    WIFI_PASSWORD = "[WIFI PASSWORD]"

    # Enable if you have a screen connected
    ENABLE_SCREEN = True
    # Enable if you have a button connected
    ENABLE_BUTTON = True

    # The name this station should be reporting metrics as
    WEATHER_LOCATION = ""

    # Address to the gateway server
    TIME_SERVER = "192.168.1.1"
    TIME_PORT = "80"
    TIME_PATH = "/time.php"

    # Address to the influx server
    # Probably same server as gateway
    INFLUX_SERVER = "192.168.1.1"
    INFLUX_PORT = "8086"
    INFLUX_USERNAME = ""
    INFLUX_PASSWORD = ""
    INFLUX_DATABASE = ""

    # Hardware settings:
    GPIO_PIN_DHT_22_DATA = 2
    GPIO_PIN_DISPLAY_SDA = 4
    GPIO_PIN_DISPLAY_SCL = 5
    GPIO_PIN_BUTTON = 22

    DISPLAY_WIDTH  = 128
    DISPLAY_HEIGHT = 64

    # Which network chip you are using?
    # "pico" for a Pico W (recommended)
    # "esp" for an ESP01 (ESP8266). Support for ESP01 is buggy and not really worth it.
    NETWORK_CHIP = "pico"

    # Not really configs, should be moved
    ERROR_WIFI = "WIFI ERR"
    ERROR_GATEWAY = "GTW ERR"