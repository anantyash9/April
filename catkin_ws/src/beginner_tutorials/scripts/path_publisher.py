#!/usr/bin/env python

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic
from __future__ import print_function
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import pickle
from threading import Thread

from flask import Flask
from flask_sockets import Sockets

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
app = Flask(__name__)
sockets = Sockets(app)
rospy.init_node('path_publisher', anonymous=True)

state=0
to_state=0
state_chart={'Aquafina':1,'Good':2,'Lays':3,'return':0}


@sockets.route('/')
def echo_socket(ws):
    global to_state
    while not ws.closed:
        message = ws.receive()
        print (message)
        if message in state_chart:
            to_state=state_chart[message]


server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
path=Path()
def talker():
    global path
    pub2 = rospy.Publisher('path', Path, queue_size=1)

    rate = rospy.Rate(10) # 1hz
    while not rospy.is_shutdown():
        path.header.stamp = rospy.Time.now()
        if len(path.poses)>0:
            for i in range(len(path.poses)):
                path.poses[i].header.stamp=rospy.Time.now()
            pub2.publish(path)
            rate.sleep()

def selector():
    global path
    pfile = open('path', 'rb')
    path_b = pickle.load(pfile)
    pfile = open('path_forward', 'rb')
    path_f = pickle.load(pfile)
    i=None
    while not rospy.is_shutdown():
        if to_state ==1:
            path=path_f
            print('forward path selected')
        elif to_state==2:
            path=path_b
            print ('backward path seclected')



if __name__ == '__main__':
    try:
        Thread(target=selector, args=()).start()
        Thread(target=talker, args=()).start()
        server.serve_forever()



    except rospy.ROSInterruptException:
        pass
