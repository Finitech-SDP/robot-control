import logging
import socket
import sys
import traceback
from Queue import Queue
from threading import Thread

import config
from control import decoder, movement
from protocol import protocol
from motors import Motors


MC = Motors()
MESSAGE_QUEUE = Queue(maxsize=config.CONTROL_QUEUE_SIZE)

 
def cli():
    while True:

        command = raw_input(">")

        if command == "STOP":  # Kill-switch
            movement.setTime(0)
            clear_queue()
        else:
            MESSAGE_QUEUE.put_nowait(command)


def server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((config.TCP_HOST, config.TCP_PORT))
            s.listen(1)
            logging.info(
                "Listening on %s:%d, use ctrl+c to stop",
                config.TCP_HOST,
                config.TCP_PORT,
            )
            sock, addr = s.accept()

            # Disable TCP buffering
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            with sock:
                while True:
                    #movement.exit_if_motors_not_connected()

                    try:
                        msg = protocol.receive_message(sock).decode("ascii")

                        if msg == "STOP":  # Kill-switch
                            MC.stop_motors()
                        else:
                            MESSAGE_QUEUE.put_nowait(msg)
                    except BrokenPipeError:
                        print("Peer closed the connection")
                        break
    except Exception as e:
        logging.error("Server error: %s", str(e))
        traceback.print_exc()


def consumer():
    while True:
        try:
            msg = MESSAGE_QUEUE.get()
            decoder.parse_command(msg)
        except Exception as e:
            logging.error("Consumer error: %s", str(e))
            traceback.print_exc()
        finally:
            MESSAGE_QUEUE.task_done()


def clear_queue():
    while not MESSAGE_QUEUE.empty():
        MESSAGE_QUEUE.get_nowait()
        MESSAGE_QUEUE.task_done()

def main():
    '''if len(sys.argv) > 1 and sys.argv[1] == "server":
        producer = server
    else:'''
    producer = cli

    producer_thread = Thread(target=producer)
    consumer_thread = Thread(target=consumer)
    try:
        producer_thread.start()
        consumer_thread.start()
        producer_thread.join()
        consumer_thread.setDaemon(True)
    except (KeyboardInterrupt,SystemExit):
        print("exit")
    # TODO: handle keyboard interrupts
    



if __name__ == "__main__":
    main()