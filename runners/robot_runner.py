from config.robots_config import robots
from controllers.igus_controller import IgusRobot

def run_robot(robot_id):
    if robot_id not in robots:
        raise ValueError(f"Robot '{robot_id}' no está definido.")

    config = robots[robot_id]

    robot = IgusRobot(
        ip=config["ip"],
        port=config["port"],
        program_name=config["program_name"],
        sequence_path=config["sequence_path"]
    )

    robot.run()
