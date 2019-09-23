from requests.adapters import HTTPAdapter
from requests.packages import PoolManager, HTTPConnectionPool

try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection


class NewAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.soqt = kwargs.pop("soqt")
        super(NewAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, **kwargs):
        self.poolmanager = NewPoolManager(num_pools=connections,
                                          maxsize=maxsize,
                                          soqt=self.soqt, **kwargs)


class NewPoolManager(PoolManager):
    def __init__(self, *args, **kwargs):
        self.soqt = kwargs.pop("soqt")
        super(NewPoolManager, self).__init__(*args, **kwargs)

    def _new_pool(self, scheme, host, port, soqt=None, **kwargs):
        return NewHTTPConnectionPool(host, port, soqt=self.soqt, **self.connection_pool_kw)


class NewHTTPConnectionPool(HTTPConnectionPool):
    def __init__(self, *args, **kwargs):
        self.soqt = kwargs.pop("soqt")
        super(NewHTTPConnectionPool, self).__init__(*args, **kwargs)

    def _new_conn(self):
        self.num_connections += 1
        return NewHTTPConnection(host=self.host,
                                 port=self.port,
                                 strict=self.strict,
                                 soqt=self.soqt)


class NewHTTPConnection(HTTPConnection):
    def __init__(self, *args, **kwargs):
        self.soqt = kwargs.pop("soqt")
        HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        """Connect to the host and port specified in __init__."""
        print "Connecting with custom socket"
        self.sock = self.soqt
        self.sock.connect((self.host, self.port))
        if self._tunnel_host:
            self._tunnel()
