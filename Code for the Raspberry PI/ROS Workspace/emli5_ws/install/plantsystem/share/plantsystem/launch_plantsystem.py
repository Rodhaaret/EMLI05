from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
import os
from ament_index_python import get_package_share_directory



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

    foxglove=IncludeLaunchDescription(
        XMLLaunchDescriptionSource(
            os.path.join('/opt/ros/humble/share/foxglove_bridge/foxglove_bridge_launch.xml'))
    )

    ld.add_action(FarmerNode)
    ld.add_action(PiNode)
    ld.add_action(WateringsystemNode)
    ld.add_action(foxglove)
   
    return ld

def main():
    generate_launch_description()

if __name__ == '__main__':
    main()
