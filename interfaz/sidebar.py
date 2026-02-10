from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QScrollArea, QWidget, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from interfaz.estilos import ESTILO_SIDEBAR

class Sidebar(QFrame):
    canal_seleccionado = pyqtSignal(str, str, str) 

    def __init__(self, canales):
        super().__init__()
        self.setObjectName("Sidebar")
        
        # Empieza oculta (Ancho 0)
        self.setFixedWidth(0) 
        
        self.setStyleSheet(ESTILO_SIDEBAR)
        
        self.lista_completa = canales
        self.botones = []

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15, 25, 15, 20)

        # Logo App
        self.lbl_logo = QLabel("ONYX PLAY")
        self.lbl_logo.setObjectName("Logo")
        self.layout.addWidget(self.lbl_logo)

        # Buscador
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar canal...")
        self.search_bar.textChanged.connect(self.filtrar)
        self.layout.addWidget(self.search_bar)

        self.layout.addSpacing(10)

        # Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ScrollContent")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(2)
        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

        self.cargar_botones(self.lista_completa)

    def cargar_botones(self, lista):
        for btn in self.botones:
            btn.deleteLater()
        self.botones = []

        for ch in lista:
            btn = QPushButton(ch['name']) 
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("url", ch['url'])
            btn.setProperty("name", ch['name'])
            btn.setProperty("logo", ch['logo'])
            
            btn.clicked.connect(lambda _, b=btn: self.on_click(b))
            self.scroll_layout.addWidget(btn)
            self.botones.append(btn)

    def on_click(self, btn):
        for b in self.botones:
            b.setProperty("active", False)
            b.style().unpolish(b)
            b.style().polish(b)

        btn.setProperty("active", True)
        btn.style().unpolish(btn)
        btn.style().polish(btn)

        self.canal_seleccionado.emit(btn.property("url"), btn.property("name"), btn.property("logo"))

    def filtrar(self, texto):
        texto = texto.lower()
        for btn in self.botones:
            nombre = btn.property("name").lower()
            if texto in nombre: btn.show()
            else: btn.hide()