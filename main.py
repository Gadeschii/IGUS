from runners.robot_runner import run_robot
from controllers.variable_monitor import VariableMonitor
from config.robots_config import robots
from config.conditions import robot_start_conditions
import time

def main():
    monitor = VariableMonitor(robots)
    launched = set()

    while len(launched) < len(robots):
        monitor.update_variables()
        vars_now = monitor.get_all()

        for robot_name in robots:
            if robot_name not in launched:
                condition = robot_start_conditions.get(robot_name, lambda _: False)
                if condition(vars_now):
                    print(f"🚀 Iniciando {robot_name}")
                    run_robot(robot_name)
                    launched.add(robot_name)
        time.sleep(1)

if __name__ == "__main__":
    main()
