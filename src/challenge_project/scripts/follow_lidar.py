#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SIMPLY PUT :
-get lidar datas from the front
-setting a treshold for the distance of the obstacle
-if treshold is not respected : move it.
-optional but we do not have any trust in all these things: check previous datas to check if we stopped.
"""
import rospy
import numpy as np
from pykeyboard import PyKeyboard
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8


###GLOBALS###
keyb = PyKeyboard()

front_previous = 0

distance=rospy.get_param("distance")

################################################################################################
def read_distance_callback(msg):
    global front_previous
    global distance

    front = np.mean(msg.ranges[0:10]+msg.ranges[350:359])
    print(front)
    if (front <=distance):
        if front_previous>front:
            keyb.tap_key('d')

        print("distance reglementaire trop petite")
    else:
        if front_previous<front:
            keyb.tap_key('u')

        print("distance reglementaire trop grande")

    front_previous=front

################################################################################################

def lidar_listener():
    rospy.init_node('lidar_follow', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, read_distance_callback)

    rospy.spin()

#################################################################################################

if __name__ == '__main__':
    try:
        lidar_listener()

    except rospy.ROSInterruptException:
        pass
