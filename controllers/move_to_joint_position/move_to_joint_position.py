from controller import Robot

robot = Robot()
time_step = 32  # Webots simulation time step

# Mosajelhom 3shan lw e7tijta lehom bas
initial_positions = {
    "panda_joint1": 0.0000,
    "panda_joint2": 0.0000,
    "panda_joint4": -1.7708,
    "panda_joint6": 1.6000
}


# Define target joint positions (radians)
target_positions = {
    "panda_joint1": 0.0000,
    "panda_joint2": 0.5000,
    "panda_joint4": -2.3208,
    "panda_joint6": 2.6000
}

# Define gripper target position
gripper_target_position = 0.0400

# Get motor devices
joint_motors = {joint: robot.getDevice(joint) for joint in target_positions.keys()}
gripper_motors = {
    "panda_finger::right": robot.getDevice("panda_finger::right"),
    "panda_finger::left": robot.getDevice("panda_finger::left")
}

print("\n🔹 Current Joint Positions (radians):")
for joint, motor in joint_motors.items():
    print(f"  {joint}: {motor.getTargetPosition():.4f}")

print(f"  Gripper Position: {gripper_target_position:.4f}")


# Move joints to target positions
for joint, motor in joint_motors.items():
    motor.setPosition(target_positions[joint])

# Move gripper to target position
for motor in gripper_motors.values():
    motor.setPosition(gripper_target_position)

print("\n🔹 Moving Panda arm to target positions...")

# Keep the controller running to let the robot move
while robot.step(time_step) != -1:
    # Print joint positions in real-time
    print("\n🔹 Current Joint Positions (radians):")
    for joint, motor in joint_motors.items():
        print(f"  {joint}: {motor.getTargetPosition():.4f}")

    print(f"  Gripper Position: {gripper_target_position:.4f}")
