import os
import zipfile
import subprocess
import json
import re
import shutil

class ROSCodeChecker:
    def __init__(self, upload_dir="uploads", extract_dir="extracted", report_dir="reports"):
        self.upload_dir = upload_dir
        self.extract_dir = extract_dir
        self.report_dir = report_dir
        self.report = {
            "syntax_errors": [],
            "structure_errors": [],
            "nodes_detected": [],
            "safety_warnings": [],
            "score": 100
        }

    def unzip_package(self, zip_path):
        """Extracts the user's zip file."""
        # Clean previous extraction
        if os.path.exists(self.extract_dir):
            shutil.rmtree(self.extract_dir)
        os.makedirs(self.extract_dir)

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_dir)
            return True
        except zipfile.BadZipFile:
            self.report["structure_errors"].append("Invalid ZIP file.")
            return False

    def check_structure(self):
        """Checks for package.xml and setup.py/CMakeLists.txt."""
        found_package_xml = False
        found_build_file = False

        for root, dirs, files in os.walk(self.extract_dir):
            if "package.xml" in files:
                found_package_xml = True
            if "setup.py" in files or "CMakeLists.txt" in files:
                found_build_file = True

        if not found_package_xml:
            self.report["structure_errors"].append("Missing package.xml")
            self.report["score"] -= 20
        if not found_build_file:
            self.report["structure_errors"].append("Missing setup.py or CMakeLists.txt")
            self.report["score"] -= 20

    def check_syntax(self):
        """Runs flake8 on Python files to check for syntax errors."""
        # Find all python files
        py_files = []
        for root, dirs, files in os.walk(self.extract_dir):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))

        for py_file in py_files:
            # Run flake8 via the current python executable
            import sys # Make sure this is at the top of your file
            
            result = subprocess.run(
                [sys.executable, "-m", "flake8", py_file, "--select=E9,F63,F7", "--format=default"], 
                capture_output=True, text=True
            )
            if result.returncode != 0:
                self.report["syntax_errors"].append(f"Syntax Error in {os.path.basename(py_file)}: {result.stdout.strip()}")
                self.report["score"] -= 50  # Heavy penalty for syntax errors

    def check_safety_and_nodes(self):
        """Scans code text for ROS patterns and infinite loops[cite: 15, 16]."""
        for root, dirs, files in os.walk(self.extract_dir):
            for file in files:
                if file.endswith(".py"): # Focusing on Python for Day 1
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        content = f.read()
                        
                        # Check 1: Node Detection
                        if "create_publisher" in content:
                            self.report["nodes_detected"].append(f"Publisher found in {file}")
                        if "create_subscription" in content:
                            self.report["nodes_detected"].append(f"Subscriber found in {file}")
                        
                        # Check 2: Safety (Infinite Loop check)
                        # Regex explanation: Looks for 'while True' or 'while(1)'
                        if re.search(r'while\s*(True|1)\s*:', content):
                            # If found, check if 'sleep' is also in the file
                            if "sleep" not in content and "Rate" not in content:
                                self.report["safety_warnings"].append(
                                    f"DANGEROUS: Infinite loop detected without sleep in {file}!"
                                )
                                self.report["score"] -= 30

    def run_check(self, zip_filename):
        zip_path = os.path.join(self.upload_dir, zip_filename)
        if self.unzip_package(zip_path):
            self.check_structure()
            self.check_syntax()
            self.check_safety_and_nodes()
        
        # Save Report
        report_path = os.path.join(self.report_dir, "report.json")
        with open(report_path, "w") as f:
            json.dump(self.report, f, indent=4)
        
        return self.report

# --- Main Execution Block for Testing ---
if __name__ == "__main__":
    # Create dummy directories if they don't exist
    os.makedirs("uploads", exist_ok=True)
    
    # NOTE: You need to put a zip file in 'uploads/' to test this!
    # Example: python3 checker.py
    
    specific_file = "test_pkg.zip" 
    checker = ROSCodeChecker()
    print(checker.run_check(specific_file))
    print("Checker script ready. Import this into your Flask app later.")
    
