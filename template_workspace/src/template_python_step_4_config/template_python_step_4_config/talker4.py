import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimpleTalker(Node):
    def __init__(self):
        super().__init__('simple_talker')

        # === Original code (hardcoded) ===
        # self.publisher = self.create_publisher(String, 'chatter', 10)
        # self.timer = self.create_timer(1.0, self.timer_callback)
        # self.count = 0

        # === Using parameters from config ===
        # Declare parameters with default values
        self.declare_parameter('publish_frequency', 1.0)
        self.declare_parameter('topic_name', 'chatter')
        self.declare_parameter('message_prefix', 'Hello World')
        self.declare_parameter('queue_size', 10)

        # Get parameter values
        freq = self.get_parameter('publish_frequency').get_parameter_value().double_value
        topic = self.get_parameter('topic_name').get_parameter_value().string_value
        self.prefix = self.get_parameter('message_prefix').get_parameter_value().string_value
        queue_size = self.get_parameter('queue_size').get_parameter_value().integer_value

        # Create publisher and timer with parameters
        self.publisher = self.create_publisher(String, topic, queue_size)
        self.timer = self.create_timer(1.0 / freq, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        # === Original code ===
        # msg.data = f'Hello World: {self.count}'

        # === Using parameter ===
        msg.data = f'{self.prefix}: {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = SimpleTalker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
