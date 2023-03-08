from runLoop import Operation, Events, EventArgs
from config import Config

class MetricsUploader(Operation):
    logger = None
    networkManager = None

    def __init__(self, logger, networkManager):
        super().__init__("metricsUploader", scheduled=False)
        self.logger = logger
        self.networkManager = networkManager

    def handleEvent(self, runLoop, event, args):
        if event is Events.POST_METRICS:
            self.postMetrics(args[EventArgs.METRICS])

    def postMetrics(self, metrics):
        # Metrics format: [(key, value), (key, value)]
        def join_key_value(tuple):
            return "=".join(map(str, tuple))
        values = " ".join(list(map(join_key_value, metrics)))
        body = "weather,location={},{}".format(Config.WEATHER_LOCATION, values)

        path = "/api/v2/write?u={}&p={}&bucket={}".format(Config.INFLUX_USERNAME,
                                                          Config.INFLUX_PASSWORD,
                                                          Config.INFLUX_DATABASE)
        try:
            httpResult = self.networkManager.httpPost(Config.INFLUX_SERVER,
                                                      path,
                                                      "plain/text",
                                                      body,
                                                      port=Config.INFLUX_PORT)
            if httpResult != None:
                self.logger.debug("HTTP Code:", httpResult.status_code)
        except Exception as error:
            self.logger.exc(error, "Post metrics error")
