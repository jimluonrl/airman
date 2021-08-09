import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect(("192.168.80.91", 5002))

    i = 0;
    while True:
      i += 1
      sock.send(b"hi from client")
      if i == 1000:
        print('sent 1000 packets ')
        i = 0
