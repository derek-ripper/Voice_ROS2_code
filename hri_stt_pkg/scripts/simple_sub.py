#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import  py_utils_pkg.text_colours     as TC
cname = 'simple_sub'
# simple routine to use instead of print() - to get colour coded messages for ERROR,INFO,RESULT, etc
prt = TC.Tc()

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'stt',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        prt.debug(cname + "In subscriber callback6")
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    prt.info(cname + "In sumple suscriber!")
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
