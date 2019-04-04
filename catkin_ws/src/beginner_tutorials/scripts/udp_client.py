import socket

pwm = "0:0"

bytesToSend = str.encode(pwm)

serverAddressPort = ("192.168.254.2", 20001)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
i=0
# Send to server using created UDP socket
while(i<100):
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    i+=1