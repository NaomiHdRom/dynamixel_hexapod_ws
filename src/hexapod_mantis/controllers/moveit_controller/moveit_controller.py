#!/usr/bin/env python3

from controller import Robot
import rclpy
from rclpy.node import Node

from moveit_msgs.msg import DisplayTrajectory


class MoveItBridge(Node):
    def __init__(self, robot):
        super().__init__('moveit_webots_bridge')

        self.robot = robot
        self.timestep = int(robot.getBasicTimeStep())

        # -----------------------------
        # Webots motors
        # -----------------------------
        self.motors = {}

        joint_names = [
            'joint_1A', 'joint_1B', 'joint_1C',
            'joint_2A', 'joint_2B', 'joint_2C',
            'joint_3A', 'joint_3B', 'joint_3C',
            'joint_4A', 'joint_4B', 'joint_4C',
            'joint_5A', 'joint_5B', 'joint_5C',
            'joint_6A', 'joint_6B', 'joint_6C',
        ]

        for name in joint_names:
            motor = robot.getDevice(name)
            if motor is None:
                self.get_logger().error(f'Motor {name} not found in Webots')
            else:
                motor.setPosition(0.0)
                self.motors[name] = motor

        # -----------------------------
        # MoveIt subscription
        # -----------------------------
        self.subscription = self.create_subscription(
            DisplayTrajectory,
            '/display_planned_path',
            self.trajectory_callback,
            10
        )

        self.get_logger().info('MoveIt → Webots bridge READY')


    def trajectory_callback(self, msg: DisplayTrajectory):
        if not msg.trajectory:
            return

        traj = msg.trajectory[0].joint_trajectory

        joint_names = traj.joint_names

        self.get_logger().info(
            f'Received trajectory with {len(traj.points)} points'
        )

        # Ejecutar punto por punto
        for point in traj.points:
            for name, position in zip(joint_names, point.positions):
                if name in self.motors:
                    self.motors[name].setPosition(position)

            # Avanzar simulación el tiempo necesario
            steps = int(
                (point.time_from_start.sec +
                 point.time_from_start.nanosec * 1e-9) /
                (self.timestep * 1e-3)
            )

            for _ in range(max(steps, 1)):
                if self.robot.step(self.timestep) == -1:
                    return


def main():
    # -----------------------------
    # Webots init
    # -----------------------------
    robot = Robot()

    # -----------------------------
    # ROS 2 init
    # -----------------------------
    rclpy.init()
    node = MoveItBridge(robot)

    # -----------------------------
    # Main loop
    # -----------------------------
    while robot.step(node.timestep) != -1:
        rclpy.spin_once(node, timeout_sec=0.0)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()