#!/usr/bin/env python

from __future__ import print_function

import math

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from nav_msgs.msg import Path
import tf
import numpy
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion
pub2=None
pub3=None
id=0
def dist(x,y):
    return numpy.sqrt(numpy.sum((x-y)**2))


def callback(data):
    global pub2,pub3,pub4,pub5,id
    a = numpy.array((0, 0))
    cte=0
    roll = 0
    distance=100
    for i in range(len(data.poses)):
        x=data.poses[i].pose.position.x
        y=data.poses[i].pose.position.y
        b = numpy.array((x, y))
        temp = dist(a,b)
        if distance>temp:
            id=data.poses[i].header.seq
            distance=temp
            cte=y

    f=Float32()
    f.data=cte
    pub2.publish(f)
    f.data=distance
    pub3.publish(f)
    f.data = temp
    pub5.publish(f)



def angle_publisher(data):
    global pub4
    for pose in data.poses:
        if pose.header.seq==id:
            qList = [pose.pose.orientation.x, pose.pose.orientation.y,
                     pose.pose.orientation.z, pose.pose.orientation.w]
            (y, p, r) = euler_from_quaternion(qList)
            roll = r
            roll = numpy.rad2deg(roll)
            f=Float32()
            f.data = roll
            pub4.publish(f)


def node():
    global pub2,pub3,pub4,pub5
    pub2 = rospy.Publisher('cte',Float32, queue_size=1)
    pub3 = rospy.Publisher('dist', Float32, queue_size=1)
    pub4 = rospy.Publisher('angle', Float32, queue_size=1)
    pub5 = rospy.Publisher('dist_end', Float32, queue_size=1)
    rospy.init_node('cte_node', anonymous=True)
    rospy.Subscriber("path_transformed", Path, callback)
    rospy.Subscriber("path", Path, angle_publisher)
    rospy.spin()


if __name__ == '__main__':
    try:
        node()

    except rospy.ROSInterruptException:
        pass