from controller import Robot
import threading
import socket

# Constants
TIME_STEP = 32
OPEN_HAND = 0.05   # Increased value so the hand opens more
CLOSE_HAND = 0.012

# Device names
JOINT_NAMES = ["panda_joint1", "panda_joint2", "panda_joint4", "panda_joint6"]
FINGER_NAME = "panda_finger::right"

# Combined block positions dictionary
BLOCK_POSITIONS = {
    'blue': [
        [0.0, 0.5, -2.37, 2.7],         # Blue Block 1
        [-0.72, 0.48, -2.3908, 2.7],      # Blue Block 2
        [-0.4800, 1.3600, -0.7298, 1.9200],  # Blue Block 3
        [-0.1199, 1.2001, -1.0309, 2.0400]   # Blue Block 4
    ],
    'red': [
        [0.5601, 0.4001, -2.5309, 2.7000],  # Red Block 1
        [0.2101, 1.1501, -1.1109, 2.0600],   # Red Block 2
        [-0.3499, 0.6001, -2.1609, 2.6400],   # Red Block 3
        [0.5051, 0.9801, -1.4259, 2.2050]     # Red Block 4
    ]
}

# Neutral (or "home") position: arm up and away from blocks
NEUTRAL_POSITIONS = [0.0001, 0.0001, -1.7709, 1.6000]

# Crate positions
CRATE_POSITIONS = {
    'blue': [1.3951, 0.7501, -1.0709, 1.7100],
    'red':  [-1.4299, 0.7501, -1.0709, 1.7100]
}

def run_steps(steps, robot):
    for _ in range(steps):
        robot.step(TIME_STEP)

# Initialize Webots robot and devices
robot = Robot()
motors = {name: robot.getDevice(name) for name in JOINT_NAMES}
finger = robot.getDevice(FINGER_NAME)

def hand_control(command):
    if command == "open":
        finger.setPosition(OPEN_HAND)
    else:
        finger.setPosition(CLOSE_HAND)
    run_steps(10, robot)

def move_to_block(color, block):
    try:
        positions = BLOCK_POSITIONS[color][block]
    except KeyError:
        raise ValueError("Unknown color")
    except IndexError:
        raise ValueError("Block index out of range")
    for i, joint in enumerate(JOINT_NAMES):
        motors[joint].setPosition(positions[i])
    run_steps(20, robot)

def move_to_neutral():
    for i, joint in enumerate(JOINT_NAMES):
        motors[joint].setPosition(NEUTRAL_POSITIONS[i])
    run_steps(20, robot)

def move_to_crate(color):
    if color not in CRATE_POSITIONS:
        raise ValueError("Unknown crate color")
    positions = CRATE_POSITIONS[color]
    for i, joint in enumerate(JOINT_NAMES):
        motors[joint].setPosition(positions[i])
    run_steps(20, robot)

# Command dictionary for dynamic control
commands = {
    'hand_control': hand_control,
    'move_to_block': move_to_block,
    'move_to_neutral': move_to_neutral,
    'move_to_crate': move_to_crate,
}

def socket_server():
    host = 'localhost'
    port = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Socket server listening on {host}:{port}", flush=True)
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}", flush=True)
                data = conn.recv(1024).decode().strip()
                if data:
                    # Check if the command is an error message from the LLM.
                    parts = data.split()
                    if parts[0].lower() == "error":
                        print(f"LLM reported an error: {' '.join(parts[1:])}", flush=True)
                    else:
                        print(f"Received command: {data}", flush=True)
                        cmd_name = parts[0]
                        args = parts[1:]
                        converted_args = []
                        for arg in args:
                            try:
                                converted_args.append(int(arg))
                            except ValueError:
                                converted_args.append(arg)
                        if cmd_name in commands:
                            try:
                                commands[cmd_name](*converted_args)
                            except Exception as e:
                                print(f"Error executing command '{cmd_name}': {e}", flush=True)
                        else:
                            print(f"Unknown command: {cmd_name}", flush=True)
                conn.close()

# Start the socket server in a separate daemon thread
threading.Thread(target=socket_server, daemon=True).start()

# Ensure simulation starts with hand open
hand_control("open")

# Main simulation loop
while robot.step(TIME_STEP) != -1:
    pass
