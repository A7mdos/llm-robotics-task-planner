# LLM Robotics Task Planner

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Webots](https://img.shields.io/badge/Webots-2023b-green?style=flat-square&logo=webots)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

## Overview

This repository presents a sophisticated simulation environment for the Franka Emika Panda robot within Webots, designed to advance research in dynamic task planning. At its core, this project explores a novel hybrid approach that synergizes Large Language Models (LLMs) with affordance-based robotics. It serves as a tangible implementation of the key findings from the Bachelor's thesis, "Integrating Large Language Models with Reasoning for Smart Robotic Task Planning," demonstrating how intelligent agents can effectively navigate and perform complex tasks in dynamic, simulated environments.

## Features

This project boasts several innovative features that contribute to its robust task planning capabilities:

*   **Realistic Simulation Environment**: A high-fidelity simulation of the Franka Emika Panda robot is provided within Webots, offering a safe and controlled sandbox for developing and testing robotic behaviors without the need for physical hardware.

*   **Affordance-Guided Action Selection**: The robot's decision-making process is enhanced by an affordance-based system. This allows the robot to intelligently perceive and determine potential interactions with objects in its environment based on their properties and its own capabilities, leading to more intuitive and context-aware task execution.

*   **High-Level Control Architecture**: A meticulously designed control architecture facilitates dynamic task planning. This system enables the robot to adapt its actions in real-time to changing environmental conditions and task requirements, ensuring flexibility and responsiveness.

*   **Natural Language-Based Interaction**: A key highlight is the integration of natural language processing (NLP) capabilities. Users can issue high-level commands in plain English, which are then interpreted by an LLM and translated into actionable robotic instructions, bridging the gap between human intent and robot execution.

## Relevance to Our Thesis

This repository directly embodies the theoretical and practical contributions of our research, *"Integrating Large Language Models with Reasoning for Smart Robotic Task Planning."* It concretely demonstrates the following pivotal aspects:

*   **Affordance-Guided Action Execution**: The system showcases how the robot dynamically identifies and executes actions by understanding the affordances of objects. For instance, it can determine that a block is 'grabbable' or a crate is 'receivable,' enabling it to perform appropriate interactions.

*   **Hybrid LLM-based Planning**: The integration of a Large Language Model (specifically, the Groq Llama-3 model) with traditional robotic control paradigms is a central theme. This hybrid approach allows for more flexible and intelligent task sequencing, where the LLM interprets abstract goals and translates them into a series of concrete, executable steps.

*   **Advanced Simulation Tools**: The strategic use of Webots as the simulation platform is critical for testing and validating complex robotic behaviors. It provides a scalable and reproducible environment for evaluating the effectiveness of our hybrid LLM and affordance-based planning strategies in both structured and unstructured scenarios.

## Getting Started

To set up and run the simulation, please follow these instructions carefully.

### Prerequisites

Ensure you have the following software installed on your system:

*   **Webots**: The official Webots simulation software. You can download it from the [Webots official site](https://cyberbotics.com/).
*   **Python 3.x**: A compatible Python interpreter. It is recommended to use Python 3.8 or newer.
*   **Required Python Dependencies**: These can be installed via `pip` using the provided `requirements.txt` file.

### Installation

1.  **Clone the Repository**:
    Begin by cloning the project repository to your local machine using Git:
    ```bash
    git clone https://github.com/A7mdos/llm-robotics-task-planner.git
    cd llm-robotics-task-planner
    ```

2.  **Install Python Dependencies**:
    Navigate into the cloned directory and install all necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Webots Simulation**:
    Open the Webots simulation environment by executing the following command from the project root:
    ```bash
    webots ./worlds/panda.wbt
    ```
    *Note: The `demo.wbt` mentioned in the original README might be a typo or an older version. `panda.wbt` is the main world file found in the `worlds` directory.* 

4.  **Start the Natural Language Interface**:
    In a separate terminal, run the natural language interface. This script establishes a socket server that listens for commands from the LLM:
    ```bash
    python controllers/LLM_socket_server_controller/NL_interface_groq.py
    ```

## Usage

Once the simulation and the natural language interface are running, you can interact with the robot using natural language commands.

*   **Experiment with Controllers**: Feel free to modify the existing controllers (`controllers/LLM_socket_server_controller/LLM_socket_server_controller.py`) to observe how different behaviors and control strategies impact the robot's performance.

*   **Dynamic Task Planning**: Explore the affordance-guided control strategies to understand how the robot plans and executes tasks in dynamic scenarios.

*   **LLM-based Task Execution**: Integrate and experiment with various NLP modules to enhance the LLM's ability to interpret and generate robot commands, pushing the boundaries of natural language-based control.

### Example Interaction

Here's an example of how you can interact with the system through the natural language interface:

```
Enter your natural language command (type 'exit' to quit): move two of the blue boxes to the red crate
Generated terminal commands:
move_to_block blue 0
move_to_neutral
move_to_block blue 1
hand_control close
move_to_neutral
move_to_crate red
hand_control open
move_to_neutral
Enter your natural language command (type 'exit' to quit): exit
```

## Project Structure

The repository is organized logically to facilitate development and understanding:

```
llm-robotics-task-planner/
├── controllers/                     # Main robot control scripts
│   └── LLM_socket_server_controller/
│       ├── LLM_socket_server_controller.py  # Core robot control logic and socket server
│       ├── NL_interface_groq.py             # Natural Language Interface (LLM integration)
│       └── prompt.txt                       # System prompt for the LLM
│   └── webotcam/                      # Webots camera related scripts
│       └── webotcam.py
├── extra controllers/               # Additional controllers for specific functionalities
│   ├── IK/                          # Inverse Kinematics
│   ├── camera/                      # Camera control (e.g., YOLOv8 integration)
│   ├── keyboard/                    # Keyboard control for manual robot movement
│   ├── move_to_joint_position/      # Scripts for precise joint control
│   ├── panda_arm_demo/              # Example demonstrations for Panda arm
│   ├── socket_server_3_joints/      # Socket server for 3-joint control
│   └── socket_server_with_4_joints/ # Socket server for 4-joint control
├── worlds/                          # Webots world files defining simulation environments
│   └── panda.wbt                    # Main simulation world for the Franka Emika Panda
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation (this file)
```

## Future Work

We envision several exciting avenues for future development:

*   **Reinforcement Learning Integration**: Expanding task planning capabilities by incorporating reinforcement learning techniques to enable the robot to learn optimal strategies through trial and error.

*   **Real-World Applicability**: Enhancing the project's real-world relevance through physical robot testing, bridging the gap between simulation and practical deployment.

*   **Advanced NLP and Affordance Detection**: Further refining the NLP-based control and improving affordance detection mechanisms to enable more nuanced and robust human-robot interaction.

## Authors

*   **Ahmed Osman Ibrahim** (Email: a7mdos1999@gmail.com)
*   **Obada Abdalbadee Siralkhatim** (Email: obadabadee.pro@gmail.com)

## References

For a comprehensive understanding of the underlying research, please refer to our full thesis:

*   *"Integrating Large Language Models with Reasoning for Smart Robotic Task Planning."*

## License

This project is licensed under the MIT License. See the `LICENSE` file in the repository for full details.

