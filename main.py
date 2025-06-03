from runners.robot_runner import run_robot
from controllers.igus_controller import IgusRobot


if __name__ == "__main__":
    scara = run_robot("Scara")

    rebel = run_robot("RebelLine")
    
    rebel1 = run_robot("Rebel1")
    
    rebel2 = run_robot("Rebel2")
   
