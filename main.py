import sys, ctypes, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QEvent
from PyQt6.QtGui import QIcon
from logica.parser import cargar_canales
from logica.reproductor import VideoEngine
from interfaz.sidebar import Sidebar
from interfaz.controles import Controles
from interfaz.estilos import ESTILO_MAIN

def obtener_ruta_recurso(relativa):
    try: base = sys._MEIPASS
    except: base = os.path.abspath(".")
    return os.path.join(base, relativa)

class OnyxApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ONYX PLAY - PC")
        self.setWindowIcon(QIcon(obtener_ruta_recurso("onix.ico"))) 
        self.resize(1280, 720); self.setStyleSheet(ESTILO_MAIN); self.setMouseTracking(True)
        self.canales = cargar_canales(); self.engine = VideoEngine()

        central = QWidget(); central.setMouseTracking(True); self.setCentralWidget(central)
        self.layout = QHBoxLayout(central); self.layout.setContentsMargins(0, 0, 0, 0); self.layout.setSpacing(0)

        self.sidebar = Sidebar(self.canales); self.sidebar.canal_seleccionado.connect(self.reproducir)
        self.video_cont = QFrame(); self.video_cont.setObjectName("VideoContainer")
        self.video_cont.setStyleSheet("background-color: black;"); self.video_cont.setMouseTracking(True)
        self.layout.addWidget(self.sidebar); self.layout.addWidget(self.video_cont)

        self.controles = Controles(self.engine, self.toggle_fullscreen, self.video_cont)
        self.controles.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.controles.show()

        QTimer.singleShot(100, self.centrar_controles)
        self.anim_w = QPropertyAnimation(self.sidebar, b"minimumWidth"); self.anim_w.setDuration(300); self.anim_w.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.anim_w.valueChanged.connect(lambda: self.centrar_controles())
        self.anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth"); self.anim_max.setDuration(300)
        self.menu_abierto = False

    def changeEvent(self, e):
        if e.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow(): self.controles.show(); self.controles.raise_(); self.centrar_controles()
            else: self.controles.hide()
        super().changeEvent(e)

    def moveEvent(self, e): self.centrar_controles(); super().moveEvent(e)
    def resizeEvent(self, e): self.centrar_controles(); super().resizeEvent(e)
    def closeEvent(self, e): self.controles.close(); super().closeEvent(e)

    def centrar_controles(self):
        if not self.isVisible() or self.isMinimized(): return
        g = self.video_cont.mapToGlobal(QPoint(0, 0))
        x = g.x() + (self.video_cont.width() - self.controles.width()) // 2
        y = g.y() + self.video_cont.height() - self.controles.height() - 40 
        self.controles.move(x, y)
        self.controles.reubicar_carga()

    def toggle_menu(self, abrir):
        if abrir == self.menu_abierto: return
        w = 300 if abrir else 0
        self.anim_w.stop(); self.anim_max.stop()
        self.anim_w.setEndValue(w); self.anim_max.setEndValue(w)
        self.anim_w.start(); self.anim_max.start()
        self.menu_abierto = abrir

    def mouseMoveEvent(self, e):
        if e.pos().x() < 30: self.toggle_menu(True)
        elif e.pos().x() > 320: self.toggle_menu(False)
        super().mouseMoveEvent(e)

    def reproducir(self, url, nombre, logo):
        self.engine.reproducir(url, int(self.video_cont.winId()))
        self.controles.actualizar_info(nombre, logo)
        self.controles.mostrar_carga() 
        QTimer.singleShot(4000, self.controles.ocultar_carga)
        self.toggle_menu(False); self.controles.show(); self.controles.raise_()
        QTimer.singleShot(200, self.centrar_controles)

    def toggle_fullscreen(self):
        if self.isFullScreen(): self.showNormal()
        else: self.showFullScreen()
        self.toggle_menu(False); QTimer.singleShot(100, self.centrar_controles); self.controles.raise_()

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton: self.toggle_fullscreen()

if __name__ == "__main__":
    try: ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('onyx.play.v3')
    except: pass
    app = QApplication(sys.argv); app.setWindowIcon(QIcon(obtener_ruta_recurso("onix.ico")))
    win = OnyxApp(); win.show(); sys.exit(app.exec())