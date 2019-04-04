#!/usr/bin/env python

from __future__ import print_function
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import numpy
import pickle
import signal
import sys




path=Path()
path.header.seq=0
path.header.frame_id = "base_link"
first=True
prev=None
i=0


def signal_handler(sig, frame):
    pfile = open('path', 'ab')
    print('dumping path')
    pickle.dump(path, pfile)
    pfile.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def dist(x,y):
    return numpy.sqrt(numpy.sum((x-y)**2))

def callback(data):
    global i,path,first,prev
    x = data.pose.position.x
    y = data.pose.position.y
    if first==True:
        path.header.stamp = rospy.Time.now()
        data.header.seq=i
        i+=1
        path.poses.append(data)
        prev=numpy.array((x, y))
        first=False
    else:
        a = numpy.array((x, y))
        d = dist(a, prev)
        if d >=0.3:
            data.header.seq = i
            i += 1
            path.poses.append(data)
            prev = a
            print(i)





def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("line", PoseStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pfile = open('path', 'ab')
        print('dumping path')
        pickle.dump(path,pfile)
        pfile.close()
