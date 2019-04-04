import signal
import socket
import sys

from pyserver import move_bot


def sigint_handler(signum, frame):
    move_bot(0, 0)
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 50001))
s.listen(1)

if __name__ == '__main__':
    while True:
        conn, addr = s.accept()
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                pwm = str(data).split(":")
                lpwm, rpwm = pwm[0],pwm[1]
                move_bot(int(lpwm),int(rpwm))
        except Exception as e:
            print e
            pass
        finally:
            conn.close()
