import socket
import codecs


def send_message(sock, message):
    sock.sendall(
        b"%s%s%s" % (b"\x01", len(message).to_bytes(4, byteorder="big"), message)
    )


def receive_message(sock):
    type_header = recv_all(sock, 1)
    length_header = recv_all(sock, 4)
    #length = int.from_bytes(length_header, byteorder="big")
    length = int(codecs.encode(length_header, 'hex'), 16)
    msg = recv_all(sock, length)

    return msg


def recv_all(sock, n):
    """
        Receive until n bytes are fully received.
    """

    buffer = bytearray()

    while len(buffer) < n:
        r = sock.recv(n - len(buffer))

        if r == b"":
            raise BrokenPipeError("Peer has closed the connection")

        buffer += r

    return buffer
