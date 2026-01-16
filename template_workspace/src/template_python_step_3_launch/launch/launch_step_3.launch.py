from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='template_python_step_3_launch',
            executable='talker',
            name='talker',
            output='screen',
        ),
        Node(
            package='template_python_step_3_launch',
            executable='listener',
            name='listener',
            output='screen',
        ),
    ])
