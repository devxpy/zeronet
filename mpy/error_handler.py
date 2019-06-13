import sys

from utime import sleep

from common import AbstractErrorHandler, log


class MpyErrorHandler(AbstractErrorHandler):
    def handle_error(self, exc: Exception):
        log("\nCrash report:")
        sys.print_exception(exc)
        log("Retrying in %d sec...\n" % self.retry_delay)
        sleep(self.retry_delay)
