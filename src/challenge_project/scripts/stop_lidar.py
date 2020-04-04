#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SIMPLY PUT :
-get lidar datas
-put mean of lidar datas in a tab of directions of the robot
-setting a treshold for the tab
-if treshold is not respected : stop.
-optional but we do not have any trust in all these things: check previous datas to check if we stopped.
- theres some braking distance if we are going too fast so please drive responsibly.
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
back_previous = 0
right_previous=0
left_previous=0
stop=rospy.get_param("stop")

################################################################################################
def read_distance_callback(msg):
    global front_previous
    global back_previous
    global left_previous
    global right_previous
    global stop

    right = np.mean(msg.ranges[0:10]+msg.ranges[350:359])

    back = np.mean(msg.ranges[80:100])

    left = np.mean(msg.ranges[170:190])

    front = np.mean(msg.ranges[260:280])

    tab=[right,back,left,front]
    print(tab)

    if (right<=stop and right<=right_previous):
        keyb.tap_key('s')
        keyb.tap_key('s')
        keyb.tap_key('s')
        print("obstacle")

    elif (back<=stop  and back<=back_previous):
        keyb.tap_key('s')
        keyb.tap_key('s')
        keyb.tap_key('s')
        print("obstacle")

    elif (left<=stop and left<=left_previous):
        keyb.tap_key('s')
        keyb.tap_key('s')
        keyb.tap_key('s')
        print("obstacle")

    elif (front <=stop and front<=front_previous):
        keyb.tap_key('s')
        keyb.tap_key('s')
        keyb.tap_key('s')
        print("obstacle")

    else :
        front_previous=front
        back_previous=back
        left_previous=left
        right_previous=right

################################################################################################

def lidar_listener():
    rospy.init_node('lidar_stop', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, read_distance_callback)

    rospy.spin()

#################################################################################################

if __name__ == '__main__':
    try:
        lidar_listener()

    except rospy.ROSInterruptException:
        pass
