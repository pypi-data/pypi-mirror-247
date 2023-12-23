import functools
import sys
import httpcore
import httpx

from ivette.utils import print_color


def http_request(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError, httpcore.RemoteProtocolError):
                continue
    return wrapper


def main_process(exit_message):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyboardInterrupt, SystemExit) as e:
                print_color(f"\n{exit_message}", "34")
                sys.exit()
        return wrapper
    return decorator
