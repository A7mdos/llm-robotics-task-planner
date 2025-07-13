from controller import Robot, Keyboard

robot = Robot()
keyboard = Keyboard()
keyboard.enable(50)  # Enable keyboard input (refresh rate: 50ms)

time_step = 32  # Webots simulation time step

# Define joints to control and their key bindings
joint_bindings = {
    "panda_joint1": {"increase": ord('D'), "decrease": ord('A'), "min": -2.8973, "max": 2.8973},
    "panda_joint2": {"increase": ord('S'), "decrease": ord('W'), "min": -1.7628, "max": 1.7628},
    "panda_joint4": {"increase": ord('E'), "decrease": ord('Q'), "min": -3.0718, "max": -0.0698},
    "panda_joint6": {"increase": ord('C'), "decrease": ord('Z'), "min": -0.0175, "max": 3.7525}
}

# Gripper key bindings
gripper_bindings = {
    "panda_finger::right": {"open": ord('O'), "close": ord('P')},
    "panda_finger::left": {"open": ord('O'), "close": ord('P')}
}

# Get motor devices for arm joints
joint_motors = {joint: robot.getDevice(joint) for joint in joint_bindings.keys()}

# Get motor devices for gripper
gripper_motors = {joint: robot.getDevice(joint) for joint in gripper_bindings.keys()}

# Enable position sensors for joints
joint_sensors = {joint: robot.getDevice(joint + "_sensor") for joint in joint_bindings.keys()}
for sensor in joint_sensors.values():
    if sensor:  # Ensure sensor exists
        sensor.enable(time_step)

# Wait for Webots to update sensor values
robot.step(time_step)

# Initialize joint positions safely (fallback to 0 if sensor fails)
joint_positions = {
    joint: (joint_sensors[joint].getValue() if joint_sensors[joint] else 0.0)
    for joint in joint_sensors.keys()
}

# Initialize gripper position
gripper_position = 0.02  # Default open position
gripper_min = 0.0  # Minimum gripper closure
gripper_max = 0.04  # Maximum open position

# Define movement step size
step_size = 0.005
gripper_step = 0.005  # Adjust gripper movement speed

print("🔹 Use the following keys to control the Panda arm:")
print("Joint 1: [A] Left, [D] Right")
print("Joint 2: [W] Up, [S] Down")
print("Joint 4: [Q] Left, [E] Right")
print("Joint 6: [Z] Left, [C] Right")
print("Gripper: [O] Open, [P] Close")

while robot.step(time_step) != -1:
    key = keyboard.getKey()

    if key == -1:
        continue  # No key pressed

    # Update joint positions based on key inputs, ensuring they stay within limits
    for joint, config in joint_bindings.items():
        if key == config["increase"]:
            joint_positions[joint] = min(joint_positions[joint] + step_size, config["max"])
        elif key == config["decrease"]:
            joint_positions[joint] = max(joint_positions[joint] - step_size, config["min"])

    # Update gripper position safely
    if key in [ord('O'), ord('P')]:  # Only update when pressing O/P
        for joint, keys in gripper_bindings.items():
            if key == keys["open"]:
                gripper_position = min(gripper_position + gripper_step, gripper_max)
            elif key == keys["close"]:
                gripper_position = max(gripper_position - gripper_step, gripper_min)

    # Apply new joint positions
    for joint, motor in joint_motors.items():
        motor.setPosition(joint_positions[joint])

    # Apply gripper position
    for motor in gripper_motors.values():
        motor.setPosition(gripper_position)

    # 🔹 Print joint positions in a single line
    formatted_positions = ", ".join(f"{joint_positions[joint]:.4f}" for joint in joint_bindings.keys())
    print(formatted_positions)
