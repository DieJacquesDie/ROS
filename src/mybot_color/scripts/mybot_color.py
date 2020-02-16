#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

def listener():

    rospy.init_node('mybot_color', anonymous=True)
    rospy.Subscriber('turtle1/pose', Pose, read_pose_callback) #inscription à turtle pose avec msg rendu Pose et affichage de la pose
    rospy.spin()

def read_pose_callback(msg):
    print(msg)
    rospy.wait_for_service('/turtle1/set_pen')
    print("test")
    try:

        setpen=rospy.ServiceProxy('/turtle1/set_pen',SetPen) # ServiceProxy pour

        if msg.x<3:
            a=setpen() #appel du service cree
        else:
            setpen(off=True)
    except rospy.ServiceException as e:
        raise "fail %s"%e

if __name__ == '__main__':
    try:

        listener()


    except rospy.ROSInterruptException:
         pass
