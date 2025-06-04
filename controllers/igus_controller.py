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

    def wait_for_finish_signal(self, signal_base="isfinish"):
        variable_name = f"{signal_base}{self.robot_id}" 
        print(f"⏳ Esperando que la variable '{variable_name}' sea 1...")
        start = time.time()
        self.controller.robot_state.variabels[variable_name] = 0
        while time.time() - start < self.wait_timeout:
            self.controller.wait_for_status_update(timeout=1)
            try:
                value = 0
                
                print(f"🔎 {variable_name} = {value}")
                value = int(self.controller.robot_state.variabels[variable_name])
                print(f"🔎 {variable_name} = {value}")
                if value == 1:
                    print(f"✅ Señal '{variable_name}' detectada.")
                    return
            except Exception as e:
                print(f"⚠️ Error al leer variable '{variable_name}': {e}")
            time.sleep(0.5)
        raise TimeoutError("❌ Timeout: ninguna condición se cumplió en el tiempo límite.")

    
    def set_start_signal(self):
        var_name = f"start{self.robot_id.lower()}"
        print(f"🚦 Activando señal: {var_name} = 1")
        self.controller.robot_state.variabels[var_name] = 1

    def load_variables(self):
        if self.var_file:
            print(f"📤 (Precarga) Subiendo archivo de variables: {self.var_file}")
            if not self.controller.upload_file(self.var_file, self.remote_folder):
                raise Exception("❌ Fallo al subir archivo de variables.")
            if not self.controller.load_programm(self.var_file):
                raise Exception("❌ Fallo al cargar archivo de variables.")
            print("✅ Variables cargadas.")
            self.controller.start_programm()

    # def wait_for_finish_signal(self, signal_base="isfinish"):
    #     variable_name = f"{signal_base}{self.robot_id}" 
    #     print(f"⏳ Esperando que la variable '{variable_name}' sea 1...")
    #     start = time.time()
    #     self.controller.robot_state.variabels[variable_name] = 0
    #     while time.time() - start < self.wait_timeout:
    #         self.controller.wait_for_status_update(timeout=1)
    #         try:
    #             value = int(self.controller.robot_state.variabels[variable_name])
    #             print(f"🔎 {variable_name} = {value}")
    #             if value == 1:
    #                 print(f"✅ Señal '{variable_name}' detectada.")
    #                 return
    #         except Exception as e:
    #             print(f"⚠️ Error al leer variable '{variable_name}': {e}")
    #         time.sleep(0.5)

    #     raise TimeoutError(f"❌ Timeout: '{variable_name}' no se volvió 1 en {self.wait_timeout} segundos.")
        
    def run(self):
        try:
            print(f"\n{'='*30}")
            print(f"▶️  Ejecutando secuencia para: {self.robot_id.upper()}")
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

            print("✅ Esperando a que el robot esté listo para moverse...")
            if not self.controller.wait_for_kinematics_ready(timeout=30):
                raise Exception("❌ El robot no está listo para moverse.")

            # Esperar condiciones específicas antes de iniciar la secuencia
            if self.robot_id.upper() == "SCARA":
                print("⏳ Esperando condiciones en REBELLINE...")
                conditions = [("startrebelline", 1), ("isfinishrebelline", 1), ("posdropobjrebelline", 1)]
                if not self.wait_for_variable_condition(conditions, timeout=30):
                    raise Exception("❌ Timeout: condiciones en REBELLINE no se cumplieron.")

            # 👉 PASO 1: Variables == 0
            if self.var_file:
                print(f"📤 Subiendo archivo de variables: {self.var_file}")
                if not self.controller.upload_file(self.var_file, self.remote_folder):
                    raise Exception("❌ Fallo al subir el archivo de variables.")
                print("📦 Cargando archivo de variables...")
                if not self.controller.load_programm(self.var_file):
                    raise Exception("❌ Fallo al cargar el archivo de variables.")
                print("✅ Variables inicializadas correctamente.")

            # 👉 PASO 2: Movimiento
            print(f"📤 Subiendo archivo de secuencia: {self.sequence_path}")
            if not self.controller.upload_file(self.sequence_path, self.remote_folder):
                raise Exception("❌ Fallo al subir el archivo de secuencia.")
            print("📦 Cargando programa de movimiento...")
            if not self.controller.load_programm(self.program_name):
                raise Exception("❌ Fallo al cargar el programa.")

            print("▶️ Iniciando programa...")
            if not self.controller.start_programm():
                raise Exception("❌ Error al iniciar el programa.")

            # Esperar a que la secuencia termine
            print(f"⏳ Esperando que la variable 'isfinish{self.robot_id.lower()}' sea 1...")
            finish_variable = f"isfinish{self.robot_id.lower()}"
            if not self.wait_for_variable_condition([(finish_variable, 1)], timeout=30):
                raise Exception(f"❌ Timeout: '{finish_variable}' no se volvió 1 en 30 segundos.")

            print(f"✅ Secuencia completada para: {self.robot_id.upper()}")

        except Exception as e:
            print(f"❌ Error durante la ejecución de {self.robot_id.upper()}: {e}")

        finally:
            print(f"🛑 Cerrando conexión con {self.robot_id.upper()}")
            self.controller.close()
            print(f"{'-'*30}")


