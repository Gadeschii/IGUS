from runners.robot_runner import run_robot
from controllers.igus_controller import IgusRobot

if __name__ == "__main__":
    # 1. Conectar y preparar TODOS los robots
    
    scara = run_robot("Scara")
    rebelline = run_robot("RebelLine")

    # 2. Esperar que alguna condición se cumpla para que Scara empiece
    scara.wait_for_any_external_variable
    ([
        ("startrebelline", 1),
        ("isfinishrebelline", 1),
        ("posdropobjrebelline", 1)
    ])
    scara.set_start_signal()

    # 4. Esperar que Scara deje objeto para que Rebelline empiece
    rebelline.wait_for_external_variable([
        ("isfinishscara", 1),
        ("posdropobjscara", 1)
    ])
    rebelline.set_start_signal()
    rebelline.wait_for_variable("isfinishrebelline")
