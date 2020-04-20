#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import sys, termios, tty
from geometry_msgs.msg import Twist


# Function to Publish
# =============================================================
def simple_publisher(msg):

    pub=rospy.Publisher(rospy.get_param("topic"),Twist,queue_size=10)
    rospy.init_node("teleop_lidar", anonymous=True)
    rate = rospy.Rate(20)
    if not rospy.is_shutdown():
	rospy.loginfo(msg)
	pub.publish(msg)
	rate.sleep()


# Function to get which key is pressed in the terminal
# ==============================================================
def get_ch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == '__main__':

    cmd = Twist()
    cmd.linear.x = 0
    cmd.linear.y = 0
    cmd.linear.z = 0
    cmd.angular.x = 0
    cmd.angular.y = 0
    cmd.angular.z = 0



    while not rospy.is_shutdown():
        try:
            # How to use the get_ch function
            char = get_ch()

            if char == "u":  # UP key
                cmd.angular.z=0
                if cmd.linear.x<0:
                    cmd.linear.x=0
                if cmd.linear.x>0.25:
                    cmd.linear.x =0.25
                else:
                    cmd.linear.x+=0.03
            	simple_publisher(cmd)

            if char == "d":  # DOWN key
                cmd.angular.z=0
                if cmd.linear.x>0:
                    cmd.linear.x=0
                if cmd.linear.x<-0.25:
                    cmd.linear.x =-0.25
                else:
                    cmd.linear.x-=0.03
	            simple_publisher(cmd)

            if char =="l": # left
                cmd.linear.x=0

                cmd.angular.z=0.6
                simple_publisher(cmd)

            if char =="r": # right
                cmd.linear.x=0

                cmd.angular.z=-0.6
                simple_publisher(cmd)


        except rospy.ROSInterruptException:
            pass
