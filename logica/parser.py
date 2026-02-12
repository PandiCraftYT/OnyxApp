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
    # Buscamos el archivo de datos en la raíz o dentro del .exe
    nombre_archivo = "data.js" 
    ruta = obtener_ruta_recurso(nombre_archivo)
    
    canales = []
    
    if not os.path.exists(ruta):
        print(f"Error: No se encontró el archivo de datos en: {ruta}")
        return []

    try:
        # Usamos errors='ignore' para que caracteres extraños no traben la carga
        with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.readlines()
            
        canal_actual = {}
        for linea in contenido:
            linea = linea.strip()
            
            if "#EXTINF:" in linea:
                # Extraer nombre
                if "," in linea:
                    canal_actual['name'] = linea.split(",")[-1].strip()
                
                # Extraer logo
                if 'tvg-logo="' in linea:
                    inicio = linea.find('tvg-logo="') + 10
                    fin = linea.find('"', inicio)
                    canal_actual['logo'] = linea[inicio:fin]
                else:
                    canal_actual['logo'] = ""
                    
            elif "http" in linea and ('name' in canal_actual):
                # Limpiamos basura de JS/Java para obtener la URL pura
                url_sucia = linea.replace('"', '').replace("'", "").replace(";", "").replace(",", "").strip()
                
                for palabra in url_sucia.split():
                    if palabra.startswith("http"):
                        canal_actual['url'] = palabra
                        break
                
                if 'url' in canal_actual:
                    canales.append(canal_actual)
                    canal_actual = {} 
                
        return canales

    except Exception as e:
        print(f"Error crítico al leer el archivo de canales: {e}")
        return []