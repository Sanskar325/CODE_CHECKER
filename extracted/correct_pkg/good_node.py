import rclpy
from rclpy.node import Node
import time

class GoodNode(Node):
    def __init__(self):
        super().__init__('good_node')
        self.create_publisher(str, 'topic', 10)

    def loop(self):
        while True:
            time.sleep(1) # Has sleep, so it's safe!
