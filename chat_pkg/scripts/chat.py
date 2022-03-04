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
        self.pub_text_ = self.create_publisher(String, '/stt', 10)
        self.pub_toggle= self.create_publisher(String, '/stt_toggle', 10)
        #self.timer1_=self.create_timer(2, self.speakout)

    # def set_stt_switch(self,on_OR_off):
    #     on_OR_off = on_OR_off.upper()
    #
    #     switch = String()
    #     switch.data = on_OR_off
    #
    #     self.pub_toggle.publish(switch)
    #
    #     return


    def speakout(self,text2speak):
        prt.debug(cname+'ENTER def  speakout ')
        msg = String()
        msg.data = text2speak
        self.pub_text_.publish(msg)
        prt.debug(cname+'LEAVE def  speakout ')

    def chatting(self,text2say):
        prt.debug(cname+'Enter def  chatting ')
        msg = String()
        msg.data = text2say
        prt.debug(cname+'msg.data is: '  + msg.data)
        #self.set_stt_switch ("OFF")

        try:
            self.pub_text_.publish(msg)

            #self.set_stt_switch ("ON")
        except:
            prt.error(cname+"pubish call to stt went wrong!")
        # doitagain = False
        # while doitagain == True:
        #     prt.debug(cname+'Eneter def  chatting doitagain loop ')
        #     #doitagain = False
        #     msg.data = 'Speak now please'
        #     self.pub_text_.publish(msg)

        prt.debug(cname+"2nd pub attempt")
        self.pub_text_.publish(msg)
        prt.debug(cname+'Leave def  chatting ')

def main(args=None):
    rclpy.init(args=args)
    prt.debug(cname+"Enter main")

    waffle = Chat()

    text2speak = "Last hope now"

    waffle.speakout(text2speak)
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
