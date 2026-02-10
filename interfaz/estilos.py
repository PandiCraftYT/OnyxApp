# Hojas de Estilo CSS para PyQt6

ESTILO_MAIN = """
QMainWindow {
    background-color: #000000;
}
"""

ESTILO_SIDEBAR = """
QFrame#Sidebar {
    background-color: #090909;
    border-right: 1px solid #1f1f1f;
}
QLabel#Logo {
    color: #E50914;
    font-size: 24px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
    padding-left: 10px;
    background-color: transparent;
}
QLineEdit {
    background-color: #1a1a1a;
    color: white;
    border: 1px solid #333;
    border-radius: 18px;
    padding: 8px 15px;
    font-size: 13px;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QWidget#ScrollContent {
    background-color: transparent;
}
/* Botones de Canales */
QPushButton {
    text-align: left;
    padding: 12px 15px;
    background-color: transparent;
    color: #b3b3b3;
    border: none;
    border-radius: 6px;
    font-family: 'Segoe UI';
    font-size: 14px;
}
QPushButton:hover {
    background-color: #222;
    color: white;
}
/* Botón Activo (Seleccionado) */
QPushButton[active="true"] {
    background-color: #2a1010;
    color: white;
    border-left: 3px solid #E50914;
    font-weight: bold;
}
"""

# 👇 AQUÍ ESTÁ EL ARREGLO VISUAL PARA LA BARRA DE ABAJO
ESTILO_CONTROLES = """
QFrame#Controles {
    background-color: #161616; 
    border-radius: 35px; /* Más redondeado */
    border: 1px solid #333;
}
QLabel {
    color: white;
    font-family: 'Segoe UI';
    background-color: transparent; /* IMPORTANTE: Quita el fondo negro del texto */
}
/* Botón Play Redondo */
QPushButton#BtnPlay {
    background-color: white;
    color: black;
    border-radius: 22px; /* Redondo perfecto */
    font-size: 20px;
    padding-bottom: 3px; /* Ajuste visual del icono */
}
QPushButton#BtnPlay:hover {
    background-color: #E50914; /* Rojo al pasar el mouse */
    color: white;
}
/* Otros botones */
QPushButton#BtnIcon {
    background-color: transparent;
    color: #ccc;
    font-size: 16px;
    border: none;
}
QPushButton#BtnIcon:hover {
    color: white;
}
/* Slider de Volumen */
QSlider::groove:horizontal {
    border: 1px solid #333;
    height: 4px;
    background: #333;
    margin: 2px 0;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: white;
    border: 1px solid white;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::sub-page:horizontal {
    background: #E50914;
    border-radius: 2px;
}
"""