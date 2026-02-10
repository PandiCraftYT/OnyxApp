import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, QEvent
from logica.parser import cargar_canales
from logica.reproductor import VideoEngine
from interfaz.sidebar import Sidebar
from interfaz.controles import Controles
from interfaz.estilos import ESTILO_MAIN

class OnyxApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ONYX PLAY - PC")
        self.resize(1280, 720)
        self.setStyleSheet(ESTILO_MAIN)
        
        # 1. RASTREO EN LA VENTANA PRINCIPAL
        self.setMouseTracking(True) 

        self.canales = cargar_canales()
        self.engine = VideoEngine()

        central_widget = QWidget()
        central_widget.setMouseTracking(True) # Rastrear también aquí
        self.setCentralWidget(central_widget)
        
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = Sidebar(self.canales)
        self.sidebar.canal_seleccionado.connect(self.reproducir)
        self.main_layout.addWidget(self.sidebar)

        # VIDEO CONTAINER
        self.video_container = QFrame()
        self.video_container.setObjectName("VideoContainer")
        self.video_container.setStyleSheet("background-color: black;")
        
        # 👇👇👇 ¡ESTA ES LA LÍNEA QUE FALTABA! 👇👇👇
        # Sin esto, el video ignora tu mouse si no haces clic
        self.video_container.setMouseTracking(True) 
        
        self.main_layout.addWidget(self.video_container)

        # CONTROLES FLOTANTES
        self.controles = Controles(self.engine, self.toggle_fullscreen)
        self.controles.setParent(self.video_container)
        
        # Timer de inactividad
        self.timer_inactividad = QTimer()
        self.timer_inactividad.setInterval(3000) # 3 segundos
        self.timer_inactividad.timeout.connect(self.ocultar_controles)
        self.controles_visibles = True
        
        # Filtro de eventos
        self.video_container.installEventFilter(self)
        # También instalamos el filtro en la ventana misma por si acaso
        self.installEventFilter(self)

    def reproducir(self, url, nombre, logo):
        win_id = int(self.video_container.winId())
        self.engine.reproducir(url, win_id)
        self.controles.actualizar_info(nombre, logo)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.sidebar.show()
        else:
            self.showFullScreen()
            self.sidebar.hide()
        QTimer.singleShot(100, self.centrar_controles)

    def resizeEvent(self, event):
        self.centrar_controles()
        super().resizeEvent(event)

    def centrar_controles(self):
        ancho_video = self.video_container.width()
        alto_video = self.video_container.height()
        ancho_bar = self.controles.width()
        alto_bar = self.controles.height()

        x_pos = (ancho_video - ancho_bar) // 2
        y_pos = alto_video - alto_bar - 30 
        self.controles.move(x_pos, y_pos)

    # --- DETECTOR DE MOVIMIENTO ---
    def eventFilter(self, source, event):
        # Si el mouse se mueve...
        if event.type() == QEvent.Type.MouseMove:
            self.mostrar_controles()     # Muestra la barra
            self.timer_inactividad.start() # Reinicia el contador a 3 seg
        
        return super().eventFilter(source, event)

    def ocultar_controles(self):
        self.controles.hide()
        self.controles_visibles = False
        # Ocultar cursor SOLO si estamos en pantalla completa
        if self.isFullScreen():
            self.setCursor(Qt.CursorShape.BlankCursor)

    def mostrar_controles(self):
        if not self.controles_visibles:
            self.controles.show()
            self.controles_visibles = True
            self.setCursor(Qt.CursorShape.ArrowCursor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = OnyxApp()
    ventana.show()
    sys.exit(app.exec())