#!/usr/bin/env python

'''Demonstrate Python wrapper of C apriltags library by running on camera frames.'''
# from __future__ import division
# from __future__ import print_function

import math
from argparse import ArgumentParser
import time
import cv2
import numpy
import rospy

import apriltags

# for some reason pylint complains about members being undefined :(
# pylint: disable=E1101
camera_params = (648.329284815438, 665.1984893547117, 297.3558498244366, 241.85205324200447)
size = 32
position = {'tag0': None, 'roll': None ,'time':None}


def main():
    global position
    '''Main function.'''

    parser = ArgumentParser(
        description='test apriltags Python bindings')

    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')

    apriltags.add_arguments(parser)

    options = parser.parse_args()

    try:
        cap = cv2.VideoCapture(int(options.device_or_movie))
    except ValueError:
        cap = cv2.VideoCapture(options.device_or_movie)

    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

    window = 'Camera'
    cv2.namedWindow(window)

    # set up a reasonable search path for the apriltags DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.

    detector = apriltags.Detector(options,
                                  searchpath=apriltags._get_demo_searchpath())

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # gray = clahe.apply(gray)
        detections, dimg = detector.detect(gray, return_image=True)

        num_detections = len(detections)
        # print('Detected {} tags.\n'.format(num_detections))
        overlay = frame // 2 + dimg[:, :, None] // 2
        for i, detection in enumerate(detections):
            pose, e0, e1 = detector.detection_pose(detection,
                                                   camera_params,
                                                   size)

            apriltags._draw_pose(overlay,
                                 camera_params,
                                 size,
                                 pose)

            if num_detections > 0:
                b = numpy.matrix([[0], [0], [0], [1]])
                coordinate = numpy.matmul(pose, b)
                #
                # print('Detection {} of {}:'.format(i + 1, num_detections))
                # print()
                print('x', coordinate[0], 'y', coordinate[1], 'z', coordinate[2])
                # print()
                new_coord = transformRx(53, coordinate)
                position['tag0'] = new_coord
                # print('x', new_coord[0], 'y', new_coord[1], 'z', new_coord[2])
                # print()
                roll = math.degrees(math.atan2(pose[0][1] , pose[0][0]))
                yaw = math.degrees(math.atan((-1 * pose[2][0]) / math.sqrt((pose[2][1]) ** 2 + (pose[2][2]) ** 2)))
                pitch = math.degrees(math.atan(pose[2][1] / pose[2][2]))
                position['roll'] = roll + 90
                position['time'] = rospy.Time.now()
                print('Roll ', roll+90)
                print('Yaw ', yaw)
                print('Pitch ', pitch)
                print()

        cv2.imshow(window, overlay)
        k = cv2.waitKey(1)

        if k == 27:
            break


def transformRx(deg, cood):
    # print(cood)

    Rx = numpy.matrix(
        [[1, 0, 0, 0], [0, math.cos(deg), -math.sin(deg), 0], [0, math.sin(deg), math.cos(deg), 0], [0, 0, 0, 1]])
    # print(Rx)
    # coll=numpy.transpose(cood)
    return numpy.matmul(Rx, cood)


if __name__ == '__main__':
    main()
