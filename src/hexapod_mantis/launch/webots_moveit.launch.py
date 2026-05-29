from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import PathJoinSubstitution, EnvironmentVariable
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch


def generate_launch_description():

    hexapod_pkg = FindPackageShare("hexapod_mantis")

    world_path = PathJoinSubstitution([
        hexapod_pkg,
        "worlds",
        "hexapod.wbt"
    ])

    controllers_file = PathJoinSubstitution([
        hexapod_pkg,
        "config",
        "ros2_controllers.yaml"
    ])

    # =========================
    # WEBOTS
    # =========================
    webots = ExecuteProcess(
        cmd=["webots", "--mode=realtime", world_path],
        output="screen",
        additional_env={
            "DISPLAY": EnvironmentVariable("DISPLAY"),
        }
    )

    # =========================
    # ROS2 CONTROL (CRÍTICO)
    # =========================


    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen"
    )

    # =========================
    # MOVEIT
    # =========================
    moveit_config = (
        MoveItConfigsBuilder(
            "dynamixel_hexapod",
            package_name="moveit_config"
        )
        .to_moveit_configs()
    )



    moveit_launch = generate_demo_launch(moveit_config)

    # =========================
    # FINAL
    # =========================
    return LaunchDescription([
        webots,
     
        joint_state_broadcaster,
        moveit_launch
    ])