# mantis.py
# Python controller for the Mantis hexapod in Webots
# Equivalent to the original C controller

from controller import Robot
import math

def main():
    robot = Robot()

    time_step = int(robot.getBasicTimeStep())

    # Meaning of the motor characters:
    # R / L : Right / Left
    # A / M / P : Front / Middle / Rear
    # C / F / T : Base / Shoulder / Knee
    motor_names = [
        "RPC", "RPF", "RPT",
        "RMC", "RMF", "RMT",
        "RAC", "RAF", "RAT",
        "LPC", "LPF", "LPT",
        "LMC", "LMF", "LMT",
        "LAC", "LAF", "LAT"
    ]

    # Get motors
    motors = []
    for name in motor_names:
        motor = robot.getDevice(name)
        motor.setPosition(0.0)   # Position control mode
        motors.append(motor)

    # Gait parameters (same as C controller)

    # frequency [Hz]
    f = 0.5

    # amplitudes [rad]
    aC = 0.25   # Base
    aF = 0.20   # Shoulder
    aT = 0.05   # Knee
    a = [
         aC,  aF, -aT,
        -aC, -aF,  aT,
         aC,  aF, -aT,
         aC, -aF,  aT,
        -aC,  aF, -aT,
         aC, -aF,  aT
    ]

    # phases [s]
    pC = 0.0
    pF = 2.0
    pT = 2.5
    p = [
        pC, pF, pT,
        pC, pF, pT,
        pC, pF, pT,
        pC, pF, pT,
        pC, pF, pT,
        pC, pF, pT
    ]

    # offsets [rad]
    dC = 0.6
    dF = 0.8
    dT = -2.4
    d = [
        -dC,  dF,  dT,
         0.0, dF,  dT,
         dC,  dF,  dT,
         dC,  dF,  dT,
         0.0, dF,  dT,
        -dC,  dF,  dT
    ]

    print("✅ Mantis Python controller running")

    while robot.step(time_step) != -1:
        t = robot.getTime()

        for i in range(18):
            position = a[i] * math.sin(2.0 * math.pi * f * t + p[i]) + d[i]
            motors[i].setPosition(position)

if __name__ == "__main__":
    main()