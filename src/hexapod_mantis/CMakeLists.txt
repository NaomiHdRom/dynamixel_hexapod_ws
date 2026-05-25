cmake_minimum_required(VERSION 3.8)
project(hexapod_mantis)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

find_package(cv_bridge REQUIRED)
find_package(pluginlib REQUIRED)

# ros2_control
# find_package(controller_manager REQUIRED)
# find_package(joint_trajectory_controller REQUIRED)
# find_package(forward_command_controller REQUIRED)

install(DIRECTORY
  controllers
  launch
  models
  protos
  rviz
  urdf
  worlds
  scripts
  DESTINATION share/${PROJECT_NAME}
)


ament_package()