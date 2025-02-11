from controller import Robot

# Constants
TIME_STEP = 32
OPEN_HAND = 0.02
CLOSE_HAND = 0.012
JOINT_NAMES = [f"panda_joint{i+1}" for i in range(7)]
FINGER_NAME = "panda_finger::right"

# Block positions (same values as C code)
BLOCK_POSITIONS = [[0.37, -2.7, 2.9], [0.52, -2.37, 2.73], [0.74, -1.96, 2.53]]
BLOCK_CLEARINGS = [[-0.1, -2.78, 2.61], [0.22, -2.48, 2.53], [0.33, -2.18, 2.35]]

BLOCK1, BLOCK2, BLOCK3 = 0, 1, 2

# Initialize Webots robot
robot = Robot()

# Retrieve motor devices
motors = [robot.getDevice(name) for name in JOINT_NAMES]
finger = robot.getDevice(FINGER_NAME)

def hand_control(command):
    """Opens or closes the gripper."""
    finger.setPosition(OPEN_HAND if command == "open" else CLOSE_HAND)
    for _ in range(10):  # Simulate waiting
        robot.step(TIME_STEP)

def move_to_block(block):
    """Move the robot to the block position."""
    motors[1].setPosition(BLOCK_POSITIONS[block][0])
    motors[3].setPosition(BLOCK_POSITIONS[block][1])
    motors[5].setPosition(BLOCK_POSITIONS[block][2])
    for _ in range(20):
        robot.step(TIME_STEP)

def move_to_clearing(block):
    """Move the robot to a clearing position."""
    motors[1].setPosition(BLOCK_CLEARINGS[block][0])
    motors[3].setPosition(BLOCK_CLEARINGS[block][1])
    motors[5].setPosition(BLOCK_CLEARINGS[block][2])
    for _ in range(20):
        robot.step(TIME_STEP)

def sequence(origin_block, target_block):
    """Moves a block from origin to target."""
    move_to_block(origin_block)
    hand_control("close")
    move_to_clearing(origin_block)
    move_to_clearing(target_block)
    move_to_block(target_block)
    hand_control("open")
    move_to_clearing(target_block)

# Open gripper at the start
hand_control("open")

# Execute the sequence multiple times
for _ in range(10):
    sequence(BLOCK1, BLOCK3)
    sequence(BLOCK2, BLOCK1)
    sequence(BLOCK3, BLOCK2)

