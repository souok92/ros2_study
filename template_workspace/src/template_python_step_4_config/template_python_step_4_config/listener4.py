import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimpleListener(Node):
    def __init__(self):
        super().__init__('simple_listener')

        # === Original code (hardcoded) ===
        # self.subscription = self.create_subscription(
        #     String,
        #     'chatter',
        #     self.listener_callback,
        #     10)

        # === Using parameters from config ===
        # Declare parameters with default values
        self.declare_parameter('topic_name', 'chatter')
        self.declare_parameter('queue_size', 10)

        # Get parameter values
        topic = self.get_parameter('topic_name').get_parameter_value().string_value
        queue_size = self.get_parameter('queue_size').get_parameter_value().integer_value

        # Create subscription with parameters
        self.subscription = self.create_subscription(
            String,
            topic,
            self.listener_callback,
            queue_size)

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = SimpleListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
