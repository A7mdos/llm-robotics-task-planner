# LLM Robotics Task Planner

## Overview
This repository provides a simulation of the Franka Emika Panda robot using Webots. The project is designed to explore task planning in dynamic environments, leveraging insights from our Bachelor's thesis on hybrid Large Language Model (LLM) and affordance-based robotics.

## Authors
- **Obada Siralkhatim** (Email: obadabadee.pro@gmail.com)
- **Ahmed Ibrahim** (Email: a7mdos1999@gmail.com)

## Features
- Simulation environment for the Franka Emika Panda robot
- Task execution through affordance-guided action selection
- High-level control architecture for dynamic task planning
- Natural language-based interaction capabilities

## Relevance to Our Thesis
This repository implements key findings from our research titled *"Implementation of Task Planning for Smart Agents in Dynamic Environments: A Hybrid LLM and Affordance Approach."* Specifically, it demonstrates:
- **Affordance-Guided Action Execution**: The robot determines possible interactions based on object properties.
- **Hybrid LLM-based Planning**: Integration of natural language processing to enhance task execution.
- **Simulation Tools**: Use of Webots for testing and evaluating robotic behaviors in structured and unstructured environments.

## Getting Started
### Prerequisites
- Webots installation ([Webots official site](https://cyberbotics.com/))
- Python 3.x
- Required dependencies (install via `pip install -r requirements.txt`)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/A7mdos/llm-robotics-task-planner.git
   cd llm-robotics-task-planner
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the simulation:
   ```bash
   webots ./worlds/demo.wbt
   ```
4. Run the natural language interface separately so the socket server can listen:
   ```bash
   python nl_interface_groq.py
   ```

## Usage
- Modify controllers to test different behaviors.
- Use the affordance-guided control strategies for dynamic task planning.
- Experiment with LLM-based task execution by integrating NLP modules.

### Example Usage
Start the natural language interface and enter commands:
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

## Future Work
- Expanding task planning with reinforcement learning
- Enhancing real-world applicability with physical robot testing
- Further improvements in NLP-based control and affordance detection

## References
For more details, see our full thesis: *"Implementation of Task Planning for Smart Agents in Dynamic Environments: A Hybrid LLM and Affordance Approach."*

## License
This project is licensed under the MIT License - see the LICENSE file for details.

