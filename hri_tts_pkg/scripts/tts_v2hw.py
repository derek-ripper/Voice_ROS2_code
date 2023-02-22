#!/usr/bin/env python3
################################################################################
# Filename: tts_v2hw.py
# Author  : Derek Ripper
# Created : 30 Sep 2022
# Purpose : To listen for text string on topic "/hearts/tts" and to say it
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
#   sudo pip install     gTTS       # google TTS API - NO registration/Licence required.                                         
#   sudo apt-get update -y
#   sudo apt-get -y install mpg321  # This is a command line mpeg player
#
################################################################################
# Updates:
# ??/???/???? by ????? - info ......
################################################################################
# import the required google module for "text to speech" conversion
from gtts import gTTS

import rclpy
from   rclpy.node   import Node
from   std_msgs.msg import String
# import 
import py_utils_pkg.alsa_audio as actrl # alsa control for mic and speaker
import os

import  py_utils_pkg.text_colours as TC #use instaed of print() for coloured text
prt = TC.Tc()

cname = " tts_v2hw- "
class speak(Node):
    def __init__(self):
        super().__init__('tts_node')
        self.ac         = actrl.Audio_control()
        self.language   = 'en'
        self.accent     = 'co.uk'
        self.slow       = 'False'
        self.declare_parameter("SR_MIC_VOLUME",       80     ) # % for microphone volume
        self.mic_volume       = self.get_parameter(
            'SR_MIC_VOLUME').get_parameter_value().integer_value 
            
        self.listen         = self.create_subscription(
            String,'/hearts/tts',self.listen_callback,10)
        prt.debug(cname + "Microphone volume (%)    : " + str(self.mic_volume))

    def listen_callback(self, msg):
        txt = msg.data
        #### Switch OFF microphone
        ### now done before leaving stt_v2.py -      self.ac.mic_off()

        prt.result("SPEAKING: "+txt)
        # Create the mp3 file that is to be spoken
        myobj=gTTS(text=txt, lang=self.language, tld=self.accent,slow=self.slow)

        # NB arg value for file cannot be a variable name!
        myobj.save('TheTextToSay.mp3')

        # Playing the converted file
        rc1 = os.system("mpg123  -q  TheTextToSay.mp3 2>&1 /dev/null")
        rc2 = os.system("rm  TheTextToSay.mp3")
        if(rc1 != 0 or rc2 != 0):
            prt.error(cname+"rtn code rc1 - mpg123 : "+str(rc1))
            prt.error(cname+"rtn code rc2 - rm  cmd: "+str(rc2))
        
        #### Switch microphone ON & speaker OFF
        self.ac.mic_on()
        self.ac.mixer_mic.setvolume(self.mic_volume) # percentage for voice capture
       
        return
##### end of class def for "speak"

def main(args=None):
    rclpy.init(args=args)
   
    tts_node  = speak()
    rclpy.spin(tts_node)

if  __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        prt.blank()

        prt.warning(cname+" Cancelelld by user !")
    
