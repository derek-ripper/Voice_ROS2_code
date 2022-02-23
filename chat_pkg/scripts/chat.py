#!/usr/bin/python3
###############################################################################
# Filename: chat.py
# Created : 23 Feb 2022
# Author  : Derek Ripper
# Purpose : 1- To test teh speech modules  stt aand tts.
#           2- also to sort out the controlling of the rbot NOT repeating what
#             it has just said!
#
# History:
#       None
###############################################################################
# Updates:
#
################################################################################
import rclpy
from rclpy.node     import Node
from std_msgs.msg   import String
import speech_recognition as sr # sudo pip install SpeechRecognition && sudo apt-get install python-pyaudio

# import python_support_library.text_colours     as
import  py_utils_pkg.text_colours     as TC
# simple routine to use instead of print() - to get colour coded messages for ERROR,INFO,RESULT, etc
prt = TC.Tc()

#code name - to be used in any warning/error msgs.
cname = "chat- "

class Chat(Node):

    def __init__(self):
        super().__init__('Speech_Rec')
        prt.debug(cname+"in chat.py")

        self.listen   = self.create_subscription(String,'/stt',
                        self.listen_callback,10)
        self.publish_ = self.create_publisher(String, '/tts', 10)

    def listen_callback(self,msg):
        self.decode_user_request(msg.data)

    def decode_user_request(self,txt):
        txt=txt.upper()
        result = txt.find("ABORT")
        if result == -1 :
            prt.info(cname+"Just carry on as no words foun that I know about!")
        else:
            prt.warning(cname +"KILL Node")

def main(args=None):
    rclpy.init(args=args)
    waffle = Chat()
    rclpy.spin(waffle)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        waffle.destroy_node()
        rclpy.shutdown()

        prt.blank()
        prt.warning(cname+" Cancelelld by user !")
