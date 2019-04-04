#!/usr/bin/env python
from __future__ import print_function
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Path
import tf
from geometry_msgs.msg import PoseStamped
import pickle

listener = None

def callback(path):
    global listener
    t = tf.TransformerROS(True, rospy.Duration(10))
    pub2 = rospy.Publisher('path_transformed', Path, queue_size=1)
    for i in range(len(path.poses)):
        path.poses[i].header.frame_id='base_link'
        path.poses[i].header.stamp = rospy.Time()
        trans,rotat=listener.lookupTransform('bot','base_link',rospy.Time())
        # t = listener.getLatestCommonTime("/base_link", "/bot")
        path.poses[i] = listener.transformPose("/bot", path.poses[i])
        path.poses[i].header.stamp = rospy.Time()
        path.poses[i].header.seq=i
        print('p_in_bot', path.poses[i])
    pub2.publish(path)


def subed():
    global listener
    rospy.init_node('transformed_path', anonymous=True)
    listener = tf.TransformListener()
    print(listener.allFramesAsString())
    rospy.Subscriber("path", Path, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        subed()


    except rospy.ROSInterruptException:
        pass
