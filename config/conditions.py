
def start_scara(variables):
    return True  # Scara siempre arranca

def start_rebelline(variables):
    return variables.get('isfinishscara', 0) == 1

def start_rebel1(variables):
    return variables.get('posdropobjrebellinetorebel1', 0) == 1

def start_rebel2(variables):
    return variables.get('posdropobjrebellinetorebel2', 0) == 1

robot_start_conditions = {
    "Scara": start_scara,
    "RebelLine": start_rebelline,
    "Rebel1": start_rebel1,
    "Rebel2": start_rebel2,
}
