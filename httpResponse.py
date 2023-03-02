from networkManager import NetworkResponse

class HttpResponse(NetworkResponse):
    status_code = None
    headers = None
    text = None
    response = None
    contentLength = None
    __rawData = None
    
    def __init__(self, result):
        self.__rawData = result
        self.__parse()

    def __parse(self):
        if (self.__rawData != None):
            # Split HTTP data into Headers and Body
            sections = self.__rawData.split("\r\n\r\n")
            self.headers = sections[0].split("\r\n")

            if len(sections) > 1:
                self.text = sections[1]

            for header in self.headers:
                if "Transfer-Encoding: chunked" in header:
                    parseChunkedBody(self.text)

            # Get the response code from first header
            for code in self.headers[0].split():
                if code.isdigit():
                    self.status_code = int(code)

    def parseChunkedBody(self):
        pass
        

# Example no content response:
#
# +IPD,249:HTTP/1.1 204 No Content
# Content-Type: application/json
# Request-Id: d71618d0-97eb-11ed-801e-b827eb278810
# X-Influxdb-Error: unable to parse 'temp,location=test temp=1 hum=2': bad timestamp
# Date: Thu, 19 Jan 2023 11:24:30 GMT

# Example bad request:
#
# +IPD,431:HTTP/1.1 400 Bad Request
# Content-Type: application/json
# Request-Id: 3c790810-97eb-11ed-8015-b827eb278810
# X-Influxdb-Build: OSS
# X-Influxdb-Error: unable to parse 'temp,location=test temp=1 hum=2': bad timestamp
# X-Influxdb-Version: 1.8.10
# X-Request-Id: 3c790810-97eb-11ed-8015-b827eb278810
# Date: Thu, 19 Jan 2023 11:20:10 GMT
# Content-Length: 77
#
# {"error":"unable to parse 'temp,location=test temp=1 hum=2': bad timestamp"}

# Example: chunked GET /time.php
# 
# +IPD,206:HTTP/1.1 200 OK
# Server: nginx/1.18.0
# Date: Sun, 22 Jan 2023 13:31:03 GMT
# Content-Type: text/html; charset=UTF-8
# Transfer-Encoding: chunked
# Connection: keep-alive
# 
# 19
# 2023-01-22T14:31:03+01:00
# 0

# Example: GET /time.php
# 
# 1 200 OK
# Server: nginx/1.18.0
# Date: Sun, 22 Jan 2023 13:55:06 GMT
# Content-Type: text/plain; charset=UTF-8
# Content-Length: 25
# Connection: keep-alive
# 
# 2023-01-22T14:55:06+01:00
