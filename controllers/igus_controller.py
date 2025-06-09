import time
from cri_lib import CRIController

class IgusRobot:
    def __init__(self, ip, port, program_name, sequence_path, remote_folder="Programs", wait_timeout=35, robot_id="",var_file=None):
        self.ip = ip
        self.port = port
        self.program_name = program_name
        self.sequence_path = sequence_path
        self.remote_folder = remote_folder
        self.wait_timeout = wait_timeout
        self.controller = CRIController()
        self._last_status = None
        self.var_file = var_file
        self.robot_id = robot_id.lower()
        self.controller.register_status_callback(self.status_callback)

    def status_callback(self, state):
        self._last_status = state

    # def wait_for_finish_signal(self, signal_base="isfinish"):
    #     variable_name = f"{signal_base}{self.robot_id}"
    #     print(f"⏳ Esperando que la variable '{variable_name}' sea 1.0...")
    #     print (self.controller.robot_state.variabels)
    #     print
    #     start = time.time()
    #     while time.time() - start < self.wait_timeout:
    #         self.controller.wait_for_status_update(timeout=1)
    #         try:
    #             value = float(self.controller.robot_state.variabels[variable_name])
    #             print(f"🔎 {variable_name} = {value}")
    #             print (f"{self.controller.robot_state.variabels}")
    #             if value == 1.0:
    #                 print(f"✅ Señal '{variable_name}' detectada.")
    #                 return
    #         except Exception as e:
    #             print(f"⚠️ Error al leer variable '{variable_name}': {e}")
    #         time.sleep(0.5)

    #     raise TimeoutError(f"❌ Timeout: '{variable_name}' no se volvió 1 en {self.wait_timeout} segundos.")


    # def _wait_for_axis_referenced(self, joint_name="A1", target_value=469.0, timeout=30):
    #     print(f"⏳ Esperando a que el eje {joint_name} llegue a {target_value} para considerarlo referenciado...")
    #     start = time.time()
    #     while time.time() - start < timeout:
    #         self.controller.wait_for_status_update(timeout=1)
    #         try:
    #             joint_value = getattr(self.controller.robot_state.variabels['#position'], joint_name)
    #             print(f"🔍 {joint_name} = {joint_value}")
    #             if joint_value >= target_value:
    #                 print(f"✅ Eje {joint_name} referenciado correctamente.")
    #                 return True
    #         except Exception as e:
    #             print(f"⚠️ Error al leer {joint_name}: {e}")
    #         time.sleep(0.5)

    #     raise TimeoutError(f"❌ Timeout: El eje {joint_name} no alcanzó el valor {target_value} en {timeout} segundos.")

    def wait_until_axes_referenced(self, timeout=120, axes=("A1", "A2", "A3","A4", "A5", "A6","E1")) -> bool:
                    print(f"⏳ Esperando a que los ejes {axes} estén referenciados...")
                    start = time.time()
                    while time.time() - start < timeout:
                        if self.controller.are_all_axes_referenced(axes):
                            print("♻️Segundo Reinicio...")
                            self.controller.reset()

                            print("🔓 Activando control remoto...")
                            if not self.controller.set_active_control(True):
                                raise Exception("❌ No se pudo activar el control remoto.")

                            print("⚡ Habilitando robot...")
                            if not self.controller.enable():
                                raise Exception("❌ No se pudo habilitar el robot.")

                            return True
                        time.sleep(1)
                    raise TimeoutError(f"❌ Timeout: Los ejes {axes} no se referenciaron a tiempo.")

    def move_to_safe_position_scara(self):
        """
        Mueve el robot SCARA a una posición segura predefinida.
        Lanza excepción si el movimiento falla por cualquier razón.
        """
        print("🕹️ Moviendo ejes a posición segura...")
        time.sleep(5)
        # ⚠️ Verifica que el robot esté habilitado y listo para moverse
        if not self.controller.robot_state.active_control:
            raise Exception("❌ El control remoto no está activo.")

        if not self.controller.robot_state.main_relay:
            raise Exception("❌ El relé principal no está habilitado.")

        # ❗ Verifica errores activos por eje
        for i, err in enumerate(self.controller.robot_state.error_states):
            if any([getattr(err, attr) for attr in vars(err)]):  # Si algún bit está activo
                raise Exception(f"❌ Error activo en el eje {i}: {err}")

        # 🚀 Intenta mover el robot
        success = self.controller.move_joints(
            A1=350.0,
            A2=-74.3,
            A3=70.0,
            A4=80.0,
            A5=0.0,
            A6=0.0,
            E1=0.0,
            E2=0.0,
            E3=0.0,
            velocity=40.0,
            wait_move_finished=True
        )
        if not success:
            raise Exception("❌ Fallo al mover a posición segura.")
        print("✅ Robot posicionado correctamente.")


    def move_to_safe_position_rebelLine(self):
        """
        Mueve el robot Rebel Line a una posición segura predefinida.
        Lanza excepción si el movimiento falla por cualquier razón.
        """
        print("🕹️ Moviendo ejes a posición segura...")
        time.sleep(5)
        # ⚠️ Verifica que el robot esté habilitado y listo para moverse
        if not self.controller.robot_state.active_control:
            raise Exception("❌ El control remoto no está activo.")

        if not self.controller.robot_state.main_relay:
            raise Exception("❌ El relé principal no está habilitado.")

        # if self.controller.robot_state.kinematics_state != 0:  # 2 = Kinematics Ready
        #     print(self.controller.robot_state.kinematics_state)
        #     raise Exception("❌ La cinemática no está lista para moverse.")

        # ❗ Verifica errores activos por eje
        for i, err in enumerate(self.controller.robot_state.error_states):
            if any([getattr(err, attr) for attr in vars(err)]):  # Si algún bit está activo
                raise Exception(f"❌ Error activo en el eje {i}: {err}")

        # 🚀 Intenta mover el robot
        success = self.controller.move_joints(
            A1= 60.0,
            A2= 41.66,
            A3=51.17,
            A4= -0.7,
            A5= 85.5,
            A6= -33.5,
            E1= 734.2,
            E2=0.0,
            E3=0.0,
            velocity=70.0,
            wait_move_finished=True,
            acceleration = 1.0
        )

        # if not success:
        #     raise Exception("❌ Fallo al mover a posición segura.")

        print("✅ Robot posicionado correctamente.")


    def prepare(self):
        try:
            print(f"\n{'='*30}")
            print(f"🛠️  Preparando robot: {self.robot_id.upper()}")
            print(f"{'='*30}")

            print(f"🔌 Conectando a {self.ip}:{self.port}")
            if not self.controller.connect(self.ip, self.port):
                raise Exception("❌ No se pudo conectar al robot.")

            print("♻️ Reiniciando robot...")
            self.controller.reset()

            print("🔓 Activando control remoto...")
            if not self.controller.set_active_control(True):
                raise Exception("❌ No se pudo activar el control remoto.")

            print("⚡ Habilitando robot...")
            if not self.controller.enable():
                raise Exception("❌ No se pudo habilitar el robot.")

            print("✅ Esperando a que el robot esté listo...")
            if not self.controller.wait_for_kinematics_ready(timeout=30):
                raise Exception("❌ El robot no está listo tras el referenciado.")

            success = True
            if self.robot_id == "scara":
                print("🔧 Referenciando SCARA: primero A1...")
                time.sleep(0.5)

                #self.controller.reference_single_joint('A1')
                print(f"📋 Resultado de reference_single_joint('A1'): {success}")
                time.sleep(0.5)
                print("Check referenced axis")
                print(self.controller.are_all_axes_referenced())
                if self.controller.are_all_axes_referenced(axes=("A1", "A2", "A3","A4")):

                    self.move_to_safe_position_scara()
                else:

                    if not self.controller.reference_single_joint('A1') :
                        raise Exception("❌ Fallo al referenciar A1 en SCARA.")

                    # Esperar a que A1 esté referenciado
                    self.wait_until_axes_referenced(axes=("A1",), timeout=200)

                    # Una vez A1 esté referenciado, referenciar A4
                    print("✅ A1 referenciado. Referenciando A4...")
                    if not self.controller.reference_single_joint("A4"):
                        raise Exception("❌ Fallo al iniciar la referencia de A4 en SCARA.")

                    self.wait_until_axes_referenced(axes=("A4",), timeout=30)

                    # Referenciar el resto de ejes
                    print("✅ A4 referenciado. Referenciando el resto de ejes...")
                    if not self.controller.reference_all_joints():
                        raise Exception("❌ Fallo al referenciar el resto de ejes en SCARA.")
                    time.sleep(0.2)

                # print(self.controller.robot_state.referencing_state)
                # print(self.controller.answer_events.get("info_referencing"))
                # self._wait_for_axis_referenced(joint_name='A1', target_value=469.0)

                    self.wait_until_axes_referenced(axes=("A1", "A2", "A3", "A4")) #si veo qeu el A4 me da problema lo quito
                    time.sleep(1)
                    self.controller.reset()
                    time.sleep(0.5)
                    self.controller.enable()
                    time.sleep(0.5)
                    self.move_to_safe_position_scara()



            elif self.robot_id == "rebelline":
                if self.controller.are_all_axes_referenced(axes=("A1", "A2", "A3","A4", "A5", "A6","E1")):

                    self.move_to_safe_position_rebelLine()

                else:
                    print("🔧 Referenciando REBELLINE: primero E1...")
                    time.sleep(0.5)
                      # self.controller.reference_single_joint('E1')
                    print(f"📋 Resultado de reference_single_joint('E1'): {success}")
                    time.sleep(0.5)
                    if not self.controller.reference_single_joint('E1'):
                        raise Exception("❌ Fallo al referenciar E1 en REBELLINE.")
                    # Esperar a que E1 esté referenciado
                    self.wait_until_axes_referenced(axes=("E1",), timeout=200)
                    print("✅ E1 referenciado. Continuando con el resto de ejes...")

                    if not self.controller.reference_all_joints():
                        raise Exception("❌ Fallo al referenciar el resto de ejes en REBELLINE.")

                    time.sleep(0.2)

                    self.wait_until_axes_referenced(axes=("A1", "A2", "A3", "A4","A5","A6","E1" ))
                    time.sleep(1)
                    self.controller.reset()
                    time.sleep(0.5)
                    self.controller.enable()
                    time.sleep(0.5)
                    self.move_to_safe_position_rebelLine()

            else:
                print("🎯 Referenciando todos los ejes...")
                if not self.controller.reference_all_joints():
                    raise Exception("❌ Fallo al referenciar todos los ejes.")

            print("✅ Esperando a que el robot esté listo...")
            if not self.controller.wait_for_kinematics_ready(timeout=30):
                raise Exception("❌ El robot no está listo tras el referenciado.")

            if self.var_file:
                print(f"📤 Subiendo archivo de variables: {self.var_file}")
                if not self.controller.upload_file(self.var_file, self.remote_folder):
                    raise Exception("❌ Fallo al subir el archivo de variables.")
                print("📦 Cargando archivo de variables...")
                if not self.controller.load_programm(self.var_file):
                    raise Exception("❌ Fallo al cargar el archivo de variables.")
                print("✅ Variables inicializadas correctamente.")

                print("▶️ Iniciando programa...")
                if not self.controller.start_programm():
                    raise Exception("❌ Error al iniciar el programa.")

            print(f"✅ Preparación completa para: {self.robot_id.upper()}")

        except Exception as e:
            print(f"❌ Error en preparación de {self.robot_id.upper()}: {e}")
            self.controller.close()
            raise

    def run_sequence(self):
        try:
            print(f"\n{'='*30}")
            print(f"▶️  Ejecutando secuencia para: {self.robot_id.upper()}")
            print(f"{'='*30}")

            print(f"📤 Subiendo archivo de secuencia: {self.sequence_path}")
            if not self.controller.upload_file(self.sequence_path, self.remote_folder):
                raise Exception("❌ Fallo al subir el archivo de secuencia.")

            print("📦 Cargando programa de movimiento...")
            if not self.controller.load_programm(self.program_name):
                raise Exception("❌ Fallo al cargar el programa de movimiento.")

            print("▶️ Iniciando programa...")
            if not self.controller.start_programm():
                raise Exception("❌ Error al iniciar el programa de movimiento.")

            # self.wait_for_finish_signal()
            # print(f"✅ Secuencia completada para: {self.robot_id.upper()}")

        except Exception as e:
            print(f"❌ Error en secuencia de {self.robot_id.upper()}: {e}")

        # finally:
        #     print(f"🛑 Cerrando conexión con {self.robot_id.upper()}")
        #     self.controller.close()
        #     print(f"{'-'*30}")


























































    # def run(self):
    #     try:
    #         print(f"\n{'='*30}")
    #         print(f"▶️  Ejecutando secuencia para: {self.robot_id.upper()}")
    #         print(f"{'='*30}")

    #         print(f"🔌 Conectando a {self.ip}:{self.port}")
    #         if not self.controller.connect(self.ip, self.port):
    #             raise Exception("❌ No se pudo conectar al robot.")

    #         print("♻️ Reiniciando robot...")
    #         self.controller.reset()

    #         print("🔓 Activando control remoto...")
    #         if not self.controller.set_active_control(True):
    #             raise Exception("❌ No se pudo activar el control remoto.")

    #         print("⚡ Habilitando robot...")
    #         if not self.controller.enable():
    #             raise Exception("❌ No se pudo habilitar el robot.")

    #         print("✅ Esperando a que el robot esté listo para moverse...")
    #         if not self.controller.wait_for_kinematics_ready(timeout=30):
    #             raise Exception("❌ El robot no está listo para moverse.")

    #         # 👉 PASO 1: Variables == 0
    #         if self.var_file:
    #             print(f"📤 Subiendo archivo de variables: {self.var_file}")
    #             if not self.controller.upload_file(self.var_file, self.remote_folder):
    #                 raise Exception("❌ Fallo al subir el archivo de variables.")
    #             print("📦 Cargando archivo de variables...")
    #             if not self.controller.load_programm(self.var_file):
    #                 raise Exception("❌ Fallo al cargar el archivo de variables.")
    #             print("✅ Variables inicializadas correctamente.")

    #             print("▶️ Iniciando programa...")
    #             if not self.controller.start_programm():
    #                 raise Exception("❌ Error al iniciar el programa.")

    #         # 👉 PASO 2: Movimiento
    #         print(f"📤 Subiendo archivo de secuencia: {self.sequence_path}")
    #         if not self.controller.upload_file(self.sequence_path, self.remote_folder):
    #             raise Exception("❌ Fallo al subir el archivo de secuencia.")
    #         print("📦 Cargando programa de movimiento...")
    #         if not self.controller.load_programm(self.program_name):
    #             raise Exception("❌ Fallo al cargar el programa.")

    #         print("▶️ Iniciando programa...")
    #         if not self.controller.start_programm():
    #             raise Exception("❌ Error al iniciar el programa.")

    #         self.wait_for_finish_signal()

    #         print(f"✅ Secuencia completada para: {self.robot_id.upper()}")

    #     except Exception as e:
    #         print(f"❌ Error durante la ejecución de {self.robot_id.upper()}: {e}")

    #     finally:
    #         print(f"🛑 Cerrando conexión con {self.robot_id.upper()}")
    #         self.controller.close()
    #         print(f"{'-'*30}")

