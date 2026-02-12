from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel, QSlider, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPointF, QTimer, QRectF, QTime, QPoint
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QPainterPath, QPen, QFont
import requests
from interfaz.estilos import ESTILO_CONTROLES

# --- WIDGET DE CARGA OPTIMIZADO ---
class CargaAnimada(QWidget):
    def __init__(self, parent_window_to_center_on):
        super().__init__(None)
        self.target_widget = parent_window_to_center_on
        self.setFixedSize(220, 60)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotar)
        self.texto = "CONECTANDO..."

    def rotar(self):
        self.angle = (self.angle + 30) % 360
        self.update()
        if self.isVisible():
            self.centrar_en_objetivo()

    def start(self):
        self.centrar_en_objetivo()
        self.show()
        # OPTIMIZACIÓN: 80ms en lugar de 50ms (Menos uso de CPU, misma fluidez visual)
        self.timer.start(80) 

    def stop(self):
        self.timer.stop()
        self.hide()

    def centrar_en_objetivo(self):
        if not self.target_widget or not self.target_widget.isVisible(): return
        geo = self.target_widget.mapToGlobal(QPoint(0, 0))
        x = geo.x() + (self.target_widget.width() - self.width()) // 2
        y = geo.y() + (self.target_widget.height() - self.height()) // 2
        self.move(x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0, 0, 0, 200))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 30, 30)
        
        painter.save()
        painter.translate(35, 30)
        painter.rotate(self.angle)
        pen = QPen(QColor("#E50914"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(QRectF(-12, -12, 24, 24), 0, 180 * 16)
        painter.restore()

        painter.setPen(QColor("white"))
        font = painter.font()
        font.setBold(True); font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(QRectF(60, 0, 150, 60), Qt.AlignmentFlag.AlignVCenter, self.texto)

class BotonPlay(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(56, 56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.es_reproduciendo = False 
        self.hover = False 
        # OPTIMIZACIÓN: Eliminada la sombra (DropShadow) para mejorar FPS en PCs lentas

    def enterEvent(self, event): self.hover = True; self.update(); super().enterEvent(event)
    def leaveEvent(self, event): self.hover = False; self.update(); super().leaveEvent(event)
    def set_playing(self, estado): self.es_reproduciendo = estado; self.update() 

    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color_fondo = QColor("#ff1f2a") if self.hover else QColor("#E50914") 
        if self.isDown(): color_fondo = QColor("#c4000d") 
        painter.setBrush(color_fondo); painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())
        painter.setBrush(QColor("white"))
        w, h = self.width(), self.height()
        if self.es_reproduciendo:
            x1 = (w/2)-9; y1 = (h-20)/2
            p = QPainterPath(); p.addRoundedRect(x1, y1, 6, 20, 3, 3); p.addRoundedRect((w/2)+3, y1, 6, 20, 3, 3)
            painter.drawPath(p)
        else:
            p = QPainterPath()
            p.moveTo((w/2)-4, (h/2)-10); p.lineTo((w/2)-4, (h/2)+10); p.lineTo((w/2)+12, (h/2)); p.closeSubpath()
            painter.drawPath(p)

class LogoLoader(QThread):
    imagen_cargada = pyqtSignal(QPixmap)
    def run(self):
        url = getattr(self, 'url_logo', "")
        if not url: self.imagen_cargada.emit(QPixmap()); return
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3) # Timeout reducido a 3s
            if r.status_code == 200:
                img = QImage(); img.loadFromData(r.content)
                self.imagen_cargada.emit(QPixmap.fromImage(img))
            else: self.imagen_cargada.emit(QPixmap())
        except: self.imagen_cargada.emit(QPixmap())

class Controles(QFrame):
    def __init__(self, engine, toggle_fs_callback, parent_video): 
        super().__init__()
        self.setObjectName("Controles")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(ESTILO_CONTROLES)
        self.setFixedHeight(100)
        self.setFixedWidth(850)

        self.engine = engine; self.toggle_fs = toggle_fs_callback; self.parent_v = parent_video
        self.loading_widget = CargaAnimada(self.parent_v)
        self.loader = LogoLoader(); self.loader.imagen_cargada.connect(self.mostrar_logo)
        
        layout = QHBoxLayout(self); layout.setContentsMargins(25, 10, 25, 10); layout.setSpacing(20)

        left_box = QWidget(); left_layout = QHBoxLayout(left_box); left_layout.setContentsMargins(0,0,0,0); left_layout.setSpacing(15)
        self.lbl_logo_img = QLabel(); self.lbl_logo_img.setFixedSize(50, 50); self.lbl_logo_img.setScaledContents(True); self.lbl_logo_img.hide()
        left_layout.addWidget(self.lbl_logo_img)
        
        text_box = QWidget(); text_layout = QVBoxLayout(text_box); text_layout.setContentsMargins(0,0,0,0); text_layout.setSpacing(0)
        self.lbl_info = QLabel("Bienvenido")
        self.lbl_info.setStyleSheet("color: white; font-size: 18px; font-weight: bold; font-family: 'Segoe UI';")
        self.lbl_sub = QLabel("Selecciona un canal")
        self.lbl_sub.setStyleSheet("color: #b3b3b3; font-size: 13px; font-family: 'Segoe UI'; margin-top: 2px;")
        
        self.progreso_guia = QProgressBar()
        self.progreso_guia.setFixedHeight(3)
        self.progreso_guia.setStyleSheet("QProgressBar { background: #333; border: none; } QProgressBar::chunk { background: #E50914; }")
        self.progreso_guia.setValue(50); self.progreso_guia.setTextVisible(False)
        
        text_layout.addWidget(self.lbl_info); text_layout.addWidget(self.lbl_sub); text_layout.addSpacing(5); text_layout.addWidget(self.progreso_guia)
        left_layout.addWidget(text_box); layout.addWidget(left_box); layout.addStretch() 

        self.btn_play = BotonPlay(); self.btn_play.clicked.connect(self.toggle_play)
        layout.addWidget(self.btn_play); layout.addStretch() 

        self.lbl_live = QLabel("● EN VIVO"); self.lbl_live.setObjectName("LiveTag"); layout.addWidget(self.lbl_live)
        self.btn_vol_icon = QPushButton("🔊"); self.btn_vol_icon.setObjectName("BtnIcon"); layout.addWidget(self.btn_vol_icon)
        self.slider = QSlider(Qt.Orientation.Horizontal); self.slider.setFixedWidth(100); self.slider.setRange(0, 100); self.slider.setValue(100)
        self.slider.valueChanged.connect(self.engine.set_volume); layout.addWidget(self.slider)
        self.btn_fs = QPushButton("⛶"); self.btn_fs.setObjectName("BtnIcon"); self.btn_fs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fs.clicked.connect(self.toggle_fs); layout.addWidget(self.btn_fs)

    def mostrar_carga(self):
        self.loading_widget.centrar_en_objetivo()
        self.loading_widget.start()

    def reubicar_carga(self):
        if self.loading_widget.isVisible(): self.loading_widget.centrar_en_objetivo()

    def ocultar_carga(self): self.loading_widget.stop()

    def closeEvent(self, event):
        self.loading_widget.close()
        super().closeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        painter.setBrush(QColor("#121212")); painter.setPen(Qt.PenStyle.NoPen) 
        painter.drawRoundedRect(self.rect(), 16, 16) 

    def toggle_play(self): self.btn_play.set_playing(self.engine.toggle_pause())

    def actualizar_info(self, nombre, logo_url):
        self.lbl_info.setText(nombre.upper())
        hora = QTime.currentTime().toString("HH:mm")
        self.lbl_sub.setText(f"🕒 {hora} | Transmisión en directo")
        self.btn_play.set_playing(True); self.lbl_logo_img.clear(); self.lbl_logo_img.hide()
        if logo_url and len(logo_url) > 5: self.loader.url_logo = logo_url; self.loader.start()

    def mostrar_logo(self, pixmap):
        if not pixmap.isNull(): self.lbl_logo_img.setPixmap(pixmap); self.lbl_logo_img.show()