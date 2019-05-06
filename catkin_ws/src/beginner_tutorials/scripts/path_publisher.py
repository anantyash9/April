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
import glob
from flask import Flask
from flask_sockets import Sockets
import numpy
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
app = Flask(__name__)
sockets = Sockets(app)
rospy.init_node('path_publisher', anonymous=True)

state=0
to_state=0
x,y=0,0
state_chart={'Aquafina':(0.68,2.47),'Good':(-0.638451141768,2.397513653),'Lays':(5,5),'reverse':(-1.60,5.32)}


@sockets.route('/')
def echo_socket(ws):
    global to_state
    while not ws.closed:
        message = ws.receive()
        print (message)
        if message in state_chart:
            selector(message)


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

def dist(x,y):
    return numpy.sqrt(numpy.sum((x-y)**2))

def selector(item):
    global path
    files=(glob.glob("./options/*"))
    distance=100
    path_temp=Path()
    for i in range(len(files)):
        c=0
        p= open(files[i], 'rb')
        path_t = pickle.load(p)
        p.close()
        x_end=path_t.poses[-1].pose.position.x
        print(x_end,type(x_end))
        y_end=path_t.poses[-1].pose.position.y
        print(y_end, type(y_end))
        a = numpy.array(state_chart[item])
        b = numpy.array((x_end,y_end))
        temp=dist(a,b)
        c+=temp
        x_beg = path_t.poses[0].pose.position.x
        y_beg = path_t.poses[0].pose.position.y
        a = numpy.array((x,y))
        b = numpy.array((x_beg, y_beg))
        temp = dist(a, b)
        c+=temp
        print('Path no ', i, '      a+b distance  ', c)
        if distance>c:
            distance=c
            print(path_t)
            path_temp=path_t

    path = path_temp


def updatexy(data):
    global x,y
    x=data.pose.position.x
    y=data.pose.position.y



def node():
    rospy.Subscriber("line", PoseStamped, updatexy)
    rospy.spin()


if __name__ == '__main__':
    try:
        Thread(target=node, args=()).start()
        Thread(target=talker, args=()).start()
        server.serve_forever()



    except rospy.ROSInterruptException:
        pass
