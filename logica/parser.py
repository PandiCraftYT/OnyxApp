import os
import sys

def obtener_ruta_recurso(relativa):
    """ 
    Obtiene la ruta absoluta para recursos, compatible con PyInstaller.
    """
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, relativa)

def cargar_canales():
    # Usamos el nombre del archivo que tienes en tu carpeta
    nombre_archivo = "data.js" # O "data.java" según corresponda exactamente
    ruta = obtener_ruta_recurso(nombre_archivo)
    
    canales = []
    
    if not os.path.exists(ruta):
        print(f"Error: No se encontró el archivo de datos en: {ruta}")
        return []

    try:
        # Abrimos el archivo con 'latin-1' o 'utf-8' para evitar errores de símbolos
        with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.readlines()
            
        canal_actual = {}
        for linea in contenido:
            linea = linea.strip()
            
            # Buscamos la información del canal dentro del archivo de texto
            if "#EXTINF:" in linea:
                # Extraer nombre (lo que está después de la última coma)
                if "," in linea:
                    canal_actual['name'] = linea.split(",")[-1].strip()
                
                # Extraer logo (tvg-logo="...")
                if 'tvg-logo="' in linea:
                    inicio = linea.find('tvg-logo="') + 10
                    fin = linea.find('"', inicio)
                    canal_actual['logo'] = linea[inicio:fin]
                else:
                    canal_actual['logo'] = ""
                    
            # Buscamos la URL (líneas que contienen http)
            elif "http" in linea and ('name' in canal_actual):
                # Limpiamos la línea por si hay comillas de JavaScript o Java
                url = linea.replace('"', '').replace("'", "").replace(";", "").replace(",", "").strip()
                # Si la línea tiene espacios, tomamos la primera palabra que sea la URL
                for palabra in url.split():
                    if palabra.startswith("http"):
                        canal_actual['url'] = palabra
                        break
                
                if 'url' in canal_actual:
                    canales.append(canal_actual)
                    canal_actual = {} # Reiniciar para el siguiente
                
        return canales

    except Exception as e:
        print(f"Error crítico al leer el archivo de canales: {e}")
        return []