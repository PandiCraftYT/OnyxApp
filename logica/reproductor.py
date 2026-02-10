import os
import sys
import vlc

# --- CONFIGURACIÓN DE RUTAS VLC ---
VLC_PATH = r"C:\Program Files\VideoLAN\VLC"
if os.path.exists(VLC_PATH):
    os.add_dll_directory(VLC_PATH)
    os.environ['PYTHON_VLC_MODULE_PATH'] = VLC_PATH

class VideoEngine:
    def __init__(self):
        # 👇 AQUÍ ESTÁ EL CAMUFLAJE
        # Le decimos a VLC que se comporte EXACTAMENTE como Google Chrome en Windows 10
        mis_argumentos = [
            "--quiet",
            "--no-xlib",
            "--network-caching=1500",   # 1.5 segundos de buffer para estabilidad
            "--http-reconnect",         # Reconectar si se cae
            "--http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]
        
        self.instance = vlc.Instance(mis_argumentos)
        self.player = self.instance.media_player_new()
        
    def reproducir(self, url, win_id):
        self.player.stop()
        
        # Crear el objeto multimedia
        media = self.instance.media_new(url)
        
        # 👇 DOBLE SEGURIDAD: Forzamos las opciones también en el archivo individual
        media.add_option(":http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        media.add_option(":http-reconnect=true")
        media.add_option(":network-caching=1500")
        
        self.player.set_media(media)
        
        # Conectar el video a la ventana de PyQt (Windows o Linux)
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(win_id)
        elif sys.platform.startswith("win"):
            self.player.set_hwnd(win_id)
            
        self.player.play()

    def toggle_pause(self):
        """Pausa o reanuda y devuelve True si está reproduciendo"""
        if self.player.is_playing():
            self.player.pause()
            return False 
        else:
            self.player.play()
            return True 

    def set_volume(self, val):
        self.player.audio_set_volume(int(val))