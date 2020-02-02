#! /usr/bin/env python3
import re
import sys
import getopt
import socket

from control import decoder
from control import movement
from protocol import protocol
from time import sleep


def command_line():
    while True:
        if not movement.is_motor_connected():
            print("Motor is not connected properly")
            break
        command = input(">")
        decoder.parse_command(command)


# ./main.py server
def sock():
    port = 4444  # default port is 4444
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print("waiting for connections")
        sock = s.accept()[0]
    finally:
        s.close()

    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    print("connection success! ")
    while True:
        try:
            msg = protocol.receive_message(sock).decode("ascii")  # "F 100 1000"
        except BrokenPipeError:
            break

        while not movement.is_motor_connected():
            print("Motor is not connected properly")
            sleep(10)

        decoder.parse_command(msg)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            sock()
    else:
        command_line()


if __name__ == "__main__":
    main()
