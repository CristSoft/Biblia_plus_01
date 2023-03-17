import re

def separar_cadena(cadena):
    # Definir patrón de expresión regular para buscar libro, capítulo y versículo
    patron = r'(\w+)\s+(\d+):(\d+)'
    
    # Buscar coincidencias en la cadena de entrada
    coincidencias = re.search(patron, cadena)
    
    # Extraer valores de libro, capítulo y versículo
    libro = coincidencias.group(1)
    cap = coincidencias.group(2)
    vers = coincidencias.group(3)
    
    # Devolver los valores como una tupla
    return (libro, cap, vers)

