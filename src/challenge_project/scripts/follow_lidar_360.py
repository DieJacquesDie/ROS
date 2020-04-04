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
back_previous = 0
right_previous=float("inf")
left_previous=float("inf")
test=0
distance=rospy.get_param("distance")

def my_mean(x):
    return np.average(x, weights=np.ones_like(x) / x.size)

################################################################################################
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
        keyb.tap_key('l')
        print("rotation")

    #detection gauche
    if left!=float("inf") and(back==float("inf") or front==float("inf")):
        keyb.tap_key('l')
        print("obstacle a gauche")
        test=0 #le test permet au robot de ne pas osciller en droite et gauche en revenant a l etat initial une fois qu il n y a plus de donnees sur les cotes
    #detection droite
    elif right!=float("inf")and(back==float("inf") or front==float("inf")):
        keyb.tap_key('r')
        print("obstacle a droite")
        test=1

    if (front <=distance):
        if front_previous>front:
            keyb.tap_key('d')

        print("distance reglementaire trop petite")
    else:
        if front_previous<front:
            keyb.tap_key('u')

        print("distance reglementaire trop grande")


    if (back <=distance):
        if back_previous>back:
            keyb.tap_key('u')

        print("distance reglementaire trop petite")
    else:
        if back_previous<back:
            keyb.tap_key('d')

        print("distance reglementaire trop grande")




    front_previous=front
    left_previous=left
    right_previous=right
    back_previous=back

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
