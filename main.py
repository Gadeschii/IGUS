from runners.robot_runner import run_robot

if __name__ == "__main__":
    # Crear instancias
    scara = run_robot("Scara")
    rebelline = run_robot("RebelLine")

    # 🔌 Conectar primero Rebelline y cargar variables
    rebelline.load_variables()

    # 🚦 Lanzar SCARA
    scara.set_start_signal()
    scara.run()

    # 🕒 Ahora esperar condiciones de SCARA desde Rebelline
    rebelline.wait_for_external_variable(
        scara,
        [
            ('isfinishscara', 1),
            ('posdropobjscara', 1)
        ]
    )

    # 🚦 Lanzar Rebelline
    rebelline.set_start_signal()
    rebelline.run()
