#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SIMPLY PUT :
-get lidar datas from each side of the bot
-setting a treshold for the distance of the obstacle
-if there is nothing, just turn forever until an obstacle is detected because danger could come from everywhere
-if treshold is not respected : move it or turn it depending of where the obstacle is coming from
-check previous datas to check what is coming toward us (or running away).
- // ! \\ perpendicular alignement not quite right
"""
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
    rate = rospy.Rate(10)
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

    right = np.mean(msg.ranges[240:300])
    left= np.mean(msg.ranges[60:120])
    front =  np.mean(msg.ranges[0:10]+msg.ranges[350:359])

    back = np.mean(msg.ranges[170:190])

    tab=[right,left,back,front]
    print("tab : \n ############# \n")
    print("left "+str(left))
    print('\n')
    print("right " +str(right))
    print('\n')
    print("up "+str(front))
    print('\n')
    print("down " +str(back))
    print('\n')

    #etat initial
    if  front==float("inf") and back==float("inf") and left==float("inf") and right==float("inf") and right_previous==float("inf") and left_previous==float("inf") and test==0:
        command(3)
        print("rotation")

    #detection gauche
    if left!=float("inf") and(back==float("inf") or front==float("inf")):
        command(3)
        print("obstacle a gauche")
        test=0 #le test permet au robot de ne pas osciller en droite et gauche en revenant a l etat initial une fois qu il n y a plus de donnees sur les cotes
    #detection droite
    elif right!=float("inf")and(back==float("inf") or front==float("inf")):
        command(4)
        print("obstacle a droite")
        test=1

    if (front <=distance):
        if front_previous>front:
            command(2)
    else:
        if front_previous<front:
            command(1)

    if (back <=distance):
        if back_previous>back:
            command(1)
    else:
        if back_previous<back:
            command(2)

    print("\n")
    front_previous=front
    left_previous=left
    right_previous=right
    back_previous=back

###################publish to cmd vel the datas the decisions made with the lidar datas##############################################################################

def command(instruction):

    global cmd

    if instruction ==1 : # UP KEY
        cmd.angular.z=0
        if cmd.linear.x<0:
            cmd.linear.x=0
        if cmd.linear.x>0.25:
            cmd.linear.x =0.25
        else:
            cmd.linear.x+=0.03
    	publisher_for_teleop(cmd)

    if instruction == 2:  # DOWN key
        cmd.angular.z=0
        if cmd.linear.x>0:
            cmd.linear.x=0
        if cmd.linear.x<-0.25:
            cmd.linear.x =-0.25
        else:
            cmd.linear.x-=0.03
        publisher_for_teleop(cmd)

    if instruction == 3: # left
        cmd.linear.x=0

        cmd.angular.z=0.6
        publisher_for_teleop(cmd)

    if instruction == 4: # right
        cmd.linear.x=0

        cmd.angular.z=-0.6
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
