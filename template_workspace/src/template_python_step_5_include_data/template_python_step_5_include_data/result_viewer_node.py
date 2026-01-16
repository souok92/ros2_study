"""
ROS2 node for displaying inference results.

This node subscribes to inference results and displays them in a formatted way.
Demonstrates the subscriber pattern in ROS2.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ResultViewerNode(Node):
    """
    ROS2 node that subscribes to and displays inference results.

    This node demonstrates how to create a subscriber that receives
    and processes messages from another node.
    """

    def __init__(self):
        super().__init__('result_viewer_node')

        # Create subscription to inference results
        self.subscription = self.create_subscription(
            String,
            'inference_result',
            self.result_callback,
            10
        )

        self.get_logger().info('ResultViewerNode ready! Waiting for inference results...')

    def result_callback(self, msg):
        """
        Callback function that processes received inference results.

        Args:
            msg: String message containing inference results
        """
        # Print separator for readability
        self.get_logger().info('=' * 70)
        self.get_logger().info('📊 INFERENCE RESULT:')
        self.get_logger().info('-' * 70)

        # Print the inference result
        for line in msg.data.split('\n'):
            self.get_logger().info(line)

        self.get_logger().info('=' * 70)


def main(args=None):
    rclpy.init(args=args)

    try:
        node = ResultViewerNode()
        rclpy.spin(node)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
