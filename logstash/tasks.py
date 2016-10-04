class HTTPEmitTask(object):
    """
    POST the record to the logstash server API endpoint as JSON data.
    """
    queue = "Logstash"
    retry_every = 5
    
    @staticmethod
    def perform(url, data, headers):
        try:
            import requests
            r = requests.post(url, data=data, headers=headers)
        except Exception:
            print "Couldn't send the record to the logstash server."
