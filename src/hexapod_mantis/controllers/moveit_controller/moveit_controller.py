#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from controller import Robot

class MoveItBridge(Node):
    def __init__(self, robot):
        super().__init__('moveit_webots_bridge')
        self.robot = robot

        self.motors = {}
        joint_names = [
            'joint_1A','joint_1B','joint_1C',
            'joint_2A','joint_2B','joint_2C',
            'joint_3A','joint_3B','joint_3C',
            'joint_4A','joint_4B','joint_4C',
            'joint_5A','joint_5B','joint_5C',
            'joint_6A','joint_6B','joint_6C',
        ]

        for name in joint_names:
            motor = robot.getDevice(name)
            motor.setPosition(0.0)
            self.motors[name] = motor

        self.create_subscription(
            JointTrajectory,
            '/LEG1_controller/joint_trajectory',  # 👈 OJO aquí
            self.trajectory_cb,
            10
        )

    def trajectory_cb(self, msg):
        if not msg.points:
            return

        point = msg.points[-1]
        for name, pos in zip(msg.joint_names, point.positions):
            if name in self.motors:
                self.motors[name].setPosition(pos)

def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    rclpy.init()
    node = MoveItBridge(robot)

    while robot.step(timestep) != -1:
        rclpy.spin_once(node, timeout_sec=0.0)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()