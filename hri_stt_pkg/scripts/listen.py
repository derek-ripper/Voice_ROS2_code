#!/usr/bin/env python3
###############################################################################
# Filename: listen_v2.py
# Created : 01 Jan 2022
# Author  : Derek Ripper
# Purpose : 1- listen to a range of topics but primarily for "stt" code testing

# History:
# Original code was written in 2017/2018
###############################################################################
# Updates:
# 01 Jan  2022 Derek - Code updated for ROS2 and Python3
#
###############################################################################
import rclpy
import sys

from rclpy.node     import Node
from std_msgs.msg   import String, Bool

### from sound_play.msg import SoundRequest

import  py_utils_pkg.text_colours     as TC # print text in various colours/sstyles
# simple routine to use instead of print() - to get colour coded messages for ERROR,INFO,RESULT, etc
prt = TC.Tc()
#code name - to be used in any warning/error msgs.
cname = " listen_v2: "

class Listen(Node):

    def __init__(self):
        super().__init__('Listen_Node')
        prt.info(cname + "in __init__ for listen")
    #    self.sub4 = self.create_subscription(String, "/stt",  self.callback4, 10)
        #self.run_mode= rclpy.get_param("SR_TH")
        #node.get_logger().info(cname+": Run Mode is: "+self.run_mode)

    # def listeners(self):
    #     # set up subscriber for returned TOPIC
    #     self.sub0 = self.create_subscription(String, "Wav_FileIn",  self.callback0, 10)
    #
    #
    #     # set up subscriber for returned TOPIC
    #     self.sub1 = self.create_subscription(String, "Text_4_CFR",  self.callback1, 10)
    #
    #     # set up subscriber for returned TOPIC
    #     self.sub2 = self.create_subscription(String, "CFR_Out",     self.callback2, 10)
    #
    #     # set up subscriber for returned TOPIC
    #     ### self.sub3 = self.create_subscription(String, "robotsound", SoundRequest, self.callback3, 10)
    #
          # set up subscriber for returned TOPIC
        self.sub4 = self.create_subscription(String, "/stt",  self.callback4, 10)
    #
    #     # set up subscriber for returned TOPIC
    #     self.sub5 = self.create_subscription(String, "/hearts/tts_finished",  self.callback5,10)
    #
    #     # set up subscriber for returned TOPIC
    #     self.sub6 = self.create_subscription(String, "/hearts/tts",  self.callback6, 10)
    #
    #
    #
    #
    # def callback0(self,data):
    #     print("callback #0")
    #     self.out0=data.data
    #     node.get_logger().info(cname+":\n Wav_Filin     data.data is: "+self.out0)
    #
    # def callback1(self,data):
    #     print("callback #1")
    #     self.out1=data.data
    #     node.get_logger().info(cname+":\n Text_4_CFR -  data.data is: "+self.out1)
    #
    # def callback2(self,data):
    #     print("callback #2")
    #     self.out2=data.data
    #     node.get_logger().info(cname+":\n CFR_OUT    -  data.data is: "+self.out2)
    #
    # def callback3(self,data):
    #     print("callback #3")
    #     self.out3=data.arg
    #     print(type(data.arg))
    #     node.get_logger().info(cname+":\n robotsound    -  data.SAY is: "+self.out3)

    def callback4(self,data):
        print("callback #4")
        self.out4=data.data
        prt.result(cname +  " the answer")
        #node.get_logger().info(cname+":\n hearts/stt -     data.data is: "+self.out4)

    # def callback5(self,data):
    #     print("Callback #5")
    #     self.out5=data.data
    #     node.get_logger().info(cname+":\n hearts/tts_finished -     data.data is: "+self.out5)
    #
    # def callback6(self,data):
    #     print("Callback #6")
    #     self.out6=data.data
    #     node.get_logger().info(cname+":\n hearts/tts_ -     data.data is: "+self.out6)

def main(args=None):
    rclpy.init(args=args)
    my_node=Listen()

    rclpy.spin(my_node)

if __name__ == '__main__':
    main()
