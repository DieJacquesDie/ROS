#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the main node of the robot. It is used to follow yellow or red lines, stop if an obstacle is encountered, open blue doors and avoid orange obstacles. Camera datas are mainly used.
"""

import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8, Bool

#initialize default Twist message
cmd = Twist()
cmd.linear.x = 0
cmd.linear.y = 0
cmd.linear.z = 0
cmd.angular.x = 0
cmd.angular.y = 0
cmd.angular.z = 0

#a few global variables
bridge = CvBridge()

timer = 0
garage_open = 0

stop = 0

cx_orange=None
out=None

#pub publishes on /cmd_vel to control the robot's movements
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
#pub_garage publishes on /Garage_Door_Opener to open the blue door when needed
pub_garage = rospy.Publisher("/Garage_Door_Opener", Bool, queue_size=10)


def read_image_callback(msg):

    global bridge
    global pub
    global pub_garage
    global timer
    global garage_open
    global out
    global cx_orange

#define yellow red green blue and oranges masks
    cv_image=bridge.imgmsg_to_cv2(msg,"bgr8")
    hsv_image=cv2.cvtColor(cv_image,cv2.COLOR_RGB2HSV)
    mask_yellow=cv2.inRange(hsv_image,(70,200,200),(100,255,255))
    mask_red=cv2.inRange(hsv_image,(100,100,100),(150,255,255))
    mask_green=cv2.inRange(hsv_image,(40,200,200),(80,255,255))
    mask_blue=cv2.inRange(hsv_image,(0,50,50),(10,255,255))
    mask_orange=cv2.inRange(hsv_image,(100,50,50),(120,255,255))
#cuting yellow mask in top right and left parts to detect line split
    top_mask_yellow = mask_yellow[250:350, 375:425].copy()
    right_mask_yellow = mask_yellow[700:800, 700:800].copy()
    left_mask_yellow = mask_yellow[700:800, 0:100].copy()
    sum_yellow_top=np.sum(top_mask_yellow)
    sum_yellow_right=np.sum(right_mask_yellow)
    sum_yellow_left=np.sum(left_mask_yellow)

    bottom_mask_yellow = mask_yellow[400:800, 0:800].copy()
    sum_yellow=np.sum(bottom_mask_yellow)

    bottom_mask_red = mask_red[400:800, 0:800].copy()
    sum_red=np.sum(bottom_mask_red)
    bottom_mask_green = mask_green[400:800, 0:800].copy()
    sum_green=np.sum(bottom_mask_green)
    bottom_mask_blue = mask_blue[300:800, 0:800].copy()
    sum_blue=np.sum(bottom_mask_blue)
    top_mask_orange = mask_orange[0:300, 0:800].copy()
    sum_orange=np.sum(top_mask_orange)


#actual mask used to compute line followage
    mask=bottom_mask_red+bottom_mask_yellow+bottom_mask_green

#compute moments of the followed line
    M = cv2.moments(mask)
    if M['m00'] > 0:
      cx=int (M['m10']/M['m00'])
      cy=int (M['m01']/M['m00'])
    print("image moments :",cx,cy)

#compute orange obstacles moments
    M_orange = cv2.moments(top_mask_orange)
    if M_orange['m00'] > 0:
      cx_orange=int (M_orange['m10']/M_orange['m00'])

    if 780 > cx_orange > 400:
	out=1
    elif 20 < cx_orange <= 400:
	out=-1

#define the error between the robot's orientation and the line to follow
    err=float(cx-400)

#command modes according to the line (red or yellow, green ending), and path to chose according to obstacles using moments when the line is splitting
    if stop == 0:
        if sum_green > 0 and (sum_red+sum_yellow) == 0:
	    cmd.linear.x = 0
	    cmd.angular.z = 0
        elif sum_red >= sum_yellow:
	    set_cmd_red(err,cy)
        else:
	    if cx_orange > 400 and (sum_yellow_left > 50 and sum_yellow_right > 50) and sum_orange > 1000000:
		cmd.linear.x = 0.05
	        cmd.angular.z = 0.5
		out=1
		print("Orange obstacle detected at the right, turning left")
	    elif cx_orange < 400 and (sum_yellow_left > 50 and sum_yellow_right > 50) and sum_orange > 1000000:
		cmd.linear.x = 0.05
	        cmd.angular.z = -0.5
		out=-1
		print("Orange obstacle detected at the left, turning right")
	    elif (sum_yellow_left > 50 and out == 1) or (sum_yellow_right > 50 and out == -1):
		cmd.linear.x = 0.05
	        cmd.angular.z = out*0.5
	    else:
	        set_cmd_yellow(err,cy)
		cx_orange=None
    else:
	cmd.linear.x = 0
	cmd.angular.z = 0


#detect blue garage doors, open/close them if needed
    if sum_blue > 100:
	print("Opening door")
	pub_garage.publish(1)
	garage_open = 1
    elif garage_open:
	timer+=1
	print(timer)
	if timer>50:
	    print("Closing door")
	    timer=0
	    garage_open=0
	    pub_garage.publish(0)

#publish defined command to /cmd_vel
    print(cmd)
    pub.publish(cmd)

#show image mask in a separate window
    mask=cv2.circle(mask, (cx,cy), 80, (255,255,0), 3)
    cv2.imshow("Image window",mask)
    cv2.waitKey(1)



def set_cmd_yellow(err,cy):
#set command when yellow line is detected
    global cmd

    if err>0:
	cmd.linear.x = (1-(abs(err)/400))*0.15
	cmd.angular.z = (abs(err)/400)*-0.8
    if err<0:
	cmd.linear.x = (1-(abs(err)/400))*0.15
	cmd.angular.z = (abs(err)/400)*0.8
#when very steep curves are detected
    if cy > 350:
	cmd.linear.x = 0.05
	cmd.angular.z *= 1.5


    if cy > 380:
	cmd.linear.x = 0
	cmd.angular.z *= 2


def set_cmd_red(err,cy):
#set command when red line is detected
    global cmd

    if err>0:
	cmd.linear.x = (1-(abs(err)/400))*0.075
	cmd.angular.z = (abs(err)/400)*-0.4
    else:
	cmd.linear.x = (1-(abs(err)/400))*0.075
	cmd.angular.z = (abs(err)/400)*0.4
    if cy > 350:
	cmd.linear.x = 0.05
	cmd.angular.z *= 1.5
    if cy > 380:
	cmd.linear.x = 0
	cmd.angular.z *= 2

def read_stop_callback(msg):
#set stop variable using /emergency_stop topic
    global stop

    if msg.data == 1 :
	stop = 1
    else:
	stop = 0



def camera_listener():
#initialize node "camera_listener" subscribing to 2 topics
    rospy.init_node('camera_listener', anonymous=True)
    rospy.Subscriber('/emergency_stop', Int8, read_stop_callback)
    rospy.Subscriber('/camera/image_raw', Image, read_image_callback)

    rospy.spin()



if __name__ == '__main__':
    try:
        camera_listener()

    except rospy.ROSInterruptException:
        pass
