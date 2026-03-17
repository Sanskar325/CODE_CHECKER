ROS2 Code Auto-Evaluator

I developed an automated grading and validation tool for ROS2 (Robot Operating System) projects that combines static code analysis with dynamic simulation. This system evaluates both the correctness and functionality of submitted ROS2 packages in a realistic robotic environment using Gazebo and a UR5 robotic arm.

🚀 Key Features

1. Static Code Analysis

Before execution, my system performs multiple validation checks:

Structure Validation: Verifies the presence of essential ROS2 files such as package.xml, CMakeLists.txt, or setup.py.

Syntax Checking: Uses flake8 to detect Python syntax errors and enforce coding standards.

Safety Checks: Identifies potentially unsafe code patterns like infinite loops or blocking operations that may disrupt simulations.

2. Dynamic Simulation

Simulation Environment: I integrated Gazebo with a UR5 robotic arm and a target cube.

Execution: The uploaded ROS2 node is executed within the simulation environment.

Functional Verification: The system evaluates task completion, such as whether the robotic arm successfully interacts with or moves the cube.

3. Visual Feedback System

Automated Screenshots: Captures real-time simulation states during execution.

Web-Based Report: Generates a browser-accessible report displaying pass/fail results along with visual evidence from the simulation.

🛠️ Prerequisites

To run this project, I ensured compatibility with the following setup:

Ubuntu (20.04 or 22.04)

ROS2 (Humble, Iron, or Foxy)

Gazebo Classic or Ignition

Python 3.8+

📥 Installation
1. Clone the Repository
git clone https://github.com/RISABH-UG26/ros_code_checker.git
cd ros_code_checker
2. Install Dependencies
pip install flask pyscreenshot flake8
3. Source ROS2 Environment
source /opt/ros/humble/setup.bash
🖥️ Usage
1. Start the Application
python3 app.py
2. Access the Interface

Open in browser:

http://127.0.0.1:5000
3. Upload and Evaluate

Upload .zip files containing ROS2 packages

Test with:

faulty_pkg.zip to observe error detection

correct_pkg.zip to verify successful execution in simulation

📂 Project Structure
ros_code_checker/
├── app.py              # Flask application entry point
├── static/             # CSS, JS, screenshots
├── templates/          # HTML templates
├── uploads/            # Temporary uploaded files
├── faulty_pkg.zip      # Sample faulty package
├── correct_pkg.zip     # Sample correct package
└── README.md           # Documentation

🤝 Contributions
I welcome contributions and improvements. Feel free to fork the repository and submit a pull request.

👤 Author

Sanskar Verma
