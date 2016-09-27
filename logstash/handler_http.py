import json
import logging
from logstash import formatter


# Derive from object to force a new-style class and thus allow super() to work
# on Python 2.6
class HTTPLogstashHandler(logging.Handler, object):
    """
    Python logging handler for Logstash. Sends events over HTTP.
    :param url: The url of the logstash server API endpoint.
    :param api_key: The logstash api authorization key.
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def __init__(self, url, api_key, message_type='logstash', tags=None, fqdn=False, version=0):
        super(HTTPLogstashHandler, self).__init__()
        self.url = url
        self.api_key = api_key
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, tags, fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, tags, fqdn)

    def emit(self, record):
        """
        Emit a record.
        POST the record to the logstash server API endpoint as JSON data.
        """
        try:
            import requests

            headers = {'ApiKey': api_key, 'Content-type': 'application/json'}
            data = json.dumps(record.__dict__)

            r = requests.post(self.url, data=data, headers=headers)
        except Exception:
            self.handleError(record)
