from controller import Robot
import threading
import socket

# Constants
TIME_STEP = 32
OPEN_HAND = 0.02
CLOSE_HAND = 0.012

# Joints to control
JOINT_NAMES = ["panda_joint1", "panda_joint2", "panda_joint4", "panda_joint6"]
FINGER_NAME = "panda_finger::right"

# Block positions and clearings
BLOCK_POSITIONS = [
    [0.0, 0.5, -2.32, 2.6],  # Block 1
    [0.3, 0.7, -2.0, 2.0],   # Block 2
    [0.6, 1.0, -1.5, 1.5]    # Block 3
]
BLOCK_CLEARINGS = [
    [-0.1, 0.3, -2.0, 2.2],  # Clearing 1
    [0.2, 0.5, -1.8, 2.0],   # Clearing 2
    [0.4, 0.8, -1.4, 1.7]    # Clearing 3
]

BLOCK1, BLOCK2, BLOCK3 = 0, 1, 2

# Initialize Webots robot
robot = Robot()

# Retrieve devices
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

# Function to move the arm to a block position
def move_to_block(block):
    positions = BLOCK_POSITIONS[block]
    for i, joint in enumerate(JOINT_NAMES):
        motors[joint].setPosition(positions[i])
    for _ in range(20):
        robot.step(TIME_STEP)

# Function to move the arm to a clearing position
def move_to_clearing(block):
    positions = BLOCK_CLEARINGS[block]
    for i, joint in enumerate(JOINT_NAMES):
        motors[joint].setPosition(positions[i])
    for _ in range(20):
        robot.step(TIME_STEP)

# Function to execute a pick-and-place sequence
def sequence(origin_block, target_block):
    move_to_block(origin_block)
    hand_control("close")
    move_to_clearing(origin_block)
    move_to_clearing(target_block)
    move_to_block(target_block)
    hand_control("open")
    move_to_clearing(target_block)

# Command dictionary
commands = {
    'hand_control': hand_control,
    'move_to_block': move_to_block,
    'move_to_clearing': move_to_clearing,
    'sequence': sequence,
}

# Socket server for receiving commands
def socket_server():
    host = 'localhost'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Socket server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode().strip()
                if data:
                    print("Received command:", data)
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
                            print(f"Error executing command '{cmd_name}': {e}")
                    else:
                        print(f"Unknown command: {cmd_name}")
                conn.close()

# Start the socket server in a separate thread
threading.Thread(target=socket_server, daemon=True).start()

# Main simulation loop
while robot.step(TIME_STEP) != -1:
    pass  # The simulation runs while listening for commands
