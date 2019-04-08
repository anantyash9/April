#!/usr/bin/env python

from __future__ import print_function
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Path
import tf
import numpy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32
from std_msgs.msg import Bool
import thread



state_t=False
state_d=False
state_e=False
def dist(x,y):
    return numpy.sqrt(numpy.sum((x-y)**2))


def check_time(data):
    global state_t
    if (rospy.Time.now()-data.header.stamp)>rospy.Duration.from_sec(0.1):
        state_t=False
    else:
        state_t=True


def check_dist(data):
    global  state_d
    if (data.data>0.5):
        state_d = False
    else:
        state_d=True

def check_end(data):
    global  state_e
    if (data.data<0.2):
        state_e = False
    else:
        state_e=True


def node():

    global state
    rospy.Subscriber("line", PoseStamped, check_time)
    rospy.Subscriber("dist", Float32, check_dist)
    rospy.Subscriber("dist_end", Float32, check_end)
    rospy.spin()
def publis():
    pub = rospy.Publisher('move', Bool, queue_size=1)
    rate = rospy.Rate(10)  # 1hz
    while not rospy.is_shutdown():
        d=Bool()
        d.data=state_d and state_t and state_e
        print('distance : ',state_d,'time : ',state_t,'dist_end : ',state_e)
        pub.publish(d)
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('stop', anonymous=True)
        thread.start_new_thread(node,())
        publis()

    except rospy.ROSInterruptException:
        pass