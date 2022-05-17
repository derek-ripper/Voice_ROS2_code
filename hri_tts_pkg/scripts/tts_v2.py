#!/usr/bin/env python3
################################################################################
# Filename: tts_v2.py
# Author  : Derek Ripper
# Created : 22 Feb 2022
# Purpose : To listen for text string on topic "/tts" and to say it
#           To avoid robit listening to it's self the subscriber for /tts
#            is deleted before speech is started. Then it is re-establshed.
#
################################################################################
# Reference:
#   https://www.geeksforgeeks.org/convert-text-speech-python/
#
# Required support is:
#   pip install     gTTS            # google TTS API - NO registration/Licence
#                                                      needed.
#   sudo apt-get update -y
#   sudo apt-get -y install mpg321  # command line mpeg player
#
################################################################################
# Updates:
# ??/???/???? by ????? -
#
################################################################################

# import the required google module for "text to speech" conversion
from gtts import gTTS

import rclpy
from   rclpy.node   import Node
from   std_msgs.msg import String

import os

# simple routine to use instead of print() -
# To get colour coded messages for ERROR,INFO,RESULT, etc
import  py_utils_pkg.text_colours     as TC
prt = TC.Tc()

cname = " tts_v2-"

class Sayit(Node):
    def __init__(self):
        super().__init__('tts_node')
        self.language = 'en'
        self.accent   = 'co.uk'
        self.slow     = 'False'

        self.listen         = self.create_subscription(
            String,'/tts',self.listen_callback,10)

        self.pub_stt_switch = self.create_publisher(
            String, '/stt_switch', 10)
        # self.listen   # to avoid unused variable message
        prt.debug(cname+"TTS - Leave init")

    def listen_callback(self, msg):
        txt = msg.data
        prt.debug(cname+"TOPIC: /tts contains: " + txt)

        # kill MinimalSubscriber
        ###del self.listen



        # Create the text file to be spoken
        myobj = gTTS(text=txt, lang=self.language, tld=self.accent, slow=self.slow)

        # NB arg value for file cannot be a variable name!
        myobj.save('TheTextToSay.mp3')

        # Playing the converted file
        prt.debug(cname+'playing mp3 file now?')

        # self.set_stt_switch("kill")
        rc = os.system("mpg123  TheTextToSay.mp3")
        rc = os.system("rm  TheTextToSay.mp3")
        # self.set_stt_switch("live")

        prt.debug(cname+"rtn code: "+str(rc))
        prt.debug(cname+"Speaking is complete!!!")
        prt.todo(cname+'Add "rm" command for mp3 file')

        # re-establish subscriber
        ###self.listen         = self.create_subscription(
        ###    String,'/tts',self.listen_callback,10)
    # def set_stt_switch(self,on_OR_off ):
    #     arg = String()
    #     arg.data = on_OR_off
    #     self.pub_stt_switch.publish(arg)

def main(args=None):
    rclpy.init(args=args)
    prt.info(cname + "*********************** in main")
    tts_node  = Sayit()
    rclpy.spin(tts_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    #tts_node.destroy_node()
    #rclpy.shutdown()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        prt.blank()

        prt.warning(cname+" Cancelelld by user !")
