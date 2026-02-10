from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
import requests
from interfaz.estilos import ESTILO_CONTROLES

class LogoLoader(QThread):
    imagen_cargada = pyqtSignal(QPixmap)
    def run(self):
        url = getattr(self, 'url_logo', "")
        if not url: 
            self.imagen_cargada.emit(QPixmap())
            return
        try:
            data = requests.get(url, timeout=3).content
            image = QImage()
            image.loadFromData(data)
            pixmap = QPixmap.fromImage(image)
            self.imagen_cargada.emit(pixmap)
        except:
            self.imagen_cargada.emit(QPixmap())

class Controles(QFrame):
    def __init__(self, engine, toggle_fs_callback):
        super().__init__()
        self.setObjectName("Controles")
        self.setStyleSheet(ESTILO_CONTROLES)
        self.setFixedHeight(70) # Altura fija
        self.setFixedWidth(750) # Ancho fijo

        self.engine = engine
        self.toggle_fs = toggle_fs_callback
        self.loader = LogoLoader()
        self.loader.imagen_cargada.connect(self.mostrar_logo)

        # LAYOUT PRINCIPAL HORIZONTAL
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 5, 20, 5) # Márgenes internos
        layout.setSpacing(15)

        # --- SECCIÓN IZQUIERDA (Info) ---
        # Contenedor para el logo y texto
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0,0,0,0)
        
        self.lbl_logo_img = QLabel()
        self.lbl_logo_img.setFixedSize(40, 40)
        self.lbl_logo_img.setScaledContents(True)
        left_layout.addWidget(self.lbl_logo_img)
        self.lbl_logo_img.hide() # Oculto por defecto

        info_box = QWidget()
        info_layout = QVBoxLayout(info_box)
        info_layout.setContentsMargins(0,5,0,5)
        info_layout.setSpacing(0)
        
        self.lbl_info = QLabel("Bienvenido")
        self.lbl_info.setStyleSheet("font-weight: bold; font-size: 13px; color: white;")
        self.lbl_sub = QLabel("Selecciona un canal")
        self.lbl_sub.setStyleSheet("font-size: 10px; color: #888;")
        
        info_layout.addWidget(self.lbl_info)
        info_layout.addWidget(self.lbl_sub)
        left_layout.addWidget(info_box)
        
        layout.addWidget(left_container)

        # RESORTE 1: Empuja el Play al centro
        layout.addStretch()

        # --- SECCIÓN CENTRAL (Play) ---
        self.btn_play = QPushButton("▶")
        self.btn_play.setObjectName("BtnPlay")
        self.btn_play.setFixedSize(45, 45)
        self.btn_play.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_play.clicked.connect(self.toggle_play)
        layout.addWidget(self.btn_play)

        # RESORTE 2: Empuja Volumen a la derecha
        layout.addStretch()

        # --- SECCIÓN DERECHA (Herramientas) ---
        self.lbl_live = QLabel("● EN VIVO")
        self.lbl_live.setStyleSheet("color: #E50914; font-weight: bold; font-size: 10px;")
        layout.addWidget(self.lbl_live)

        self.btn_vol_icon = QPushButton("🔊")
        self.btn_vol_icon.setObjectName("BtnIcon")
        layout.addWidget(self.btn_vol_icon)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setFixedWidth(80)
        self.slider.setRange(0, 100)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.engine.set_volume)
        layout.addWidget(self.slider)

        self.btn_fs = QPushButton("⛶")
        self.btn_fs.setObjectName("BtnIcon")
        self.btn_fs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fs.clicked.connect(self.toggle_fs)
        layout.addWidget(self.btn_fs)

    def toggle_play(self):
        playing = self.engine.toggle_pause()
        self.btn_play.setText("❚❚" if playing else "▶")

    def actualizar_info(self, nombre, logo_url):
        self.lbl_info.setText(nombre)
        self.lbl_sub.setText("Reproduciendo ahora")
        self.btn_play.setText("❚❚")
        
        if logo_url:
            self.lbl_logo_img.show()
            self.loader.url_logo = logo_url
            self.loader.start()
        else:
            self.lbl_logo_img.hide()

    def mostrar_logo(self, pixmap):
        if not pixmap.isNull():
            self.lbl_logo_img.setPixmap(pixmap)
            self.lbl_logo_img.show()