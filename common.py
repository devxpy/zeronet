LOG_PREFIX = "[μNetwork] "
BCAST_HOST = "255.255.255.255"
LOCAL_HOST = "0.0.0.0"


def log(*args, **kwargs):
    print(LOG_PREFIX, *args, **kwargs)


class AbstractErrorHandler:
    def __init__(self, *, retry_for: tuple = (), retry_delay: float = 5):
        self.retry_for = retry_for
        self.retry_delay = retry_delay

    def handle_error(self, exc: Exception):
        ...

    def __enter__(self):
        pass

    def __exit__(self, e, *args, **kwargs):
        if e in self.retry_for:
            self.handle_error(e)
            return True


class AbstractNetworkMan:
    _error_handler = AbstractErrorHandler()

    def __init__(
        self,
        *,
        ap_ssid: str = None,
        ap_password: str = None,
        sta_ssid: str = None,
        sta_password: str = None
    ):
        self.ap_ssid = ap_ssid
        self.ap_password = ap_password
        self.sta_ssid = sta_ssid
        self.sta_password = sta_password

    @property
    def connected(self) -> bool:
        ...

    def configure(self):
        ...

    def connect(self):
        ...

    def wait(self, *, max_tries=None, refresh_freq_hz=1):
        ...

    def disconnect(self):
        ...

    def get_bind_addrs(self) -> list:
        ...
