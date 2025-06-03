from controllers.igus_controller import IgusRobot
from config import robots_config

def run_robot(robot_name: str) -> IgusRobot:
    if robot_name not in robots_config.robots:
        raise ValueError(f"Robot '{robot_name}' no está definido en config.py")

    cfg = robots_config.robots[robot_name]

    robot = IgusRobot(
        ip=cfg["ip"],
        port=cfg["port"],
        program_name=cfg["program_name"],
        sequence_path=cfg["sequence_path"],
        wait_timeout=cfg.get("wait_timeout", 30),
        robot_id=cfg.get("id", robot_name.lower()),
        var_file=cfg.get("var_file") 
    )

    robot.run()
    return robot
