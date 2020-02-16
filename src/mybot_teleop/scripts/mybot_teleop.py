#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import sys, termios, tty

from geometry_msgs.msg import Twist


linear_value=1
angular_value=1




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

def simple_publisher(t):
    pub=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10) #publish ds cmd_vel de type float64 avec q10
    rospy.init_node('mybot_teleop', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    if not rospy.is_shutdown():
        rospy.loginfo(t)
        pub.publish(t)
        rate.sleep()
while __name__ == '__main__':

    try:
        # How to use the get_ch function
        char = get_ch()
        commande=Twist()
        commande.linear.x = linear_value
        commande.linear.y = 0
        commande.linear.z = 0
        commande.angular.x = 0
        commande.angular.y = 0
        commande.angular.z = 0
        if char == "\x1b[A":  # UP key
            pass
        if char == "\x1b[B":  # DOWN key
            commande.linear.x = -linear_value

        if char == "\x1b[C":  # RIGHT key
            commande.angular.z = -angular_value

        if char == "\x1b[D":  # LEFT
            commande.angular.z = angular_value

        if char == "qqq":  # QUIT
            rospy.is_shutdown()
        if char == "sss":  # STOP
            commande.linear.x = 0
            commande.linear.y = 0
            commande.linear.z = 0
            commande.angular.x = 0
            commande.angular.y = 0
            commande.angular.z = 0

        simple_publisher(commande)
    except rospy.ROSInterruptException:
        pass
