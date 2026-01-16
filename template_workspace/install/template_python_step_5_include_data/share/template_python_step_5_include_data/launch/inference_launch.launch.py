"""
Launch file for running inference node and result viewer together.

This demonstrates how to launch multiple nodes that communicate via topics.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Inference node - runs AI model and publishes results
        Node(
            package='template_python_step_5_include_data',
            executable='inference_node',
            name='inference_node',
            output='screen',
        ),
        # Result viewer node - subscribes to results and displays them
        Node(
            package='template_python_step_5_include_data',
            executable='result_viewer_node',
            name='result_viewer_node',
            output='screen',
        ),
    ])
