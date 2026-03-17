# ROS2 Code Auto-Evaluator

An automated grading and validation tool designed for ROS2 (Robot Operating System) projects. This tool performs static code analysis to check for syntax and structure errors, and executes dynamic simulations using Gazebo and a UR5 robotic arm to verify code functionality in a realistic environment.

## 🚀 Features

### 1. Static Analysis
Before running the code, the system performs a series of checks:
* **Structure Validation:** Ensures essential files like `package.xml` and `CMakeLists.txt` or `setup.py` exist.
* **Syntax Checking:** Uses `flake8` to identify Python syntax errors and style violations.
* **Safety Checks:** Scans for potential infinite loops or blocking code that could crash the simulation.

### 2. Dynamic Simulation
* **Environment:** Launches a Gazebo simulation with a UR5 Robotic Arm and a target Cube.
* **Execution:** Runs the uploaded ROS2 node to control the arm.
* **Verification:** Checks if the arm successfully performs the task (e.g., touching or moving the cube).

### 3. Visual Feedback
* **Automated Screenshots:** Captures the simulation state during execution.
* **Web Report:** Generates a visual report accessible via a web browser, showing the pass/fail status and the simulation screenshot.

---

## 🛠️ Prerequisites

Before running this tool, ensure your system meets the following requirements:
* **OS:** Ubuntu (20.04 or 22.04 recommended)
* **ROS2 Distribution:** Humble, Iron, or Foxy
* **Simulator:** Gazebo Classic or Ignition
* **Python:** Python 3.8+

---

## 📥 Installation

### 1. Clone the Repository
Open your terminal and clone the project files:

```bash
git clone https://github.com/RISABH-UG26/ros_code_checker.git
cd ros_code_checker
```

### 2. Install Python Dependencies
Install the required Flask and utility libraries:

```bash
pip install flask pyscreenshot flake8
```

### 3. Source ROS2 Environment
Make sure your ROS2 environment is sourced (replace `humble` with your specific version if different):

```bash
source /opt/ros/humble/setup.bash
```

---

## 🖥️ Usage

### 1. Start the Server
Run the Flask application:

```bash
python3 app.py
```

### 2. Access the Web Interface
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Upload & Test
The system accepts `.zip` files containing ROS2 packages.
* **Test Failure Case:** Upload `faulty_pkg.zip` to see how the static analyzer catches errors.
* **Test Success Case:** Upload `correct_pkg.zip` to witness the UR5 arm move in Gazebo and generate a success report.

---

## 📂 Project Structure

```
ros_code_checker/
├── app.py              # Main Flask application entry point
├── static/             # CSS, JS, and generated screenshots
├── templates/          # HTML templates for the web interface
├── uploads/            # Temporary storage for uploaded zip files
├── faulty_pkg.zip      # Sample faulty package for testing
├── correct_pkg.zip     # Sample correct package for testing
└── README.md           # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.

---

## 👤 Author

**Risabh Paul**
* GitHub: [RISABH-UG26](https://github.com/RISABH-UG26)
