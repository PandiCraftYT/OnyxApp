import os
import sys
import vlc
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

# --- CONFIGURACIÓN DE RUTAS VLC ---
VLC_PATH = os.path.abspath(".")
if os.path.exists(os.path.join(VLC_PATH, "libvlc.dll")):
    os.add_dll_directory(VLC_PATH)
else:
    VLC_STD = r"C:\Program Files\VideoLAN\VLC"
    if os.path.exists(VLC_STD):
        os.add_dll_directory(VLC_STD)

class VideoEngine(QObject):
    reintentar_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # --- CONFIGURACIÓN OPTIMIZADA PARA BAJOS RECURSOS ---
        mis_argumentos = [
            "--quiet",
            "--no-xlib",
            "--no-video-title-show",
            "--no-stats",                 # Ahorra CPU desactivando estadísticas
            "--skip-frames",              # Salta cuadros si la CPU va lenta
            "--drop-late-frames",         # Descarta video atrasado para no congelarse
            "--avcodec-hw=any",           # Usa la GPU si existe, si no, usa CPU eficientemente
            "--network-caching=1500",     # 1.5s: Equilibrio perfecto entre rapidez y estabilidad
            
            # Camuflaje estándar
            "--http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]

        self.instance = vlc.Instance(mis_argumentos)
        
        # Rescate si falla la inicialización
        if not self.instance:
            self.instance = vlc.Instance()

        self.player = self.instance.media_player_new()
        
        self.ultima_url = None
        self.ultimo_win_id = None
        
        self.reintentar_signal.connect(self._ejecutar_reintento_seguro)
        
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEncounteredError, self._manejador_errores)
        self.events.event_attach(vlc.EventType.MediaPlayerOpening, self._log_estado)
        self.events.event_attach(vlc.EventType.MediaPlayerBuffering, self._log_estado)

        self.player.video_set_mouse_input(False)
        self.player.video_set_key_input(False)

    def _log_estado(self, event):
        # Logs mínimos para no saturar consola
        pass 

    def _manejador_errores(self, event):
        print("❌ Reintentando conexión...")
        self.reintentar_signal.emit()

    def _ejecutar_reintento_seguro(self):
        if self.ultima_url:
            QTimer.singleShot(2000, lambda: self.reproducir(self.ultima_url, self.ultimo_win_id))

    def reproducir(self, url, win_id):
        self.ultima_url = url
        self.ultimo_win_id = win_id
        
        self.player.stop()
        media = self.instance.media_new(url)

        # Opciones críticas para evitar bloqueos
        media.add_option(":network-caching=1500")
        media.add_option(":http-reconnect=true")
        media.add_option(":http-continuous=1")
        media.add_option(":http-ssl-verify=0") 
        media.add_option(":avcodec-hw=any") 
        
        # Headers necesarios
        media.add_option(":http-forward-cookies=1")
        media.add_option(":http-referrer=https://mdstrm.com/") 
        media.add_option(":http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        self.player.set_media(media)

        if sys.platform.startswith("win"):
            self.player.set_hwnd(win_id)
        elif sys.platform.startswith("linux"):
            self.player.set_xwindow(win_id)

        self.player.play()

    def set_volume(self, val):
        self.player.audio_set_volume(int(val))

    def toggle_pause(self):
        if self.player.is_playing():
            self.player.pause()
            return False 
        else:
            self.player.play()
            return True