
## Pybullet is not installed. It needs Microsoft C++ build tools, which is 4 GB
import pybullet as p
import pybullet_data
from controller import Robot

robot = Robot()
time_step = 32  # Webots simulation time step

# Load PyBullet (no GUI)
p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load the Panda arm in PyBullet (must match Webots' URDF)
pandaId = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

# Define the target position for the end-effector
target_position = [0, 2.75, -0.27]  # (x, y, z)

# Solve IK in PyBullet to get joint angles
joint_angles = p.calculateInverseKinematics(pandaId, 7, target_position)

# Define the joint names in Webots
joint_names = ["panda_joint1", "panda_joint2", "panda_joint3",
               "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"]

# Get motor devices in Webots
joint_motors = {joint: robot.getDevice(joint) for joint in joint_names}

# Apply computed joint angles to Webots
while robot.step(time_step) != -1:
    for motor, angle in zip(joint_motors.values(), joint_angles):
        motor.setPosition(angle)

    print("\n🔹 Moving to Target Position:", target_position)
    for joint, angle in zip(joint_names, joint_angles):
        print(f"  {joint}: {angle:.4f} rad")
