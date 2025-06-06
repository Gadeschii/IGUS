# controllers/variable_monitor.py

from cri_lib import CRIController

class VariableMonitor:
    def __init__(self, robot_configs):
        self.robot_configs = robot_configs
        self.variables = {}

    def update_variables(self):
        for name, config in self.robot_configs.items():
            controller = CRIController()
            if controller.connect(config["ip"], config["port"]):
                try:
                    vars_dict = controller.robot_state.variabels
                    for k, v in vars_dict.items():
                        self.variables[k.lower()] = v  # homogéneo en minúscula
                except:
                    pass
                controller.close()

    def get_all(self):
        return self.variables
