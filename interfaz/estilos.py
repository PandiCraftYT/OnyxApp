# ---------------------------------------------------------
# HOJAS DE ESTILO CSS (PyQt6) - ONYX PLAY PREMIUM FINAL
# ---------------------------------------------------------

# 1. ESTILO DE LA VENTANA PRINCIPAL
ESTILO_MAIN = """
QMainWindow {
    background-color: #050505; /* Negro profundo */
}
"""

# 2. ESTILO DE LA BARRA LATERAL (SIDEBAR)
ESTILO_SIDEBAR = """
QFrame#Sidebar {
    background-color: #0a0a0a;
    border-right: 1px solid #1a1a1a;
}

/* Logo Principal */
QLabel#Logo {
    color: #E50914;
    font-size: 26px;
    font-weight: 800; /* Extra Bold */
    font-family: 'Segoe UI', sans-serif;
    padding-left: 5px;
    background-color: transparent;
    margin-bottom: 10px;
}

/* Barra de Búsqueda */
QLineEdit {
    background-color: #141414;
    color: #e0e0e0;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 13px;
}
QLineEdit:focus {
    border: 1px solid #E50914; /* Borde rojo al escribir */
    background-color: #1a1a1a;
}

/* Scroll Invisible */
QScrollArea { border: none; background: transparent; }
QWidget#ScrollContent { background: transparent; }

/* --- BOTONES DE CANALES --- */
QPushButton {
    text-align: left;
    padding: 12px 15px;
    background-color: transparent;
    color: #999;
    border: none;
    border-radius: 6px;
    font-family: 'Segoe UI';
    font-size: 14px;
    margin: 2px 5px;
}

QPushButton:hover {
    background-color: #1a1a1a;
    color: white;
}

/* ESTADO ACTIVO (Seleccionado) */
QPushButton[active="true"] {
    /* Degradado rojo a transparente */
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 rgba(229, 9, 20, 0.15), 
                                      stop:1 rgba(0, 0, 0, 0));
    color: white;
    border-left: 4px solid #E50914;
    font-weight: 700;
    padding-left: 11px;
}
"""

# 3. ESTILO DE LOS CONTROLES (Barra Flotante)
ESTILO_CONTROLES = """
QFrame#Controles {
    background-color: #121212; 
    border-radius: 16px; 
    border: none; /* Sin bordes para que se vea limpia */
}

QLabel {
    color: white;
    font-family: 'Segoe UI';
    background-color: transparent;
}

/* Jerarquía de Texto */
QLabel#TituloInfo { font-weight: 700; font-size: 14px; color: #fff; }
QLabel#SubInfo { font-size: 11px; color: #888; }
QLabel#LiveTag { color: #E50914; font-weight: bold; font-size: 11px; }

/* NOTA: El botón de Play (#BtnPlay) ya no necesita estilo aquí 
   porque la clase BotonPlay en Python lo dibuja manualmente. */

/* --- BOTONES DE HERRAMIENTAS (Volumen, Pantalla Completa) --- */
QPushButton#BtnIcon {
    background-color: transparent;
    color: #ccc;
    font-size: 16px;
    border: none;
    padding: 5px;
    border-radius: 5px;
}
QPushButton#BtnIcon:hover {
    color: white;
    background-color: #222;
}

/* --- SLIDER DE VOLUMEN (DISEÑO FINO) --- */
QSlider::groove:horizontal {
    border: none;
    height: 4px;
    background: #333;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #E50914; /* Relleno Rojo */
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: white;
    border: none;
    width: 12px;
    height: 12px;
    margin: -4px 0;
    border-radius: 6px; /* Bolita blanca */
}
QSlider::handle:horizontal:hover {
    transform: scale(1.2); /* Crece un poco al tocarlo */
    background: #fff;
    margin: -5px 0;
    width: 14px;
    height: 14px;
    border-radius: 7px;
}
"""