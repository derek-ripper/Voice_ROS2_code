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

# import python_support_library.text_colours     as
import  py_utils_pkg.text_colours     as TC
# simple routine to use instead of print() - to get colour coded messages for ERROR,INFO,RESULT, etc
prt = TC.Tc()

#code name - to be used in any warning/error msgs.
cname = "chat- "

class Chat(Node):

    def __init__(self):
        super().__init__('Speech_Rec')
        prt.debug(cname+"Enter __init__ chat.py")

        self.listen   = self.create_subscription(String,'/stt',
                        self.listen_callback,10)

        self.publish_ = self.create_publisher(String, '/tts', 10)

        prt.debug(cname+'Leave __init__ ')

    def listen_callback(self,msg):
        self.answer = (msg.data)

    def chatting(self):
        prt.debug(cname+'Enter def  chatting ')
        txt = String()
        txt.data = 'Hi I will now ask you to speak and then I will repeat back to you'
        self.publish_.publish(txt)
        doitagain = True

        while doitagain == True:
            prt.debug(cname+'Eneter def  chatting doitagain loop ')
            doitagain = False
            txt.data = 'Speak now please'
            self.publish_.publish(txt)

        prt.debug(cname+'Leave def  chatting ')

def main(args=None):
    rclpy.init(args=args)
    waffle = Chat()
    waffle.chatting()
    rclpy.spin(waffle)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)s

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        waffle.destroy_node()
        rclpy.shutdown()

        prt.blank()
        prt.warning(cname+" Cancelelld by user !")
