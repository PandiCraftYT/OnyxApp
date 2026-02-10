import os
import re

def cargar_canales():
    path = "data.js"
    if not os.path.exists(path): return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read()
            # Buscar contenido entre backticks ` ` o comillas " "
            match = re.search(r'`(.*?)`', contenido, re.DOTALL)
            if not match: match = re.search(r'"(.*?)"', contenido, re.DOTALL)
            
            if match: 
                return parse_m3u(match.group(1))
            return []
    except Exception as e:
        print(f"Error parseando: {e}")
        return []

def parse_m3u(content):
    lines = content.split('\n')
    channels = []
    name = "Sin Nombre"
    logo = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            parts = line.split(',')
            name = parts[-1].strip()
            # Intentar sacar el logo
            logo_match = re.search(r'tvg-logo="([^"]+)"', line)
            logo = logo_match.group(1) if logo_match else ""
        elif line and not line.startswith("#"):
            channels.append({"name": name, "url": line, "logo": logo})
            name = "Sin Nombre"
    return channels