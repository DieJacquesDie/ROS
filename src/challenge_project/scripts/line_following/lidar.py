#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- This is simple node using Lidar datas to publish on a topic "/emergency_stop"
- if an obstacle is detected in the front (1) or back (2) at less than 0.3 meters.
- If no obstacle is being detected, 0 is published.
"""

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int8



pub = rospy.Publisher("/emergency_stop", Int8, queue_size=10)


def read_distance_callback(msg):
#computes front and back mean ranges using a 20 degrees radius then publish adequate message to /emergency_stop

    global pub

    front_range=np.mean(np.concatenate((msg.ranges[0:10],msg.ranges[350:360]),axis=None))
    back_range=np.mean(msg.ranges[170:190])

    if front_range <= 0.3:
	pub.publish(1)
	print("obstacle in front at "+ str(front_range) + " m")

    elif back_range <= 0.3:
	pub.publish(2)
	print("obstacle behind at "+ str(back_range) +" m")

    else :
	pub.publish(0)
	print("front "+ str(front_range) +", back "+ str(back_range))




def lidar_listener():
#starts the subscriber node using datas from /scan

    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, read_distance_callback)

    rospy.spin()



if __name__ == '__main__':
    try:
        lidar_listener()

    except rospy.ROSInterruptException:
        pass
