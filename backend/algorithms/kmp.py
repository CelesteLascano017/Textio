"""
Algoritmo Knuth–Morris–Pratt (KMP) para búsqueda de patrones.
Responsabilidad única: búsqueda eficiente de patrones en texto.
"""


def build_lps(pattern: str) -> list[int]:
    """
    Construye el array LPS (Longest Proper Prefix which is also Suffix).
    
    Args:
        pattern: Patrón a analizar
    
    Returns:
        Array LPS de longitud len(pattern)
    
    Complejidad: O(m) donde m = len(pattern)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps


def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Busca todas las ocurrencias de un patrón en un texto usando KMP.
    
    Args:
        text: Texto en el que buscar
        pattern: Patrón a buscar
    
    Returns:
        Lista de posiciones (índices) donde se encuentra el patrón
    
    Complejidad: O(n + m) donde n = len(text), m = len(pattern)
    """
    if not pattern or not text:
        return []
    
    n = len(text)
    m = len(pattern)
    
    if m > n:
        return []
    
    lps = build_lps(pattern)
    matches = []
    i = 0  # índice en text
    j = 0  # índice en pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            # Encontramos una coincidencia
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return matches
