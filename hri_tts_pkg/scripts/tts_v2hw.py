#!/usr/bin/env python3
################################################################################
# Filename: tts_v2hw.py
# Author  : Derek Ripper
# Created : 30 Sep 2022
# Purpose : To listen for text string on topic "/tts" and to say it
#                AND To avoid robot listening to it's self:
#                - the mic is deavtivated  the spk is activated
#                - speech is spoken
#                - the mic is activated    the spk is deactivated
################################################################################
# Reference:
#   https://www.geeksforgeeks.org/convert-text-speech-python/
#
# Required support is:
#
#   sudo pip install     gTTS            # google TTS API - NO registration/Licence required.                                         
#   sudo apt-get update -y
#   sudo apt-get -y install mpg321  # This isn a command line mpeg player
#
################################################################################
# Updates:
# ??/???/???? by ????? - info ......
################################################################################
# import the required google module for "text to speech" conversion
from gtts import gTTS
import rclpy
from   rclpy.node      import Node
from   std_msgs.msg import String
# import alsaaudio
import alsa_audio as actrl

import os
# simple routine to use instead of print() -
# To get colour coded messages for ERROR,INFO,RESULT, etc
import  py_utils_pkg.text_colours     as TC
prt = TC.Tc()

cname = " tts_v2hw-"
class speak(Node):
    def __init__(self):
        super().__init__('tts_node')
        self.ac           = actrl.audio_control()
        self.language = 'en'
        self.accent     = 'co.uk'
        self.slow        = 'False'

        self.listen         = self.create_subscription(
            String,'/tts',self.listen_callback,10)

        # self.listen   # to avoid unused variable message
        prt.debug(cname+"TTS - Leave init")
        return

    def listen_callback(self, msg):
        txt = msg.data
        #### Switch OFF microphone
        self.ac.mic_off()
        # Create the text file to be spoken
        myobj=gTTS(text=txt, lang=self.language, tld=self.accent,slow=self.slow)

        # NB arg value for file cannot be a variable name!
        myobj.save('TheTextToSay.mp3')

        # Playing the converted file
        rc1 = os.system("mpg123  -q  TheTextToSay.mp3")
        rc2 = os.system("rm  TheTextToSay.mp3")
        if(rc1 != 0 or rc2 != 0):
            prt.error(cname+"rtn code rc1 - mpg123: "+str(rc1))
            prt.error(cname+"rtn code rc2 - rm  cmd: "+str(rc2))
        
        #### Switch ON microphone
        self.ac.mic_on()
        prt.info(cname+"Speaking is complete!!!")
        prt.blank()
        return
##### end of class def for "speak"

def main(args=None):
    rclpy.init(args=args)
    prt.info(cname + "*********************** in main")
    tts_node  = speak()
    rclpy.spin(tts_node)

if  __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        prt.blank()

        prt.warning(cname+" Cancelelld by user !")
    
