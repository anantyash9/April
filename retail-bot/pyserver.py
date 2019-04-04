import signal
import sys

import RPi.GPIO as GPIO
from time import sleep


def sigint_handler(signum, frame):
    move_bot(0, 0)
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)



pwmMotor1 = 12  # PWM pin connected to LED
pwmMotor2 = 32
forwardMotor1 = 11
forwardMotor2 = 21
backwardMotor1 = 19
backwardMotor2 = 13

GPIO.setwarnings(False)  # disable warnings
GPIO.setmode(GPIO.BOARD)  # set pin numbering system
GPIO.setup(pwmMotor1, GPIO.OUT)
lPWM = GPIO.PWM(pwmMotor1, 1000)  # create PWM instance with frequency

GPIO.setup(pwmMotor2, GPIO.OUT)
rPWM = GPIO.PWM(pwmMotor2, 1000)

GPIO.setup(forwardMotor1,GPIO.OUT)
GPIO.setup(forwardMotor2,GPIO.OUT)
GPIO.setup(backwardMotor1,GPIO.OUT)
GPIO.setup(backwardMotor2,GPIO.OUT)

lPWM.start(0)
sleep(0.01)

rPWM.start(0)
sleep(0.01)


def move_bot(lpwm, rpwm):
   if (lpwm < 0):
      GPIO.output(forwardMotor1, GPIO.LOW)  # Turn on
      GPIO.output(backwardMotor1, GPIO.HIGH)  # Turn on

   else:
      GPIO.output(forwardMotor1, GPIO.HIGH)
      GPIO.output(backwardMotor1, GPIO.LOW)

   if (rpwm < 0):
      GPIO.output(forwardMotor2, GPIO.LOW)
      GPIO.output(backwardMotor2, GPIO.HIGH)

   else:
      GPIO.output(forwardMotor2, GPIO.HIGH)
      GPIO.output(backwardMotor2, GPIO.LOW)

   lPWM.ChangeDutyCycle(abs(lpwm))
   rPWM.ChangeDutyCycle(abs(rpwm))


#
# i = 1
# while (True):
#     move_bot(20,40)
#     move_bot(i,i)
#     sleep(0.1)
#     print((i) % 100, (i) % 100)
#     i+=1
if __name__ == '__main__':
    while True:
        move_bot(24,16)