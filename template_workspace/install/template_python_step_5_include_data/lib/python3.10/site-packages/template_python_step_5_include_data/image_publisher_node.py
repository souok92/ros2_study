"""
ROS2 node for publishing image paths.

This node cycles through test images and publishes their paths to a topic.
Other nodes can subscribe to this topic to process the images.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory
import os


class ImagePublisherNode(Node):
    """
    ROS2 node that publishes image paths from a directory.

    This node demonstrates separation of concerns by only handling
    image path publishing, not image processing.

    Publishes to: /image_path (String) - full path to image file
    """

    def __init__(self):
        super().__init__('image_publisher_node')

        # Get package share directory and images folder
        pkg_dir = get_package_share_directory('template_python_step_5_include_data')
        self.images_dir = os.path.join(pkg_dir, 'data')

        # Create publisher for image paths
        self.publisher = self.create_publisher(String, 'image_path', 10)

        # Create timer for periodic publishing (every 10 seconds)
        self.timer = self.create_timer(10.0, self.publish_image_path)

        # Index for cycling through images
        self.current_image_index = 0

        # Get list of images once
        self.image_list = [
            f for f in os.listdir(self.images_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif'))
        ]

        if not self.image_list:
            self.get_logger().error('No images found in data directory!')
            raise RuntimeError('No images found')

        self.get_logger().info(f'ImagePublisherNode ready! Found {len(self.image_list)} images')

    def publish_image_path(self):
        """
        Publish the path of the next image in the sequence.

        This is called periodically by the timer.
        """
        if not self.image_list:
            return

        # Get current image
        image_name = self.image_list[self.current_image_index]
        image_path = os.path.join(self.images_dir, image_name)

        # Publish image path
        msg = String()
        msg.data = image_path

        self.publisher.publish(msg)
        self.get_logger().info(
            f'📤 Published: {image_name} ({self.current_image_index + 1}/{len(self.image_list)})'
        )

        # Update index for next image
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)


def main(args=None):
    rclpy.init(args=args)

    try:
        node = ImagePublisherNode()
        rclpy.spin(node)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
