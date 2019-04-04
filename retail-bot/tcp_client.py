import getch
import socket
import sys
from threading import Thread
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.254.2', 50000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

left, right, direction = 0, 0, 1


def decay():
    global left, right
    while True:
        left = max(0, left - 1)
        right = max(0, right - 1)
        sleep(0.001)
Thread(target=decay).start()

try:
    i = 0
    while True:
        key = ord(getch.getch())
        if key == 27:  # ESC
            break
        elif key == 224:  # Special keys (arrows, f keys, ins, del, etc.)
            key = ord(getch.getch())
            if key == 72:  # Up arrow
                left += 1
                right += 1
            elif key == 80:  # Down arrow
                left -= 1
                right -= 1

        sock.sendall(str(left)+":"+str(right).encode('utf-8'))
        i+=1
        i%=100
        sleep(0.1)
finally:
    sock.close()
