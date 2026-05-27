from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, EnvironmentVariable
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch


def generate_launch_description():

    # =========================
    # Paths
    # =========================
    hexapod_pkg = FindPackageShare("hexapod_mantis")
    moveit_pkg = FindPackageShare("moveit_config")

    world_path = PathJoinSubstitution([
        hexapod_pkg,
        "worlds",
        "hexapod.wbt"
    ])

    controllers_path = PathJoinSubstitution([
        hexapod_pkg,
        "controllers"
    ])

    # =========================
    # Webots
    # =========================
    webots = ExecuteProcess(
        cmd=[
            "webots",
            "--mode=realtime",
            world_path
        ],
        output="screen",
        additional_env={
            "WEBOTS_CONTROLLER_PATH": controllers_path,
            "DISPLAY": EnvironmentVariable("DISPLAY")
        }
    )

    # =========================
    # MoveIt
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
    # LaunchDescription
    # =========================
    return LaunchDescription([
        webots,
        moveit_launch
    ])