#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SIMPLY PUT :
-get lidar datas from the front
-setting a treshold for the distance of the obstacle
-if treshold is not respected : stop it. else all gas no brakes

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

cmd = Twist()
cmd.linear.x = 0
cmd.linear.y = 0
cmd.linear.z = 0
cmd.angular.x = 0
cmd.angular.y = 0
cmd.angular.z = 0

###############################################################################################
def publisher_for_teleop(msg):
    #lidar_follow
    pub=rospy.Publisher(rospy.get_param("topic"),Twist,queue_size=10)
    rate = rospy.Rate(50)
    if not rospy.is_shutdown():
	rospy.loginfo(msg)
	pub.publish(msg)
	rate.sleep()

################################################################################################
def read_distance_callback(msg):

    global front_previous
    global distance

    front = np.mean(msg.ranges[0:10]+msg.ranges[350:359])
    print(front)
    if front>distance:
            command(1)
    else:
            command(0)


    front_previous=front
#################################################################################################
def command(instruction):

    global cmd

    if instruction ==1 :
        if cmd.linear.x>0.4:
            cmd.linear.x =0.4
        else:
            cmd.linear.x+=0.04
    	publisher_for_teleop(cmd)

    if instruction == 0:  # stop key
        cmd.linear.x=0
        publisher_for_teleop(cmd)


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