#!/usr/bin/env python

import rospy
from std_msgs.msg import String #type du message

def subscriber():
    sub = rospy.Subscriber('string_publish', String, callback_function)#nom du topic, type du message, callback

    rospy.spin()

def callback_function(message):
    rospy.loginfo("I received: %s"%message.data)

if __name__ == "__main__":
    rospy.init_node("simple_subscriber")
    subscriber()
