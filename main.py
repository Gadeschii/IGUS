from config.robots_config import robots
from config.conditions import robot_start_conditions
from controllers.igus_controller import IgusRobot
from controllers.variable_monitor import VariableMonitor
from time import sleep

def main():
    robot_instances = {}

    print("\n🔧 INICIALIZANDO TODOS LOS ROBOTS...\n")
    for name, config in robots.items():
        try:
            robot = IgusRobot(
                ip=config["ip"],
                port=config["port"],
                program_name=config["program_name"],
                sequence_path=config["sequence_path"],
                robot_id=config["id"],
                var_file=config.get("var_file")
            )
            robot.prepare()
            robot_instances[name] = robot
        except Exception as e:
            print(f"❌ Error inicializando {name.upper()}: {e}")

    # print("\n🕹️  ESPERANDO CONDICIONES PARA INICIAR SECUENCIAS...\n")
    # launched = set()
    # monitor = VariableMonitor(robots)

    # while len(launched) < len(robot_instances):
    #     monitor.update_variables()
    #     current_vars = monitor.get_all()

    #     for name, robot in robot_instances.items():
    #         if name not in launched:
    #             condition_fn = robot_start_conditions.get(name, lambda vars: False)
    #             if condition_fn(current_vars):
    #                 print(f"🚀 Lanzando secuencia para {name.upper()}")
    #                 robot.run_sequence()
    #                 launched.add(name)

    #     sleep(1)

if __name__ == "__main__":
    main()
