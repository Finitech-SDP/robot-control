import logging
import socket
import time


def retry(on_fail_message, tries=10, initial_delay=1, multiplier=2):
    """ Retries a function until it returns True. """

    def retry_decorator(func):
        def func_retry(*args, **kwargs):
            remaining_tries, delay = tries, initial_delay

            rv = func(*args, **kwargs)

            if rv is False:
                logging.warning("%s. Retrying in %ss", on_fail_message, delay)

            while remaining_tries > 0:
                if rv is True:
                    return True

                remaining_tries -= 1
                time.sleep(delay)

                delay *= multiplier

                rv = func(*args, **kwargs)

                if rv is False:
                    logging.warning("%s. Retrying in %ss", on_fail_message, delay)

            return False

        return func_retry

    return retry_decorator


def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.connect(("10.255.255.255", 1))  # we don't care about reachability

            return sock.getsockname()[0]
        except socket.error:
            return ""
