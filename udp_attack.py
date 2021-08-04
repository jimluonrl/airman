import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect(("192.168.80.90", 5002))

    sock.send(b"hi from client")
    print(sock.recvfrom(8192))
