#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
teleop_camera is used when the robot needs to follow a line : use it when you encounter a specific line or it will crash !
basically, we convert the datas of the camera to opencv exploitable datas, we extract the line that we want to follow with a mask
, we compute the centroid of the image and we publish to /cmd_vel linear/angular values to join this centroid.

"""
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError
from pykeyboard import PyKeyboard
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8


keyb2 = PyKeyboard()

########### command init ########################
"""
cmd_left = Twist()
cmd_left.linear.x = 0.01
cmd_left.linear.y = 0
cmd_left.linear.z = 0
cmd_left.angular.x = 0
cmd_left.angular.y = 0e
cmd_left.angular.z = 0.01

cmd_right = Twist()
cmd_right.linear.x = 0.01
cmd_right.linear.y = 0
cmd_right.linear.z = 0
cmd_right.angular.x = 0
cmd_right.angular.y = 0
cmd_right.angular.z = -0.01

cmd = Twist()
cmd.linear.x = 0
cmd.linear.y = 0
cmd.linear.z = 0
cmd.angular.x = 0
cmd.angular.y = 0
cmd.angular.z = 0
"""


bridge = CvBridge()
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)


def read_image_callback(msg):

    global bridge
    global pub
    r=-1
    l=-1

    cv_image=bridge.imgmsg_to_cv2(msg,"bgr8") #convert ROS img msg to openCV image
    hsv_image=cv2.cvtColor(cv_image,cv2.COLOR_RGB2HSV) # convert RGB/BGR to HSV (hue saturation value)
    mask_white=cv2.inRange(hsv_image,(0,0,200),(50,50,255)) #filter treshold to leave only the line in binary datas
    bottom_mask_white = mask_white[500:800, 0:800].copy() #select only the bottom of the image, important for computing optimization / avoid noises on practical applications

    #for optimisation -> reduce the size of images received

    #compute Centroids of our line
    M = cv2.moments(bottom_mask_white)
    if M['m00'] > 0:
      cx=int (M['m10']/M['m00'])
      cy=int (M['m01']/M['m00'])
    print(cx,cy)

    bottom_mask_white_c=cv2.circle(bottom_mask_white, (cx,cy), 50, (255,0,0), 3)

    err=float(cx-400) #400 for the middle of the screen

    set_cmd(err)
    print(cmd)
    pub.publish(cmd)


    cv2.imshow("Image window",bottom_mask_white_c)
    cv2.waitKey(1)


def set_cmd(err):
    global cmd

    if err>0:
	cmd.linear.x = (1-(abs(err)/400))*0.06
	cmd.angular.z = (abs(err)/400)*-0.35

    if err<0:
	cmd.linear.x = (1-(abs(err)/400))*0.06
	cmd.angular.z = (abs(err)/400)*(0.35)



def camera_listener():
    rospy.init_node('camera_listener', anonymous=True)
    rospy.Subscriber('/mybot/camera/image_raw', Image, read_image_callback) #Type Image : height width data[] ...

    rospy.spin()



if __name__ == '__main__':
    try:
        camera_listener()

    except rospy.ROSInterruptException:
        pass
