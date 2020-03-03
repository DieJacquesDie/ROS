#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
p_bord = 0



def set_color(r,g,b):

    try:
	setpen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
	setpen(r,g,b,3,False)
    except rospy.ServiceException, e:
	print "Service call failed: %s"%e

# Callback function for reading turtlesim node output
def read_pose_callback(msg):

    global p_bord

    if msg.x < 2 or msg.x > 9 or msg.y < 2 or msg.y > 9 :
	bord = 1
    else :
	bord = 0

    print(msg.x,msg.y)

    if bord and not p_bord:
	set_color(255,0,0)
    elif not bord and p_bord:
	set_color(255,255,255)

    p_bord = bord


def simple_listener():
    rospy.init_node('simple_listener', anonymous=True)
    rospy.Subscriber('/turtle1/pose', Pose, read_pose_callback)

    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.wait_for_service('turtle1/set_pen')
        simple_listener()

    except rospy.ROSInterruptException:
        pass
