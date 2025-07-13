from controller import Robot
import threading
import socket

# Constants
TIME_STEP = 32
OPEN_HAND = 0.02
CLOSE_HAND = 0.012
JOINT_NAMES = [f"panda_joint{i+1}" for i in range(7)]
FINGER_NAME = "panda_finger::right"

# Block positions and clearings
BLOCK_POSITIONS = [[0.37, -2.7, 2.9], [0.52, -2.37, 2.73], [0.74, -1.96, 2.53]]
BLOCK_CLEARINGS = [[-0.1, -2.78, 2.61], [0.22, -2.48, 2.53], [0.33, -2.18, 2.35]]
BLOCK1, BLOCK2, BLOCK3 = 0, 1, 2

# Initialize Webots robot
robot = Robot()

# Retrieve devices
motors = [robot.getDevice(name) for name in JOINT_NAMES]
finger = robot.getDevice(FINGER_NAME)

# Dictionary of commands
def hand_control(command):
    if command == "open":
        finger.setPosition(OPEN_HAND)
    else:
        finger.setPosition(CLOSE_HAND)
    for _ in range(10):
        robot.step(TIME_STEP)

def move_to_block(block):
    motors[1].setPosition(BLOCK_POSITIONS[block][0])
    motors[3].setPosition(BLOCK_POSITIONS[block][1])
    motors[5].setPosition(BLOCK_POSITIONS[block][2])
    for _ in range(20):
        robot.step(TIME_STEP)

def move_to_clearing(block):
    motors[1].setPosition(BLOCK_CLEARINGS[block][0])
    motors[3].setPosition(BLOCK_CLEARINGS[block][1])
    motors[5].setPosition(BLOCK_CLEARINGS[block][2])
    for _ in range(20):
        robot.step(TIME_STEP)

def sequence(origin_block, target_block):
    move_to_block(origin_block)
    hand_control("close")
    move_to_clearing(origin_block)
    move_to_clearing(target_block)
    move_to_block(target_block)
    hand_control("open")
    move_to_clearing(target_block)

commands = {
    'hand_control': hand_control,
    'move_to_block': move_to_block,
    'move_to_clearing': move_to_clearing,
    'sequence': sequence,
}

# Socket server to receive commands
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

# Start the socket server in a separate daemon thread
threading.Thread(target=socket_server, daemon=True).start()

# Main simulation loop
while robot.step(TIME_STEP) != -1:
    # Your simulation continues to run normally.
    pass
