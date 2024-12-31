# Copy this file to config.py and enter the values
class Config:
    # WIFI information
    WIFI_SSID = "[WIFI NAME]"
    WIFI_PASSWORD = "[WIFI PASSWORD]"

    # Enable if you have a screen connected
    ENABLE_SCREEN = True
    # Enable to auto-sleep the screen and after how long
    ENABLE_SCREEN_SLEEP = True
    SCREEN_SLEEP_TIMEOUT_MS = 5000
    # Enable if you have a button connected, to wake/sleep the screen.
    ENABLE_BUTTON = True
    # Enable if you have an IR sensor to wake the screen, and if input is reversed (some sensors)
    ENABLE_IR_SENSOR = True
    IR_SENSOR_REVERSE_INPUT = False

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
    GPIO_PIN_IR_SENSOR = 20

    DISPLAY_WIDTH  = 128
    DISPLAY_HEIGHT = 64

    # Which network chip you are using?
    # "pico" for a Pico W (recommended)
    # "esp" for an ESP01 (ESP8266). Support for ESP01 is buggy and not really worth it.
    NETWORK_CHIP = "pico"
