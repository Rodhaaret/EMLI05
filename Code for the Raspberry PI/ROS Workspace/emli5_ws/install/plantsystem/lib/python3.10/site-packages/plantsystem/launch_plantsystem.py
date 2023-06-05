from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    FarmerNode=Node(
        package='plantsystem',
        executable='farmer_node',
        name='Farmer'
    )

    PiNode=Node(
        package='plantsystem',
        executable='pi_node',
        name='Pi_unit'
    )

    WateringsystemNode=Node(
        package='plantsystem',
        executable='wateringsystem_node',
        name='Wateringsystem'
    )

    ld.add_action(FarmerNode)
    ld.add_action(PiNode)
    ld.add_action(WateringsystemNode)
    return ld