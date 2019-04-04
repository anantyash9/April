#!/usr/bin/env python
import sys
import thread
import camtest
import rospy
import tf
from tf import transformations
from geometry_msgs.msg import PoseStamped
import signal

def sigint_handler(signum, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

thread.start_new_thread(camtest.main, ())

def handle_turtle_pose():

    pub2 = rospy.Publisher('line', PoseStamped, queue_size=1)
    rospy.init_node('bot_motion', anonymous=True)
    br = tf.TransformBroadcaster()
    while True:
        if camtest.position['tag0'] is not None and camtest.position['roll'] is not None:
            # print('bot position', camtest.position['tag0'])
            # print('roll', camtest.position['roll'] / 360 * 2 * 22 / 7)
            br.sendTransform((-camtest.position['tag0'][0] / 100, camtest.position['tag0'][2] / 100, 0),
                             transformations.quaternion_from_euler(0, 0, camtest.position['roll'] / 360 * 2 * 22 / 7),
                             rospy.Time.now(),
                             'bot',
                             "base_link")
            p = to_pose_stamped(-camtest.position['tag0'][0] / 100, camtest.position['tag0'][2] / 100,
                                camtest.position['roll'])

            p.header.stamp = camtest.position['time']

            pub2.publish(p)


            br.sendTransform((0.0, 0.0, 0.0),
                             (0.0, 0.0, 0.0, 1),
                             rospy.Time.now(),
                             "map",
                             "base_link")
            br.sendTransform((0.0, 0.0, 0.0),
                             (0.0, 0.0, 0.0, 1),
                             rospy.Time.now(),
                             "bot2",
                             "bot")


def to_pose_stamped(x, y, roll):
    pose = PoseStamped()
    pose.header.stamp = rospy.Time.now()
    pose.header.frame_id = "map"
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0
    # print roll
    temp = transformations.quaternion_from_euler(0, 0, roll / 360 * 2 * 22 / 7)
    pose.pose.orientation.x = temp[0]
    pose.pose.orientation.y = temp[1]
    pose.pose.orientation.z = temp[2]
    pose.pose.orientation.w = temp[3]

    return pose


if __name__ == '__main__':
    handle_turtle_pose()
