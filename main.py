from runners.robot_runner import run_robot
from controllers.igus_controller import IgusRobot


if __name__ == "__main__":
    scara = run_robot("Scara")
    #scara.wait_for_finish_signal()

    rebel = run_robot("RebelLine")
    #rebel.wait_for_finish_signal()
