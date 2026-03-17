import subprocess
import time
import os
import signal
import sys
import pyscreenshot as ImageGrab

class SimulationRunner:
    def __init__(self, workspace_path="~/ros2_ws"):
        self.workspace_path = os.path.expanduser(workspace_path)
        self.processes = []

    def launch_simulation(self):
        """Launches Gazebo with the UR5 arm."""
        print("[Runner] Launching Gazebo + UR5...")
        
        # 1. Source ROS2
        # 2. Source your Workspace
        # 3. Launch the UR5 robot (No RViz for speed)
        cmd = f"source /opt/ros/humble/setup.bash && " \
              f"source {self.workspace_path}/install/setup.bash && " \
              f"ros2 launch ur_simulation_gazebo ur_sim_control.launch.py ur_type:=ur5e launch_rviz:=false headless:=False"
        
        proc = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            shell=True, 
            preexec_fn=os.setsid, 
            executable='/bin/bash'
        )
        self.processes.append(proc)
        
        # Wait 15 seconds for Gazebo to actually open
        print("[Runner] Waiting 15s for Gazebo to initialize...")
        time.sleep(15)

    def spawn_cube(self):
        """Spawns the red cube."""
        print("[Runner] Spawning Target Cube...")
        
        # IMPORTANT: The <?xml tag must be at the very start. NO SPACES before it.
        cube_sdf = """<?xml version='1.0'?>
<sdf version='1.4'>
  <model name="target_cube">
    <pose>0.5 0 0.2 0 0 0</pose>
    <static>false</static>
    <link name="link">
      <visual name="visual">
        <geometry><box><size>0.1 0.1 0.1</size></box></geometry>
        <material><script><uri>file://media/materials/scripts/gazebo.material</uri><name>Gazebo/Red</name></script></material>
      </visual>
      <collision name="collision">
        <geometry><box><size>0.1 0.1 0.1</size></box></geometry>
      </collision>
    </link>
  </model>
</sdf>"""
        
        with open("cube.sdf", "w") as f:
            f.write(cube_sdf)

        spawn_cmd = f"source /opt/ros/humble/setup.bash && " \
                    f"ros2 run gazebo_ros spawn_entity.py -entity target_cube -file cube.sdf"
        
        # We add a timeout so it doesn't hang forever if Gazebo is broken
        try:
            result = subprocess.run(
                spawn_cmd, 
                shell=True, 
                executable='/bin/bash',
                capture_output=True,
                text=True,
                timeout=10 # Stop trying after 10 seconds
            )
            if result.returncode == 0:
                print("[Runner] Cube Spawned Successfully!")
            else:
                print(f"[Runner] FAILED to spawn cube. Error:\n{result.stderr}")
        except subprocess.TimeoutExpired:
            print("[Runner] ERROR: Timed out waiting for Gazebo. Is it running?")

    def cleanup(self):
        """Kills processes aggressively."""
        print("[Runner] Cleaning up...")
        for proc in self.processes:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except:
                pass
        
        # Force kill to prevent 'Zombie' Gazebos
        subprocess.run("pkill -f gazebo", shell=True)
        subprocess.run("pkill -f ros2", shell=True)

    def run_full_test(self, duration=20):
        try:
            self.launch_simulation()
            self.spawn_cube()
            
            print(f"[Runner] Simulation running for {duration} seconds...")
            
            # Wait half the time, then take a screenshot
            time.sleep(duration / 2)
            
            print("[Runner] 📸 Taking Screenshot...")
            im = ImageGrab.grab()
            save_path = os.path.join(os.getcwd(), "static", "simulation_preview.png")
            
            # Ensure static folder exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            im.save(save_path)
            print(f"[Runner] Saved to {save_path}")
            
            # Wait remaining time
            time.sleep(duration / 2)
            
        except KeyboardInterrupt:
            print("\n[Runner] User interrupted!")
        except Exception as e:
            print(f"\n[Runner] Unexpected Error: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    runner = SimulationRunner()
    runner.run_full_test()
