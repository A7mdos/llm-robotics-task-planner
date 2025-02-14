from controller import Robot
import threading
import socket

# Constants
TIME_STEP = 32
OPEN_HAND = 0.02
CLOSE_HAND = 0.012

# Joints to control (using a subset for this example)
JOINT_NAMES = ["panda_joint1", "panda_joint2", "panda_joint4", "panda_joint6"]
FINGER_NAME = "panda_finger::right"

# Blue and Red block positions (4 values per block, corresponding to JOINT_NAMES)
BLUE_BLOCKS_POSITIONS = [
    [0.0, 0.5, -2.37, 2.7],         # Blue Block 1
    [-0.72, 0.48, -2.3908, 2.7],      # Blue Block 2
    [-0.4800, 1.3600, -0.7298, 1.9200],  # Blue Block 3
    [-0.1199, 1.2001, -1.0309, 2.0400]   # Blue Block 4
]

RED_BLOCKS_POSITIONS = [
    [0.5601, 0.4001, -2.5309, 2.7000],  # Red Block 1
    [0.2101, 1.1501, -1.1109, 2.0600],   # Red Block 2
    [-0.3499, 0.6001, -2.1609, 2.6400],   # Red Block 3
    [0.5051, 0.9801, -1.4259, 2.2050]     # Red Block 4
]

# Clearing positions for each block (8 total: 4 blue and 4 red)
BLUE_BLOCK_CLEARINGS = [
    [0.1, 0.55, -2.1, 2.65],    # Clearing for Blue Block 1
    [-0.65, 0.50, -2.3, 2.65],  # Clearing for Blue Block 2
    [-0.45, 1.30, -0.65, 1.95],  # Clearing for Blue Block 3
    [-0.10, 1.15, -0.95, 2.05]   # Clearing for Blue Block 4
]

RED_BLOCK_CLEARINGS = [
    [0.6, 0.35, -2.55, 2.68],   # Clearing for Red Block 1
    [0.25, 1.10, -1.15, 2.05],   # Clearing for Red Block 2
    [-0.35, 0.65, -2.20, 2.63],  # Clearing for Red Block 3
    [0.50, 1.00, -1.40, 2.20]    # Clearing for Red Block 4
]

# Define block indices for convenience
BLOCK1, BLOCK2, BLOCK3, BLOCK4 = 0, 1, 2, 3

# Initialize Webots robot
robot = Robot()

# Retrieve motor devices and the finger
motors = {joint: robot.getDevice(joint) for joint in JOINT_NAMES}
finger = robot.getDevice(FINGER_NAME)

# Function to open or close the hand
def hand_control(command):
    if command == "open":
        finger.setPosition(OPEN_HAND)
    else:
        finger.setPosition(CLOSE_HAND)
    for _ in range(10):
        robot.step(TIME_STEP)

# Function to move the arm to a block position.
# New signature: move_to_block(color, block)
def move_to_block(color, block):
    if color == 'blue':
        positions = BLUE_BLOCKS_POSITIONS[block]
    elif color == 'red':
        positions = RED_BLOCKS_POSITIONS[block]
    else:
        raise ValueError("Unknown color")
    for i, joint in enumerate(JOINT_NAMES):
        motors[joint].setPosition(positions[i])
    for _ in range(20):
        robot.step(TIME_STEP)

# Function to move the arm to a clearing position.
# New signature: move_to_clearing(color, block)
def move_to_clearing(color, block):
    if color == 'blue':
        positions = BLUE_BLOCK_CLEARINGS[block]
    elif color == 'red':
        positions = RED_BLOCK_CLEARINGS[block]
    else:
        raise ValueError("Unknown color")
    for i, joint in enumerate(JOINT_NAMES):
        motors[joint].setPosition(positions[i])
    for _ in range(20):
        robot.step(TIME_STEP)

# Command dictionary for dynamic control
commands = {
    'hand_control': hand_control,
    'move_to_block': move_to_block,
    'move_to_clearing': move_to_clearing,
}

# Socket server for receiving commands
def socket_server():
    host = 'localhost'
    port = 12345
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
                    print("Received command:", data, flush=True)
                    parts = data.split()
                    cmd_name = parts[0]
                    args = parts[1:]
                    # Convert numeric arguments
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

# Main simulation loop
while robot.step(TIME_STEP) != -1:
    pass  # The simulation continues to run while commands are processed.
