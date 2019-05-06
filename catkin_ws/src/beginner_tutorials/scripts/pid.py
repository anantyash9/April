#!/usr/bin/env python

import socket
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
import thread
import urllib2
from time import sleep
import numpy
import time
from tf.transformations import euler_from_quaternion


from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)



move=True
avg = 30
right,left = 0,0
rpwm=0
lpwm=0
kp= 40
roll=0
target_roll=0
cte=0
def get_cte(data):
    global cte
    cte = data.data

def pid():
    global right,left
    error= cte*kp
    r=avg+error-4
    l=avg-error+4
    left=max(min(100,l),-100)
    right = max(min(100, r), -100)

def can_bot_move(data):
    global move
    move=data.data

def update_pose(data):
    global roll
    qList = [data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w]
    (y, p, r) = euler_from_quaternion(qList)
    roll = numpy.rad2deg(r)

def update_angle(data):
    global target_roll
    target_roll = data.data

def node():
    rospy.Subscriber("cte", Float32, get_cte)
    rospy.Subscriber("move", Bool, can_bot_move)
    rospy.Subscriber('line',PoseStamped,update_pose)
    rospy.Subscriber('angle', Float32, update_angle )
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
server_address = ('192.168.1.96', 50001)
sock.connect(server_address)

def align_right():
    global right,left
    while not rospy.is_shutdown():
        #print(lpwm,rpwm)
        print(roll,'            ',target_roll)
        while  not (target_roll-10 <= roll <= target_roll+10 ):
            error=roll-target_roll
            if abs(error)>180:
                if error <0:
                    error = error +360
                else:
                    error = error - 360
            #print(roll, '            ', target_roll , '            ', error )

            if error >0:
                if abs(error) >= 50:
                    left = 30
                    right = -30
                else:
                    left = avg+10
                    right = 0
            else:
                if abs(error) >= 50:
                    left = -30
                    right = 30
                else:
                    left = 0
                    right = avg+10

        pid()




def hitFlask():
    try:
        while not rospy.is_shutdown():
            message = str(lpwm) + ":" + str(rpwm)
            if not( lpwm== 0 and rpwm==0):
                print message
            try:
                sock.sendall(message)
                sleep(0.3)
            except Exception as e:
                print(e)
                pass
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