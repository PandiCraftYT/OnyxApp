import sys
import ctypes
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QEvent
from PyQt6.QtGui import QIcon
from logica.parser import cargar_canales
from logica.reproductor import VideoEngine
from interfaz.sidebar import Sidebar
from interfaz.controles import Controles
from interfaz.estilos import ESTILO_MAIN

def obtener_ruta_recurso(relativa):
    """ Función para encontrar archivos tanto en desarrollo como en el .exe """
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, relativa)

class OnyxApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ONYX PLAY - PC")
        
        # 👇 CONFIGURACIÓN DEL ICONO (Asegúrate que onix.ico esté en la carpeta raíz)
        ruta_icono = obtener_ruta_recurso("onix.ico")
        self.setWindowIcon(QIcon(ruta_icono)) 
        
        self.resize(1280, 720)
        self.setStyleSheet(ESTILO_MAIN)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.canales = cargar_canales()
        self.engine = VideoEngine()

        central_widget = QWidget()
        central_widget.setMouseTracking(True) 
        self.setCentralWidget(central_widget)
        
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.sidebar = Sidebar(self.canales)
        self.sidebar.canal_seleccionado.connect(self.reproducir)
        self.main_layout.addWidget(self.sidebar)

        self.video_container = QFrame()
        self.video_container.setMouseTracking(True)
        self.video_container.setObjectName("VideoContainer")
        self.video_container.setStyleSheet("background-color: black;")
        self.video_container.setCursor(Qt.CursorShape.ArrowCursor)
        self.main_layout.addWidget(self.video_container)

        self.controles = Controles(self.engine, self.toggle_fullscreen)
        self.controles.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool 
        )
        self.controles.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.controles.show()

        QTimer.singleShot(100, self.centrar_controles)

        self.animacion_menu = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animacion_menu.setDuration(300) 
        self.animacion_menu.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animacion_menu.valueChanged.connect(lambda: self.centrar_controles())
        
        self.animacion_menu_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.animacion_menu_max.setDuration(300)
        
        self.menu_abierto = False

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                self.controles.show()
                self.controles.raise_()
                self.centrar_controles()
            else:
                self.controles.hide()
        elif event.type() == QEvent.Type.WindowStateChange:
            if self.isMinimized():
                self.controles.hide()
            elif self.isVisible():
                self.controles.show()
        super().changeEvent(event)

    def moveEvent(self, event):
        self.centrar_controles()
        super().moveEvent(event)
        
    def resizeEvent(self, event):
        self.centrar_controles()
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.controles.close()
        super().closeEvent(event)

    def centrar_controles(self):
        if not self.isVisible() or self.isMinimized(): return
        geo_global = self.video_container.mapToGlobal(QPoint(0, 0))
        x_pos = geo_global.x() + (self.video_container.width() - self.controles.width()) // 2
        y_pos = geo_global.y() + self.video_container.height() - self.controles.height() - 40 
        self.controles.move(x_pos, y_pos)

    def toggle_menu(self, abrir):
        if abrir and self.menu_abierto: return
        if not abrir and not self.menu_abierto: return
        ancho = 300 if abrir else 0
        self.animacion_menu.stop()
        self.animacion_menu_max.stop()
        self.animacion_menu.setEndValue(ancho)
        self.animacion_menu_max.setEndValue(ancho)
        self.animacion_menu.start()
        self.animacion_menu_max.start()
        self.menu_abierto = abrir

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        if x < 30: self.toggle_menu(True)
        elif x > 320: self.toggle_menu(False)
        super().mouseMoveEvent(event)

    def reproducir(self, url, nombre, logo):
        win_id = int(self.video_container.winId())
        self.engine.reproducir(url, win_id)
        self.controles.actualizar_info(nombre, logo)
        self.toggle_menu(False)
        self.controles.show()
        self.controles.raise_()
        QTimer.singleShot(200, self.centrar_controles)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        self.toggle_menu(False) 
        QTimer.singleShot(100, self.centrar_controles)
        self.controles.raise_()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_fullscreen()

if __name__ == "__main__":
    # 👇 ID ÚNICO PARA FORZAR EL ICONO EN LA BARRA DE TAREAS
    try:
        myappid = 'onyx.play.system.final.v3' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

    app = QApplication(sys.argv)
    
    # Icono global de la aplicación
    ruta_icon_global = obtener_ruta_recurso("onix.ico")
    app.setWindowIcon(QIcon(ruta_icon_global)) 
    
    ventana = OnyxApp()
    ventana.show()
    sys.exit(app.exec())