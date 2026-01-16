import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import String


class DynamicTalker(Node):
    def __init__(self):
        super().__init__('dynamic_talker')

        # === Declare parameters with default values ===
        self.declare_parameter('publish_frequency', 1.0)
        self.declare_parameter('message_prefix', 'Hello World')

        # Get initial parameter values
        self.freq = self.get_parameter('publish_frequency').get_parameter_value().double_value
        self.prefix = self.get_parameter('message_prefix').get_parameter_value().string_value

        # Create publisher and timer
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0 / self.freq, self.timer_callback)
        self.count = 0

        # === Register parameter callback for runtime changes ===
        self.add_on_set_parameters_callback(self.parameter_callback)

        self.get_logger().info(
            f'DynamicTalker started with freq={self.freq}Hz, prefix="{self.prefix}"'
        )
        self.get_logger().info(
            'Try: ros2 param set /dynamic_talker publish_frequency 5.0'
        )

    def parameter_callback(self, params):
        """
        Called when parameters are changed at runtime.
        This allows the node to respond to parameter updates without restarting.
        """
        for param in params:
            if param.name == 'publish_frequency' and param.type_ == Parameter.Type.DOUBLE:
                new_freq = param.value

                # Validate the new frequency
                if new_freq <= 0.0:
                    self.get_logger().error(f'Invalid frequency: {new_freq}. Must be > 0')
                    return SetParametersResult(successful=False)

                # Update timer with new frequency
                self.timer.cancel()
                self.timer = self.create_timer(1.0 / new_freq, self.timer_callback)
                self.freq = new_freq

                self.get_logger().info(f'Updated publish_frequency to {new_freq}Hz')

            elif param.name == 'message_prefix' and param.type_ == Parameter.Type.STRING:
                self.prefix = param.value
                self.get_logger().info(f'Updated message_prefix to "{self.prefix}"')

        return SetParametersResult(successful=True)

    def timer_callback(self):
        msg = String()
        msg.data = f'{self.prefix}: {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = DynamicTalker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
