import os
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, PushRosNamespace, Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('baud_rate', default_value='9600', description='Baud rate da comunicação serial'),
        DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0', description='Porta serial'),

        # Inicia o nó serial_node_arduino
        Node(
            package='navegacao_pkg',
            executable='serial_node_arduino',
            name='serial_node_arduino',
            output='screen',
            parameters=[{'baud_rate': LaunchConfiguration('baud_rate'),
                         'serial_port': LaunchConfiguration('serial_port')}],
            emulate_tty=True
        ),
    ])
