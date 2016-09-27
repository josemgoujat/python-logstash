import json
import logging
from logstash import formatter


# Derive from object to force a new-style class and thus allow super() to work
# on Python 2.6
class HTTPLogstashHandler(logging.Handler, object):
    """
    Python logging handler for Logstash. Sends events over HTTP.
    :param host: The host of the logstash server.
    :param api_key: The logstash api authorization key.
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def __init__(self, host, api_key, message_type='logstash', tags=None, fqdn=False, version=0):
        super(HTTPLogstashHandler, self).__init__()
        self.host = host
        self.api_key = api_key
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, tags, fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, tags, fqdn)

    def emit(self, record):
        """
        Emit a record.
        POST the record to the logstash server as JSON data.
        """
        try:
            import httplib

            h = httplib.HTTPConnection(self.host)
            data = json.dumps(record.__dict__)

            h.putrequest('POST', '/')
            h.putheader("Host", self.host)
            h.putheader("Content-type", "application/json")
            h.putheader("ApiKey", self.api_key)
            h.endheaders()

            h.send(data.encode('utf-8'))
            h.getresponse()    #can't do anything with the result
        except Exception:
            self.handleError(record)
