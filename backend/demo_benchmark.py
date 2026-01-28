"""
Script de demostración de mediciones de rendimiento.
"""

from benchmark import AlgorithmBenchmark
from services.detector import create_detector
from preprocessing.normalize import normalize_text


def demo_benchmark():
    """Demuestra las mediciones de rendimiento de los algoritmos."""
    
    print("\n" + "=" * 70)
    print("  BENCHMARK: MEDICION DE TIEMPO DE EJECUCION (ms)")
    print("=" * 70 + "\n")
    
    # Casos de prueba variados
    test_cases = [
        ("cliente", "cliente"),
        ("el cliente no esta satisfecho", "cliente"),
        ("problema problema problema", "problema"),
        ("el servicio es defectuoso y no funciona correctamente", "defecto"),
        ("a" * 100, "a" * 10),  # Texto largo
        ("defecto defecto defecto defecto", "defecto"),
    ]
    
    print("Comparativa KMP vs Boyer-Moore:\n")
    
    for i, (text, pattern) in enumerate(test_cases, 1):
        print(f"[Caso {i}]")
        print(f"  Texto:   '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"  Patron:  '{pattern}'")
        
        comparison = AlgorithmBenchmark.compare(text, pattern, iterations=1000)
        
        print(f"  KMP:           {comparison['kmp']['time_ms']:.4f} ms")
        print(f"  Boyer-Moore:   {comparison['boyer_moore']['time_ms']:.4f} ms")
        print(f"  Diferencia:    {comparison['comparison']['difference_ms']:.4f} ms")
        print(f"  Mas rapido:    {comparison['comparison']['faster_algorithm']}")
        print()
    
    print("\n" + "=" * 70)
    print("  BENCHMARK BULK: RESULTADO AGREGADO")
    print("=" * 70 + "\n")
    
    bulk_result = AlgorithmBenchmark.benchmark_bulk(test_cases, iterations=500)
    
    summary = bulk_result['summary']
    print(f"Total de casos:        {bulk_result['total_cases']}")
    print(f"Iteraciones por caso:  {bulk_result['iterations_per_case']}")
    print()
    print("Promedio de tiempos:")
    print(f"  KMP:           {summary['kmp_avg_ms']:.4f} ms")
    print(f"  Boyer-Moore:   {summary['boyer_moore_avg_ms']:.4f} ms")
    print()
    print("Rango KMP:")
    print(f"  Min:  {summary['kmp_min_ms']:.4f} ms")
    print(f"  Max:  {summary['kmp_max_ms']:.4f} ms")
    print()
    print("Rango Boyer-Moore:")
    print(f"  Min:  {summary['boyer_moore_min_ms']:.4f} ms")
    print(f"  Max:  {summary['boyer_moore_max_ms']:.4f} ms")


def demo_detector_with_timing():
    """Demuestra el detector con medición de tiempo."""
    
    print("\n" + "=" * 70)
    print("  DETECTOR: MEDICION DE TIEMPO DE EJECUCION")
    print("=" * 70 + "\n")
    
    detector = create_detector()
    
    test_messages = [
        "Producto con defecto grave",
        "No funciona correctamente, es un problema",
        "Muy satisfecho con la compra",
        "Pedido incompleto, dano en transito, calidad pésima",
    ]
    
    for msg in test_messages:
        print(f"Mensaje: {msg}\n")
        
        # Medición con KMP
        analysis_kmp = detector.detect_all(msg, algorithm="kmp")
        
        # Medición con Boyer-Moore
        analysis_bm = detector.detect_all(msg, algorithm="boyer_moore")
        
        print(f"  KMP:           {analysis_kmp['performance']['total_execution_time_ms']:.4f} ms")
        print(f"  Boyer-Moore:   {analysis_bm['performance']['total_execution_time_ms']:.4f} ms")
        print(f"  Patrones:      {analysis_kmp['patterns_found']} encontrados")
        
        if analysis_kmp['patterns_found'] > 0:
            for detection in analysis_kmp['detections']:
                print(f"    - {detection['pattern']} ({detection['alert_level']})")
        print()


def demo_benchmark_single_algorithm():
    """Demuestra medición individual de un algoritmo."""
    
    print("\n" + "=" * 70)
    print("  MEDICION INDIVIDUAL: KMP y Boyer-Moore")
    print("=" * 70 + "\n")
    
    text = "el cliente no esta satisfecho con el servicio"
    pattern = "cliente"
    
    print(f"Texto:   {text}")
    print(f"Patron:  {pattern}\n")
    
    # Múltiples iteraciones
    for iterations in [1, 100, 1000]:
        print(f"Iteraciones: {iterations}")
        
        kmp_result = AlgorithmBenchmark.measure_kmp(text, pattern, iterations=iterations)
        bm_result = AlgorithmBenchmark.measure_boyer_moore(text, pattern, iterations=iterations)
        
        print(f"  KMP:           {kmp_result.execution_time_ms:.6f} ms (por iteracion)")
        print(f"  Boyer-Moore:   {bm_result.execution_time_ms:.6f} ms (por iteracion)")
        print()


if __name__ == "__main__":
    demo_benchmark()
    demo_detector_with_timing()
    demo_benchmark_single_algorithm()
