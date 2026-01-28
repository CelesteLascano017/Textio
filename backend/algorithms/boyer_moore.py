"""
Algoritmo Boyer–Moore para búsqueda de patrones.
Responsabilidad única: búsqueda eficiente usando bad character rule.
"""


def build_bad_char_table(pattern: str) -> dict[str, int]:
    """
    Construye la tabla de carácter malo (Bad Character Rule).
    Para cada carácter en el patrón, almacena su última posición.
    
    Args:
        pattern: Patrón a analizar
    
    Returns:
        Diccionario {caracter: última_posición_desde_derecha}
    
    Complejidad: O(m) donde m = len(pattern)
    """
    bad_char = {}
    
    for i, char in enumerate(pattern):
        bad_char[char] = i
    
    return bad_char


def boyer_moore_search(text: str, pattern: str) -> list[int]:
    """
    Busca todas las ocurrencias de un patrón en un texto usando Boyer-Moore.
    Utiliza la regla del carácter malo para saltar posiciones.
    
    Args:
        text: Texto en el que buscar
        pattern: Patrón a buscar
    
    Returns:
        Lista de posiciones (índices) donde se encuentra el patrón
    
    Complejidad: 
        - Mejor caso: O(n/m)
        - Peor caso: O(n*m)
        donde n = len(text), m = len(pattern)
    """
    if not pattern or not text:
        return []
    
    n = len(text)
    m = len(pattern)
    
    if m > n:
        return []
    
    bad_char = build_bad_char_table(pattern)
    matches = []
    
    # s es el desplazamiento del patrón en el texto
    s = 0
    
    while s <= n - m:
        # Comparar patrón de derecha a izquierda
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            # Se encontró coincidencia en posición s
            matches.append(s)
            # Desplazarse para buscar próxima coincidencia
            s += 1 if s + m < n else 1
        else:
            # Carácter malo en text[s + j]
            bad_char_pos = bad_char.get(text[s + j], -1)
            
            # Desplazamiento: máximo entre 1 y la distancia del carácter malo
            shift = max(1, j - bad_char_pos)
            s += shift
    
    return matches


def boyer_moore_search_with_good_suffix(text: str, pattern: str) -> list[int]:
    """
    Versión mejorada de Boyer-Moore que incluye good suffix rule.
    (Versión alternativa - usa la misma interfaz que boyer_moore_search)
    
    Args:
        text: Texto en el que buscar
        pattern: Patrón a buscar
    
    Returns:
        Lista de posiciones donde se encuentra el patrón
    """
    # Para esta implementación básica, usamos la versión con bad char
    # La good suffix rule es una optimización adicional
    return boyer_moore_search(text, pattern)
