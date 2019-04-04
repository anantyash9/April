#!/usr/bin/env python

from __future__ import print_function
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from nav_msgs.msg import Path
import tf
import numpy
from geometry_msgs.msg import PoseStamped
pub2=None
pub3=None
def dist(x,y):
    return numpy.sqrt(numpy.sum((x-y)**2))


def callback(data):
    global pub2,pub3
    a = numpy.array((0, 0))
    cte=0
    distance=100
    for i in range(len(data.poses)):
        x=data.poses[i].pose.position.x
        y=data.poses[i].pose.position.y
        b = numpy.array((x, y))
        temp = dist(a,b)
        if distance>temp:
            distance=temp
            cte=y
    f=Float32()
    f.data=cte
    pub2.publish(f)
    f.data=distance
    pub3.publish(f)



def node():
    global pub2,pub3
    pub2 = rospy.Publisher('cte',Float32, queue_size=1)
    pub3 = rospy.Publisher('dist', Float32, queue_size=1)
    rospy.init_node('cte_node', anonymous=True)
    rospy.Subscriber("path_transformed", Path, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        node()

    except rospy.ROSInterruptException:
        pass