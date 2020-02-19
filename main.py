import logging
import socket
import sys
import traceback
from Queue import Queue
from threading import Thread
from time import sleep

from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from control import decoder, movement
from protocol import protocol
from motors import Motors
import config

MC = Motors()
MESSAGE_QUEUE = Queue(maxsize=config.CONTROL_QUEUE_SIZE)
sonic = GroveUltrasonicRanger(5)


def stop_command():
    movement.setTime(0)
    movement.stop()


def cli():
    while True:

        command = raw_input(">")

        if command == "STOP":  # Kill-switch
            stop_command()
            clear_queue()
        else:
            MESSAGE_QUEUE.put_nowait(command)


def server():
    try:
        port = sys.argv[2] if sys.argv[2]!=None else config.TCP_PORT
        port = int(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((config.TCP_HOST, port))
        print("bind success")
        s.listen(1)
        print("waiting for connection")
        logging.info(
            "Listening on %s:%d, use ctrl+c to stop",
            config.TCP_HOST,
            config.TCP_PORT,
        )
        sock, addr = s.accept()
        # Disable TCP buffering
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        while True:
            #movement.exit_if_motors_not_connected()

            try:
                msg = protocol.receive_message(sock).decode("ascii")

                if msg == "STOP":  # Kill-switch
                    stop_command()
                    clear_queue()

                else:
                    MESSAGE_QUEUE.put_nowait(msg)
            except:
                print("Peer closed the connection")
                break
        sock.close()

    except Exception as e:
        logging.error("Server error: %s", str(e))
        traceback.print_exc()
    finally:
        s.close()


def sonicsensor():
    while True:
        sleep(0.10)
        if sonic.get_distance()<5:
            stop_command()
            print(sonic.get_distance())
            while(sonic.get_distance()<10):
                continue
            decoder.redo()

            
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
    print("queue clear")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        producer = server
        print("server mode")
    else:
        producer = cli
        
    sonic_thread = Thread(target=sonicsensor)
    consumer_thread = Thread(target=consumer)
    producer_thread = Thread(target=producer)

    try:
        producer_thread.start()
        consumer_thread.start()
        sonic_thread.start()
        producer_thread.join()
        sonic_thread.join()
    except (KeyboardInterrupt,SystemExit):
        print("exit")
    # TODO: handle keyboard interrupts
    



if __name__ == "__main__":
    main()