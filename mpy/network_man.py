import network
from utime import sleep

from common import AbstractNetworkMan
from common import log


class MpyNetworkMan(AbstractNetworkMan):
    ap = network.WLAN(network.AP_IF)
    sta = network.WLAN(network.STA_IF)

    @property
    def connected(self) -> bool:
        return self.ap.isconnected() or self.sta.isconnected()

    def configure(self):
        if self.ap_ssid is not None:
            self.ap.config(essid=self.ap_ssid, password=self.ap_password)
            self.ap.active(True)
        else:
            self.ap.active(False)

        if self.sta_ssid is not None:
            self.sta.active(True)
            self.sta.scan()
            self.sta.disconnect()
            self.sta.connect(ssid=self.sta_ssid, password=self.sta_password)
        else:
            self.sta.active(False)

    def disconnect(self):
        self.ap.active(False)
        self.sta.active(False)

    def connect(self):
        log(
            "Connecting to network... { ap_ssid: %r, ap_password: %r, sta_ssid: %r, sta_password: %r }"
            % (self.ap_ssid, self.ap_password, self.sta_ssid, self.sta_password)
        )
        while True:
            with self._error_handler:
                self.configure()
                self.wait(max_tries=50)
                log("Connected to network!")
                return
            self.disconnect()

    def wait(self, *, max_tries=None, refresh_freq_hz=1):
        wait_sec = 1 / refresh_freq_hz
        log("Waiting for network...", end="")

        count = 0
        while not self.connected:
            count += 1
            sleep(wait_sec)

            if max_tries is not None and count > max_tries:
                print()
                if not self.connected:
                    raise OSError(
                        "Couldn't establish a connection even after %d tries."
                        % max_tries
                    )
                return
            else:
                print("%d..." % count, end="")

    def get_bind_addrs(self) -> list:
        return [self.ap.ifconfig()[0], self.sta.ifconfig()[0]]
