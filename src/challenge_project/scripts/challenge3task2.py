#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import numpy as np

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8


###GLOBALS###

front_previous = 0
back_previous = 0
right_previous=float("inf")
left_previous=float("inf")
test=0
distance=rospy.get_param("distance")

cmd = Twist()
cmd.linear.x = 0
cmd.linear.y = 0
cmd.linear.z = 0
cmd.angular.x = 0
cmd.angular.y = 0
cmd.angular.z = 0

################################creating publisher for cmd vel###############################################################
def publisher_for_teleop(msg):
    #lidar_follow
    pub=rospy.Publisher(rospy.get_param("topic"),Twist,queue_size=10)
    rate = rospy.Rate(50)
    if not rospy.is_shutdown():
	rospy.loginfo(msg)
	pub.publish(msg)
	rate.sleep()

############################what to do with lidar datas####################################################################
def read_distance_callback(msg):

    global front_previous
    global back_previous
    global left_previous
    global right_previous
    global distance
    global test

    right = np.mean(msg.ranges[260:280])
    left= np.mean(msg.ranges[80:100])
    front =  np.mean(msg.ranges[0:10]+msg.ranges[350:359])
    back = np.mean(msg.ranges[170:190])

    tab=[right,left,back,front]
    #1 up
    #2 down
    #3 left
    #4 right
    #5 stop

    if left-right<0:
        command(3)
        print("go left")
    if right-left<0:
        command(4)
        print("go right")
    else :
        command(1)

        """"

    if(np.min(tab)<0.5): #too close of something
        #check left and right
        if np.argmin(tab)==0:
            command(3)
            print("right too close")
        if np.argmin(tab)==1:
            command(4)
            print("left too close")
        #retour en arriere
    else :
        command(1)
        print ("baby come on")
        """






    print("\n")
    front_previous=front
    left_previous=left
    right_previous=right
    back_previous=back

###################publish to cmd vel the datas the decisions made with the lidar datas##############################################################################

def command(instruction):

    global cmd

    if instruction ==1 : # UP KEY

            cmd.linear.x=0.2
    	    publisher_for_teleop(cmd)


    if instruction == 3: # left
        
        cmd.angular.z=cmd.angular.z+0.5
        publisher_for_teleop(cmd)

    if instruction == 4: # right

        cmd.angular.z=cmd.angular.z-0.5
        publisher_for_teleop(cmd)



########################################listener of /scan ########################################################

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
