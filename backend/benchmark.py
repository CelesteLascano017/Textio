"""
Módulo de medición de rendimiento de algoritmos.
Responsabilidad única: medir tiempo de ejecución en milisegundos.
"""

import time
from dataclasses import dataclass
from typing import Callable, Any

from preprocessing.normalize import normalize_text
from algorithms.kmp import kmp_search
from algorithms.boyer_moore import boyer_moore_search


@dataclass
class BenchmarkResult:
    """Resultado de una medición de rendimiento."""
    algorithm: str
    text_length: int
    pattern_length: int
    execution_time_ms: float
    match_count: int
    matches: list
    
    def __str__(self) -> str:
        """Representación en string del resultado."""
        return (f"{self.algorithm}: {self.execution_time_ms:.4f}ms "
                f"(texto: {self.text_length} chars, "
                f"patron: {self.pattern_length} chars, "
                f"coincidencias: {self.match_count})")


class AlgorithmBenchmark:
    """Clase para medir rendimiento de algoritmos de búsqueda."""
    
    @staticmethod
    def measure_kmp(text: str, pattern: str, iterations: int = 1) -> BenchmarkResult:
        """
        Mide tiempo de ejecución del algoritmo KMP.
        
        Args:
            text: Texto a buscar
            pattern: Patrón a buscar
            iterations: Número de iteraciones para promedio
        
        Returns:
            BenchmarkResult con mediciones
        """
        total_time = 0
        matches = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            matches = kmp_search(text, pattern)
            end = time.perf_counter()
            total_time += (end - start)
        
        execution_time_ms = (total_time / iterations) * 1000
        
        return BenchmarkResult(
            algorithm="KMP",
            text_length=len(text),
            pattern_length=len(pattern),
            execution_time_ms=execution_time_ms,
            match_count=len(matches),
            matches=matches
        )
    
    @staticmethod
    def measure_boyer_moore(text: str, pattern: str, iterations: int = 1) -> BenchmarkResult:
        """
        Mide tiempo de ejecución del algoritmo Boyer-Moore.
        
        Args:
            text: Texto a buscar
            pattern: Patrón a buscar
            iterations: Número de iteraciones para promedio
        
        Returns:
            BenchmarkResult con mediciones
        """
        total_time = 0
        matches = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            matches = boyer_moore_search(text, pattern)
            end = time.perf_counter()
            total_time += (end - start)
        
        execution_time_ms = (total_time / iterations) * 1000
        
        return BenchmarkResult(
            algorithm="Boyer-Moore",
            text_length=len(text),
            pattern_length=len(pattern),
            execution_time_ms=execution_time_ms,
            match_count=len(matches),
            matches=matches
        )
    
    @staticmethod
    def compare(text: str, pattern: str, iterations: int = 1) -> dict:
        """
        Compara rendimiento de ambos algoritmos.
        
        Args:
            text: Texto a buscar
            pattern: Patrón a buscar
            iterations: Número de iteraciones
        
        Returns:
            Diccionario con resultados y comparativa
        """
        kmp_result = AlgorithmBenchmark.measure_kmp(text, pattern, iterations)
        bm_result = AlgorithmBenchmark.measure_boyer_moore(text, pattern, iterations)
        
        # Calcular diferencia
        diff_ms = abs(kmp_result.execution_time_ms - bm_result.execution_time_ms)
        if kmp_result.execution_time_ms > 0:
            speedup = bm_result.execution_time_ms / kmp_result.execution_time_ms
        else:
            speedup = 1.0
        
        faster = "KMP" if kmp_result.execution_time_ms < bm_result.execution_time_ms else "Boyer-Moore"
        
        return {
            "kmp": {
                "time_ms": round(kmp_result.execution_time_ms, 4),
                "matches": kmp_result.match_count,
            },
            "boyer_moore": {
                "time_ms": round(bm_result.execution_time_ms, 4),
                "matches": bm_result.match_count,
            },
            "comparison": {
                "difference_ms": round(diff_ms, 4),
                "faster_algorithm": faster,
                "speedup_factor": round(speedup, 2),
            },
            "test_case": {
                "text_length": len(text),
                "pattern_length": len(pattern),
                "iterations": iterations,
            }
        }
    
    @staticmethod
    def benchmark_bulk(test_cases: list[tuple[str, str]], 
                      iterations: int = 1) -> dict:
        """
        Ejecuta benchmark en múltiples casos de prueba.
        
        Args:
            test_cases: Lista de tuplas (texto, patrón)
            iterations: Número de iteraciones por caso
        
        Returns:
            Diccionario con resultados aggregados
        """
        results = []
        
        for text, pattern in test_cases:
            comparison = AlgorithmBenchmark.compare(text, pattern, iterations)
            results.append(comparison)
        
        # Calcular promedios
        kmp_times = [r["kmp"]["time_ms"] for r in results]
        bm_times = [r["boyer_moore"]["time_ms"] for r in results]
        
        return {
            "total_cases": len(test_cases),
            "iterations_per_case": iterations,
            "results": results,
            "summary": {
                "kmp_avg_ms": round(sum(kmp_times) / len(kmp_times), 4),
                "boyer_moore_avg_ms": round(sum(bm_times) / len(bm_times), 4),
                "kmp_min_ms": round(min(kmp_times), 4),
                "kmp_max_ms": round(max(kmp_times), 4),
                "boyer_moore_min_ms": round(min(bm_times), 4),
                "boyer_moore_max_ms": round(max(bm_times), 4),
            }
        }
