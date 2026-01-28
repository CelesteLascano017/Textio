"""
Servicio de detección de patrones en textos.
Responsabilidad única: detectar patrones de reclamos usando algoritmos de búsqueda.
"""

import csv
import os
import time
from dataclasses import dataclass
from typing import Optional

from preprocessing.normalize import normalize_text
from algorithms.kmp import kmp_search
from algorithms.boyer_moore import boyer_moore_search


@dataclass
class DetectionResult:
    """Resultado de la detección de un patrón."""
    pattern: str
    category: str
    alert_level: str
    alert_message: str
    positions: list[int]
    
    def to_dict(self) -> dict:
        """Convierte resultado a diccionario."""
        return {
            "pattern": self.pattern,
            "category": self.category,
            "alert_level": self.alert_level,
            "alert_message": self.alert_message,
            "positions": self.positions,
            "found": len(self.positions) > 0,
            "match_count": len(self.positions)
        }


class ComplaintDetector:
    """Detector de reclamos basado en búsqueda de patrones."""
    
    def __init__(self, patterns_file: str):
        """
        Inicializa el detector cargando patrones desde archivo.
        
        Args:
            patterns_file: Ruta al archivo CSV con patrones
        """
        self.patterns = []
        self.load_patterns(patterns_file)
    
    def load_patterns(self, patterns_file: str) -> None:
        """
        Carga patrones desde archivo CSV.
        
        Formato esperado:
        pattern,category,alert_level,alert_message
        
        Args:
            patterns_file: Ruta al archivo CSV
        """
        if not os.path.exists(patterns_file):
            raise FileNotFoundError(f"Archivo de patrones no encontrado: {patterns_file}")
        
        with open(patterns_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.patterns.append({
                    'pattern': row['pattern'].strip(),
                    'category': row['category'].strip(),
                    'alert_level': row['alert_level'].strip(),
                    'alert_message': row['alert_message'].strip(),
                })
    
    def detect(self, text: str, algorithm: str = "kmp") -> list[DetectionResult]:
        """
        Detecta patrones en el texto.
        
        Args:
            text: Texto a analizar
            algorithm: "kmp" o "boyer_moore"
        
        Returns:
            Lista de resultados de detección
        """
        if algorithm not in ["kmp", "boyer_moore"]:
            raise ValueError("Algoritmo debe ser 'kmp' o 'boyer_moore'")
        
        # Normalizar texto
        normalized_text = normalize_text(text)
        
        # Seleccionar algoritmo de búsqueda
        search_fn = kmp_search if algorithm == "kmp" else boyer_moore_search
        
        results = []
        
        for pattern_data in self.patterns:
            pattern = normalize_text(pattern_data['pattern'])
            
            # Medir tiempo de búsqueda
            start_time = time.perf_counter()
            positions = search_fn(normalized_text, pattern)
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            if positions:
                result = DetectionResult(
                    pattern=pattern_data['pattern'],
                    category=pattern_data['category'],
                    alert_level=pattern_data['alert_level'],
                    alert_message=pattern_data['alert_message'],
                    positions=positions
                )
                results.append(result)
        
        return results
    
    def detect_single_pattern(self, text: str, pattern: str, 
                             algorithm: str = "kmp") -> DetectionResult:
        """
        Detecta un patrón específico en el texto.
        
        Args:
            text: Texto a analizar
            pattern: Patrón a buscar
            algorithm: "kmp" o "boyer_moore"
        
        Returns:
            Resultado de detección
        """
        normalized_text = normalize_text(text)
        normalized_pattern = normalize_text(pattern)
        
        search_fn = kmp_search if algorithm == "kmp" else boyer_moore_search
        positions = search_fn(normalized_text, normalized_pattern)
        
        return DetectionResult(
            pattern=pattern,
            category="custom",
            alert_level="info",
            alert_message=f"Patron '{pattern}' encontrado",
            positions=positions
        )
    
    def detect_all(self, text: str, algorithm: str = "kmp") -> dict:
        """
        Detección completa retornando estructura detallada.
        
        Args:
            text: Texto a analizar
            algorithm: "kmp" o "boyer_moore"
        
        Returns:
            Diccionario con resultados y resumen
        """
        start_total = time.perf_counter()
        results = self.detect(text, algorithm)
        end_total = time.perf_counter()
        total_execution_time_ms = (end_total - start_total) * 1000
        
        return {
            "original_text": text,
            "normalized_text": normalize_text(text),
            "algorithm": algorithm,
            "detections": [r.to_dict() for r in results],
            "total_patterns_checked": len(self.patterns),
            "patterns_found": len(results),
            "has_complaints": len(results) > 0,
            "alert_levels": {
                "high": len([r for r in results if r.alert_level == "high"]),
                "medium": len([r for r in results if r.alert_level == "medium"]),
                "low": len([r for r in results if r.alert_level == "low"]),
            },
            "performance": {
                "total_execution_time_ms": round(total_execution_time_ms, 4),
                "algorithm_used": algorithm
            }
        }


def create_detector(patterns_path: Optional[str] = None) -> ComplaintDetector:
    """
    Factory para crear detector con ruta por defecto.
    
    Args:
        patterns_path: Ruta al archivo de patrones (usa default si es None)
    
    Returns:
        Instancia de ComplaintDetector
    """
    if patterns_path is None:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        patterns_path = os.path.join(base_path, "data", "patterns.csv")
    
    return ComplaintDetector(patterns_path)
