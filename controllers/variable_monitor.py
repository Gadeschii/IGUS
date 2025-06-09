from cri_lib import CRIController

class VariableMonitor:
    def __init__(self, robot_configs):
        self.robot_configs = robot_configs
        self.variables = {}

    def update_variables(self):
        self.variables = {}  # 🔁 Reiniciar variables cada ciclo
        for name, config in self.robot_configs.items():
            controller = CRIController()
            if controller.connect(config["ip"], config["port"]):
                try:
                    controller.wait_for_status_update(timeout=1)  # 🔄 Forzar actualización
                    vars_dict = controller.robot_state.variabels
                    for k, v in vars_dict.items():
                        self.variables[k.lower()] = v  # 🧹 Homogéneo en minúsculas
                except Exception as e:
                    print(f"⚠️ Error leyendo variables de {name}: {e}")
                controller.close()

    def get_all(self):
        return self.variables
