from config.robots_config import robots
import random
from config.conditions import (
    start_scara,
    start_rebelline1,
    start_rebelline2,
    start_rebel1,
    start_rebel2,
    get_modo_rebel
)
from controllers.igus_controller import IgusRobot
from config.conditions import *
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

    print("\n🕹️  ESPERANDO CONDICIONES PARA INICIAR SECUENCIAS...\n")
    print("AlejandroEstuvoAqui3")
    print(robot_instances["Scara"].controller.robot_state.variabels)
    print("AlejandroEstuvoAqui3")
    launched = set()
    monitor = VariableMonitor(robots)
    print("AlejandroEstuvoAqui4")
    print(robot_instances["Scara"].controller.robot_state.variabels)
    print("AlejandroEstuvoAqui4")
    print("HOLA")
    print(getRobotVariables(robot_instances['Scara']))
    print(robot_instances['Scara'].getRobotVariables())
    print("HOLA")
    while len(launched) < len(robot_instances):
        # print(getRobotVariables(robot_instances['Scara']))
        monitor.update_variables()
        current_vars = monitor.get_all()
        # print(getRobotVariables(robot_instances['Scara']))

        for name, robot in robot_instances.items():
            if name not in launched:
                condition_fn = robot_start_conditions.get(name, lambda vars: False)
                if condition_fn(current_vars):
                    print(f"🚀 Lanzando secuencia para {name.upper()}")

                    # Cambiar secuencia dinámicamente para RebelLine justo antes de correr
                    if name == "RebelLine":
                        modo = get_modo_rebel(current_vars, name)
                        if modo == 1:
                            robot.program_name = "RebelLine1.xml"
                            robot.sequence_path = "sequences/RebelLine/RebelLine1.xml"
                        elif modo == 2:
                            robot.program_name = "RebelLine2.xml"
                            robot.sequence_path = "sequences/RebelLine/RebelLine2.xml"
                        print(f"📁 Modo Rebel dinámico: {modo} → {robot.program_name}")

                    robot.run_sequence()
                    launched.add(name)
                    
        varsaS = getRobotVariables(robot_instances['Scara'])
        varsaRL = getRobotVariables(robot_instances['RebelLine'])
        
        print("vamos a ver")
        print((varsaS['isfinishscara'] > 0.0))
        
        print((name == 'RebelLine'))
        print(name)
        
        if (varsaS['isfinishscara'] > 0.0):
            robot_instances["RebelLine"].program_name = "RebelLine.xml"
            robot_instances["RebelLine"].sequence_path = "sequences/RebelLine/"

            robot_instances["RebelLine"].run_sequence()
            varsaS['isfinishscara'] =0
        
        # print((varsaRL['isfinishrebelline'] > 0.0))    
        if (varsaRL['isfinishrebelline'] > 0.0):
            robot_instances["Rebel1"].program_name = "Rebel1.xml"
            robot_instances["Rebel1"].sequence_path = "sequences/Rebel1/"

            robot_instances["Rebel1"].run_sequence()
            varsaRL['isfinishrebelline'] = 0

        # if (varsa['isfinishscara'] > 0.0):
        #     robot_instances["RebelLine"].program_name = "RebelLine2.xml"
        #     robot_instances["RebelLine"].sequence_path = "sequences/RebelLine/"

        #     robot_instances["RebelLine"].run_sequence()


        sleep(1)

if __name__ == "__main__":
    main()




#############################################################################################
#############################################################################################
#############################################################################################

# Inicializar monitor de variables
# variable_monitor = VariableMonitor()
# variable_monitor.start()
# robot_instances = {}

# # Preparar robots
# for name, robot in robot_instances.items():
#     print(f"🔧 Conectando con {name}...")
#     robot.prepare()
#     print(f"✅ {name} listo")

# # Diccionario de condiciones por robot
# robot_start_conditions = {
#     "SCARA": start_scara,
#     "RebelLine": lambda vars: start_rebelline1(vars) or start_rebelline2(vars),
#     "Rebel1": start_rebel1,
#     "Rebel2": start_rebel2,
# }

# robots_en_ciclo = {"SCARA", "RebelLine", "Rebel1", "Rebel2"}
# launched = set()

# print("\n🚀 Iniciando ciclo de control...")

# while True:
#     current_vars = variable_monitor.read_all()
#     modo = get_modo_rebel(current_vars)

#     for name, robot in robot_instances.items():
#         if name in launched:
#             continue

#         # === SCARA ===
#         if name == "SCARA" and start_scara(current_vars):
#             robot.run_sequence()
#             launched.add(name)
#             print("🤖 SCARA iniciado")

#         # === RebelLine con selección dinámica de secuencia ===
#         elif name == "RebelLine" and (start_rebelline1(current_vars) or start_rebelline2(current_vars)):
#             if modo == 1:
#                 robot.program_name = "RebelLine1.xml"
#                 robot.sequence_path = "sequences/RebelLine/RebelLine1.xml"
#             elif modo == 2:
#                 robot.program_name = "RebelLine2.xml"
#                 robot.sequence_path = "sequences/RebelLine/RebelLine2.xml"
#             robot.run_sequence()
#             launched.add(name)
#             print(f"🤖 RebelLine iniciado con modo {modo}")

#         # === Rebel1 ===
#         elif name == "Rebel1" and start_rebel1(current_vars):
#             robot.run_sequence()
#             launched.add(name)
#             print("🤖 Rebel1 iniciado")

#         # === Rebel2 ===
#         elif name == "Rebel2" and start_rebel2(current_vars):
#             robot.run_sequence()
#             launched.add(name)
#             print("🤖 Rebel2 iniciado")

#     # Reinicio de ciclo cuando todos los robots han sido lanzados
#     if launched == robots_en_ciclo:
#         print("\n✅ Ciclo completo. Reiniciando...")
#         time.sleep(2)

#         # Reset de variables de sincronización
#         for var in [
#             "posdropobjscara",
#             "posdropobjrebellinetorebel1",
#             "posdropobjrebellinetorebel2"
#         ]:
#             variable_monitor.set(var, 0)

#         # Generar nuevo modo aleatorio
#         nuevo_modo = random.choice([1, 2])
#         variable_monitor.set("modo_rebel_selector", nuevo_modo)
#         print(f"🔁 Nuevo modo aleatorio seleccionado: {nuevo_modo}")

#         # Limpiar lanzamientos
#         launched.clear()

#     time.sleep(0.5)  # Pequeña espera para evitar sobrecarga del ciclo
