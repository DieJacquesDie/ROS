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
    rate = rospy.Rate(10)
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
        ch = sys.stdin.read(3)
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

    linear_vel = rospy.get_param("linear_scale")
    angular_vel = rospy.get_param("angular_scale")



    while not rospy.is_shutdown():
        try:
            # How to use the get_ch function
            char = get_ch()


            if char == "\x1b[A":  # UP key
	        cmd.angular.z = 0
                cmd.linear.x += linear_vel
		if cmd.linear.x > 1:
		    cmd.linear.x = 1
		    print("max linear vel reached")
		print(cmd.linear.x)
	        simple_publisher(cmd)
            if char == "\x1b[B":  # DOWN key
	        cmd.angular.z = 0
                cmd.linear.x += -linear_vel
		if cmd.linear.x < -1:
		    cmd.linear.x = -1
		    print("max linear vel reached")
		print(cmd.linear.x)
	        simple_publisher(cmd)
            if char == "\x1b[C":  # RIGHT key
                cmd.linear.x = 0
	        cmd.angular.z += -angular_vel
		if cmd.angular.z < -1:
		    cmd.angular.z = -1
		    print("max angular vel reached")
		print(cmd.angular.x)
	        simple_publisher(cmd)
            if char == "\x1b[D":  # LEFT
                cmd.linear.x = 0
	        cmd.angular.z += angular_vel
		if cmd.angular.z > 1:
		    cmd.angular.z = 1
		    print("max angular vel reached")
		print(cmd.angular.x)
	        simple_publisher(cmd)
            if char == "qqq":  # QUIT
		cmd.linear.x = 0
   	        cmd.linear.y = 0
    	        cmd.linear.z = 0
                cmd.angular.x = 0
                cmd.angular.y = 0
                cmd.angular.z = 0
		simple_publisher(cmd)
                break
            if char == "sss":  # STOP
		cmd.linear.x = 0
   	        cmd.linear.y = 0
    	        cmd.linear.z = 0
                cmd.angular.x = 0
                cmd.angular.y = 0
                cmd.angular.z = 0
		simple_publisher(cmd)
		print("movement stopped")



        except rospy.ROSInterruptException:
            pass
