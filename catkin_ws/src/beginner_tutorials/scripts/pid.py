#!/usr/bin/env python

import socket
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
import thread
import urllib2
from time import sleep
import time
move=True
avg = 25
right,left = 0,0
rpwm=0
lpwm=0
kp= 20
perror=0
kd=2
roll=0
target_roll=0.9983
def pid(data):
    global right,left,perror
    cte=data.data
    error= cte*kp - kd * (cte - perror)
    right=avg+error-2
    left=avg-error+2
    left=max(min(100,left),-100)
    right = max(min(100, right), -100)
    perror=cte

def can_bot_move(data):
    global move
    move=data.data

def update_pose(data):
    global roll
    roll=data.pose.orientation.z

def node():
    #rospy.Subscriber("cte", Float32, pid)
    rospy.Subscriber("move", Bool, can_bot_move)
    rospy.Subscriber('line',PoseStamped,update_pose)
    rospy.spin()
def disp():
    global lpwm,rpwm
    while not rospy.is_shutdown():
        if move:
            lpwm=int(left)
            rpwm=int(right)
        else:
            lpwm=0
            rpwm=0



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.254.2', 50000)
sock.connect(server_address)

def align_right():
    global right,left
    while not rospy.is_shutdown():
        print(lpwm,rpwm)
        print(roll,'            ',target_roll)
        while round(target_roll,2)!=round(roll,2):
            print('in')
            if move:
                left = 30
                right = -30
            else:
                left = 0
                right = 0

        left=0
        right=0



def hitFlask():
    try:
        while not rospy.is_shutdown():
            message = str(lpwm) + ":" + str(rpwm)
            if not( lpwm== 0 and rpwm==0):
                print message
            sock.sendall(message)
            sleep(0.1)
    finally:
        sock.close()

if __name__ == '__main__':
    try:
        rospy.init_node('pid', anonymous=True)
        thread.start_new_thread(node, ())
        thread.start_new_thread(disp, ())
        thread.start_new_thread(hitFlask, ())
        align_right()

    except rospy.ROSInterruptException:
        pass