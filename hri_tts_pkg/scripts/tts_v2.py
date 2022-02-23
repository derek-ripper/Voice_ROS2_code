#!/usr/bin/env python3
################################################################################
#Author  : Derek Ripper
#Created : 22 Feb 2022
#Purpose : To listen on topic /stt and to speak 

################################################################################
# Origin:
#   https://www.geeksforgeeks.org/convert-text-speech-python/
#
# Required support is:
#   pip install     gTTS            # google TTS API
#   sudo apt-get update -y
#   sudo apt-get -y install mpg321  # command line mpeg plater
#
################################################################################
# import the required google module for text
# to speech conversion
from gtts import gTTS

import rclpy
from   rclpy.node   import Node
from   std_msgs.msg import String
import os

# simple routine to use instead of print() -
# To get colour coded messages for ERROR,INFO,RESULT, etc
import  py_utils_pkg.text_colours     as TC
prt = TC.Tc()
cname = "tts_v2-"

class Sayit(Node):
    def __init__(self):
        super().__init__('tts_node')
        self.language = 'en'
        self.accent   = 'co.uk'
        self.slow     = 'False'

        self.listen   = self.create_subscription(String,'/stt',self.listen_callback,10)

    def listen_callback(self, msg):
        myobj = gTTS(text=msg.data, lang=self.language, tld=self.accent, slow=self.slow)
        myobj.save("TheTextToSay.mp3")
        # Playing the converted file
        os.system("mpg321 TheTextToSay.mp3 2>null")
        prt.debug(cname+"Speaking is complete!")

def main(args=None):
    rclpy.init(args=args)

    mynode  = Sayit()
    rclpy.spin(mynode)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    mynode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        prt.blank()

        prt.warning(cname+" Cancelelld by user !")
