import os
import sys
import vlc

# --- CONFIGURACIÓN DE RUTAS VLC ---
# Buscamos donde está instalado VLC para que Python lo encuentre sin errores
VLC_PATH = r"C:\Program Files\VideoLAN\VLC"
if os.path.exists(VLC_PATH):
    os.add_dll_directory(VLC_PATH)
    os.environ['PYTHON_VLC_MODULE_PATH'] = VLC_PATH

class VideoEngine:
    def __init__(self):
        # --- CAMUFLAJE NIVEL MILITAR ---
        # Argumentos para que el servidor crea que somos Google Chrome y no bloquee
        mis_argumentos = [
            "--quiet",
            "--no-xlib",
            "--network-caching=1500",   # 1.5 segundos de buffer (Mayor estabilidad)
            "--http-reconnect",         # Reconectar automáticamente si parpadea la red
            # User-Agent de Chrome en Windows 10
            "--http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]

        self.instance = vlc.Instance(mis_argumentos)
        self.player = self.instance.media_player_new()

        # --- TRUCO MAESTRO PARA PYQT6 ---
        # Le decimos a VLC: "Ignora el mouse y el teclado".
        # De esta forma, los clics y movimientos "atraviesan" el video y llegan a nuestra App.
        # Esto permite que el doble clic y el detector de movimiento funcionen.
        self.player.video_set_mouse_input(False)
        self.player.video_set_key_input(False)

    def reproducir(self, url, win_id):
        self.player.stop()

        # Crear el objeto multimedia
        media = self.instance.media_new(url)

        # DOBLE SEGURIDAD: Forzamos el camuflaje también en el archivo individual
        media.add_option(":http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        media.add_option(":http-reconnect=true")
        media.add_option(":network-caching=1500")

        self.player.set_media(media)

        # Conectar el video a la ventana negra de PyQt (Windows o Linux)
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(win_id)
        elif sys.platform.startswith("win"):
            self.player.set_hwnd(win_id)

        self.player.play()

    def toggle_pause(self):
        """Pausa o reanuda y devuelve True si está reproduciendo"""
        if self.player.is_playing():
            self.player.pause()
            return False # Está en Pausa
        else:
            self.player.play()
            return True # Está Reproduciendo

    def set_volume(self, val):
        self.player.audio_set_volume(int(val))