"""
Launch file for running the 3-node image classification pipeline.

This demonstrates a complete publisher-subscriber pipeline:
1. Image publisher node - publishes image paths
2. Inference node - subscribes to image paths, runs AI inference, publishes results
3. Result viewer node - subscribes to results and displays them
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Image publisher node - publishes image paths from data folder
        Node(
            package='template_python_step_5_include_data',
            executable='image_publisher_node',
            name='image_publisher_node',
            output='screen',
        ),
        # Inference node - subscribes to image paths, runs AI inference, publishes results
        Node(
            package='template_python_step_5_include_data',
            executable='inference_node',
            name='inference_node',
            output='screen',
        ),
        # Result viewer node - subscribes to inference results and displays them
        Node(
            package='template_python_step_5_include_data',
            executable='result_viewer_node',
            name='result_viewer_node',
            output='screen',
        ),
    ])
