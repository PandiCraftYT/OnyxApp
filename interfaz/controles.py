from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel, QSlider, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPointF
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QPainterPath, QPen
import requests
from interfaz.estilos import ESTILO_CONTROLES

# --- NUEVA CLASE: BOTÓN DE PLAY DIBUJADO A MANO ---
class BotonPlay(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(56, 56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.es_reproduciendo = False 
        self.hover = False 

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.hover = True
        self.update() 
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover = False
        self.update() 
        super().leaveEvent(event)

    def set_playing(self, estado):
        self.es_reproduciendo = estado
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 1. DIBUJAR CÍRCULO DE FONDO
        color_fondo = QColor("#ff1f2a") if self.hover else QColor("#E50914") 
        if self.isDown(): color_fondo = QColor("#c4000d") 
        
        painter.setBrush(color_fondo)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

        # 2. DIBUJAR ICONO BLANCO
        painter.setBrush(QColor("white"))
        
        w = self.width()
        h = self.height()
        
        if self.es_reproduciendo:
            # --- DIBUJAR PAUSA (Dos barras) ---
            ancho_barra = 6
            alto_barra = 20
            espacio = 6
            
            x1 = (w / 2) - ancho_barra - (espacio / 2)
            y1 = (h - alto_barra) / 2
            path = QPainterPath()
            path.addRoundedRect(x1, y1, ancho_barra, alto_barra, 3, 3) 
            
            x2 = (w / 2) + (espacio / 2)
            path.addRoundedRect(x2, y1, ancho_barra, alto_barra, 3, 3)
            
            painter.drawPath(path)
            
        else:
            # --- DIBUJAR PLAY (Triángulo) ---
            offset_x = 2 
            
            path = QPainterPath()
            p1 = QPointF((w / 2) - 6 + offset_x, (h / 2) - 10) 
            p2 = QPointF((w / 2) - 6 + offset_x, (h / 2) + 10) 
            p3 = QPointF((w / 2) + 10 + offset_x, (h / 2))     
            
            path.moveTo(p1)
            path.lineTo(p2)
            path.lineTo(p3)
            path.lineTo(p1)
            
            pen = QPen(QColor("white"), 3)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            
            # 👇 CORRECCIÓN AQUÍ: setPen en lugar de setStroke
            painter.setPen(pen) 
            
            painter.drawPath(path)

# --- FIN DE LA NUEVA CLASE ---


class LogoLoader(QThread):
    imagen_cargada = pyqtSignal(QPixmap)
    def run(self):
        url = getattr(self, 'url_logo', "")
        if not url: 
            self.imagen_cargada.emit(QPixmap())
            return
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                img = QImage()
                img.loadFromData(response.content)
                self.imagen_cargada.emit(QPixmap.fromImage(img))
            else: self.imagen_cargada.emit(QPixmap())
        except: self.imagen_cargada.emit(QPixmap())

class Controles(QFrame):
    def __init__(self, engine, toggle_fs_callback):
        super().__init__()
        self.setObjectName("Controles")
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.setStyleSheet(ESTILO_CONTROLES)
        self.setFixedHeight(85)
        self.setFixedWidth(780) 

        self.engine = engine
        self.toggle_fs = toggle_fs_callback
        self.loader = LogoLoader()
        self.loader.imagen_cargada.connect(self.mostrar_logo)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 10, 25, 10)
        layout.setSpacing(20)

        # IZQUIERDA
        left_box = QWidget()
        left_layout = QHBoxLayout(left_box)
        left_layout.setContentsMargins(0,0,0,0)
        left_layout.setSpacing(15)

        self.lbl_logo_img = QLabel()
        self.lbl_logo_img.setFixedSize(42, 42)
        self.lbl_logo_img.setScaledContents(True)
        self.lbl_logo_img.hide()
        left_layout.addWidget(self.lbl_logo_img)

        text_box = QWidget()
        text_layout = QVBoxLayout(text_box)
        text_layout.setContentsMargins(0,4,0,4)
        text_layout.setSpacing(2)
        
        self.lbl_info = QLabel("Bienvenido")
        self.lbl_info.setObjectName("TituloInfo") 
        self.lbl_sub = QLabel("Selecciona un canal")
        self.lbl_sub.setObjectName("SubInfo")
        
        text_layout.addWidget(self.lbl_info)
        text_layout.addWidget(self.lbl_sub)
        left_layout.addWidget(text_box)
        
        layout.addWidget(left_box)
        layout.addStretch() 

        # CENTRO
        self.btn_play = BotonPlay() 
        self.btn_play.clicked.connect(self.toggle_play)
        layout.addWidget(self.btn_play)
        layout.addStretch() 

        # DERECHA
        self.lbl_live = QLabel("● EN VIVO")
        self.lbl_live.setObjectName("LiveTag")
        layout.addWidget(self.lbl_live)

        self.btn_vol_icon = QPushButton("🔊")
        self.btn_vol_icon.setObjectName("BtnIcon")
        layout.addWidget(self.btn_vol_icon)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setFixedWidth(120) 
        self.slider.setRange(0, 100)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.engine.set_volume)
        layout.addWidget(self.slider)

        self.btn_fs = QPushButton("⛶")
        self.btn_fs.setObjectName("BtnIcon")
        self.btn_fs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fs.clicked.connect(self.toggle_fs)
        layout.addWidget(self.btn_fs)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        painter.setBrush(QColor("#121212")) 
        painter.setPen(Qt.PenStyle.NoPen) 
        rect = self.rect()
        painter.drawRoundedRect(rect, 16, 16) 

    def toggle_play(self):
        playing = self.engine.toggle_pause()
        self.btn_play.set_playing(playing)

    def actualizar_info(self, nombre, logo_url):
        self.lbl_info.setText(nombre)
        self.lbl_sub.setText("Reproduciendo ahora")
        self.btn_play.set_playing(True)
        self.lbl_logo_img.clear()
        self.lbl_logo_img.hide()
        if logo_url and len(logo_url) > 5:
            self.loader.url_logo = logo_url
            self.loader.start()

    def mostrar_logo(self, pixmap):
        if not pixmap.isNull():
            self.lbl_logo_img.setPixmap(pixmap)
            self.lbl_logo_img.show()