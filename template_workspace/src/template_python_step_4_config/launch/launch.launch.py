from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Get the path to the config file
    config_dir = get_package_share_directory('template_python_step_4_config')
    config_file = os.path.join(config_dir, 'config', 'config4.yaml')

    return LaunchDescription([
        Node(
            package='template_python_step_4_config',
            executable='talker4',
            name='talker4',
            output='screen',
            parameters=[config_file],
        ),
        Node(
            package='template_python_step_4_config',
            executable='listener4',
            name='listener4',
            output='screen',
            parameters=[config_file],
        ),
    ])
