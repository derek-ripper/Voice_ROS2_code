#!/usr/bin/env python3
###############################################################################
# Filename: chat.py
# Created : 23 Feb 2022
# Author  : Derek Ripper
# Purpose : 1- To test the speech modules  stt aand tts.
#           2- also to sort out the controlling of the robot NOT repeating what
#             it has just said!!
#
###############################################################################
# Updates:
# ??/???/???? by ????? -
#
################################################################################
import rclpy
from   rclpy.node    import Node
from   std_msgs.msg  import String

# import python general utils
import  py_utils_pkg.text_colours     as TC
# simple routine to use instead of print() - to get colour coded messages for
# ERROR,INFO,RESULT, messages, etc
prt = TC.Tc()

#code name - to be used in  warning/error msgs.
cname = "chat- "

class Chat(Node):

    def __init__(self):
        super().__init__('my_node')
        self.subscription = self.create_subscription(
            String, '/stt', self.listener_callback,  10)

        self.pub_text      = self.create_publisher(
            String, '/tts',        10)

    def listener_callback(self, msg):
        prt.debug(cname + "In listener subscriber callback")
        self.get_logger().info('I heard: "%s"' % msg.data)
        #self.set_stt_switch('OFF')
        self.speakout(msg.data)
        #self.set_stt_switch('ON')
        return

    def speakout(self,text2speak):
        prt.debug(cname+'ENTER def speakout ')
        msg      = String()
        msg.data ="You said "+ text2speak
        self.pub_text.publish(msg)
        prt.debug(cname+'LEAVE def  speakout ')


def main(args=None):
    rclpy.init(args=args)
    prt.debug(cname+"Enter def main")

    waffle = Chat()
    rclpy.spin(waffle)


    rclpy.shutdown()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)s

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:

        rclpy.shutdown()

        prt.blank()
        prt.warning(cname+" Cancelelld by user !")
