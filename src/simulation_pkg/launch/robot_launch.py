from launch import LaunchDescription
from launch_ros.actions import Node

# TODO: fazer o arquivo launch do robo

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'caramelo', '-file', 'src/simulation_pkg/urdf/caramelo.urdf'],
            output='screen'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': True}],
            arguments=['src/simulation_pkg/urdf/caramelo.urdf']
        ),
    ])