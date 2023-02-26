#!/usr/bin/env python3
###############################################################################
# Filename: chat.py
# Created : 23 Feb 2022
# Author  : Derek Ripper
# Purpose : 1- To test the speech modules  stt aand tts.
#
#
###############################################################################
# Updates:
# ??/???/???? by ????? -
#
################################################################################
import rclpy
from   rclpy.node    import Node
from   std_msgs.msg  import String

import xmasqa                    as xmasqa # contans questions with multiple answers
import py_utils_pkg.text_colours as TC #use instaed of print() for coloured text

prt = TC.Tc()

#code name - to be used in  warning/error msgs.
cname = "chat- "

class Chat(Node):

    def __init__(self):
        super().__init__('my_node')
        self.qa           = xmasqa.QandA()
        self.subscription = self.create_subscription(
            String, '/hearts/stt', self.listener_callback,  10)

        self.pub_text      = self.create_publisher(
            String, '/hearts/tts',        10)
        return

    def listener_callback(self, msg):
        txt = msg.data

        # pass text to get an appropriate answer
        anstxt = self.qa.process_answer(txt)
        self.speakout(anstxt)
        return

    def speakout(self,text2speak):
        msg      = String()
        msg.data = text2speak
        self.pub_text.publish(msg)
        return

def main(args=None):
    rclpy.init(args=args)

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
