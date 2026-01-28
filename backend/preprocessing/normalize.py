"""
Módulo de normalización de texto.
Responsabilidad única: preparar texto para análisis de patrones.
"""

import unicodedata
import string
import re


def remove_accents(text: str) -> str:
    """
    Elimina tildes/acentos del texto.
    
    Args:
        text: Texto con posibles acentos
    
    Returns:
        Texto sin acentos
    """
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')


def remove_punctuation(text: str) -> str:
    """
    Elimina signos de puntuación.
    
    Args:
        text: Texto con posible puntuación
    
    Returns:
        Texto sin puntuación
    """
    return text.translate(str.maketrans('', '', string.punctuation))


def normalize_text(text: str) -> str:
    """
    Normaliza texto: minúsculas, elimina tildes y puntuación.
    
    Transforma: "¡PÉSIMO Servicio!" → "pesimo servicio"
    
    Args:
        text: Texto bruto
    
    Returns:
        Texto normalizado para análisis de patrones
    
    Proceso:
        1. Convierte a minúsculas
        2. Elimina acentos/tildes
        3. Elimina signos de puntuación
        4. Normaliza espacios
    """
    text = text.lower()
    text = remove_accents(text)
    text = remove_punctuation(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize(text: str) -> str:
    """Alias para normalize_text (compatibilidad)."""
    return normalize_text(text)


def tokenize(text: str) -> list[str]:
    """
    Divide texto normalizado en palabras.
    
    Args:
        text: Texto normalizado
    
    Returns:
        Lista de palabras
    """
    return text.split()
