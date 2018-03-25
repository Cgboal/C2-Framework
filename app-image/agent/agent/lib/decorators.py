from urllib3 import PoolManager


class Request(object):

    def __init__(self, host, port="80", ssl="False"):
        self.host = host
        self.port = port
        self.http = PoolManager()
        if ssl == "True":
            self.url = "https://%s:%s" % (self.host, self.port)
        else:
            self.url = "http://%s:%s" % (self.host, self.port)

    def __call__(self, uri, proto='GET', data=None):
        def decorator(callback):
            def wrapper():
                resp = self.http.request(proto, self.url + uri, data).data
                return callback(resp)
            return wrapper
        return decorator
258