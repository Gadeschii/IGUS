import time
from cri_lib import CRIController

class IgusRobot:
    def __init__(self, ip, port, program_name, sequence_path, remote_folder="Programs"):
        self.ip = ip
        self.port = port
        self.program_name = program_name
        self.sequence_path = sequence_path
        self.remote_folder = remote_folder
        self.controller = CRIController()
        self._last_status = None

        # Registrar callback de estado
        self.controller.register_status_callback(self.status_callback)

    def status_callback(self, state):
        self._last_status = state

    def wait_for_finish_signal(self, signal_id="isFinish", timeout=30):
        print(f"⏳ Esperando variable {signal_id} = True...")
        start = time.time()
        print("-->")
        signal_value = self.controller.get_global_signal(signal_id)
        print("-->" + str(signal_value))
        while time.time() - start < timeout:
            self.controller.wait_for_status_update(timeout=1)
            ##signal_value = self.controller.robot_state.global_signals.__getstate__ sget(signal_id, False)
            
            # if signal_value:
            #     print(f"✅ Señal global {signal_id} detectada. Secuencia finalizada.")
            #     return

            # time.sleep(0.5)
        print("-->")
        signal_value = self.controller.get_global_signal(signal_id)
        print("-->" + str(signal_value))
        raise TimeoutError(f"❌ Señal global {signal_id} no detectada dentro del tiempo.")



    def run(self):
        try:
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

            print("✅ Esperando a que el robot esté listo para moverse (Kinematics Ready)...")
            if not self.controller.wait_for_kinematics_ready(timeout=30):
                raise Exception("❌ El robot no está listo para moverse.")

            print(f"📤 Subiendo archivo: {self.sequence_path}")
            if not self.controller.upload_file(self.sequence_path, self.remote_folder):
                raise Exception("❌ Fallo al subir el archivo.")
            else:
                print("✅ Archivo cargado correctamente.")

            print("📦 Cargando programa en el robot...")
            if not self.controller.load_programm(self.program_name):
                raise Exception("❌ Fallo al cargar el programa.")

            print("▶️ Iniciando programa...")
            if not self.controller.start_programm():
                raise Exception("❌ Error al iniciar el programa.")

            # Esperar a que termine la ejecución
            self.wait_for_finish_signal()

        except Exception as e:
            print(f"❌ Error durante la ejecución: {e}")

        finally:
            print("🛑 Cerrando conexión...")
            self.controller.close()
