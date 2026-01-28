"""
Script principal para pruebas del sistema de detección de patrones.
Responsabilidad: ejecutar y validar funcionalidad básica.
"""

from preprocessing.normalize import normalize_text
from algorithms.kmp import kmp_search
from algorithms.boyer_moore import boyer_moore_search, build_bad_char_table
from services.detector import create_detector, ComplaintDetector
from benchmark import AlgorithmBenchmark


def print_section(title: str) -> None:
    """Imprime un encabezado de sección."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def test_normalize_text():
    """Prueba la función normalize_text con el ejemplo específico."""
    print_section("PRUEBA 0: normalize_text()")
    
    test_cases = [
        ("PESIMO Servicio", "pesimo servicio"),
        ("NO ESTA CONFORME", "no esta conforme"),
        ("Defecto en la compra", "defecto en la compra"),
        ("PROBLEMA, PROBLEMA...", "problema problema"),
        ("  Multiples   espacios  ", "multiples espacios"),
    ]
    
    print("Validando funcion normalize_text():\n")
    
    for input_text, expected in test_cases:
        result = normalize_text(input_text)
        passed = result == expected
        status = "[PASS]" if passed else "[FAIL]"
        
        print(f"{status} Input:    '{input_text}'")
        print(f"  Expected: '{expected}'")
        print(f"  Got:      '{result}'")
        print()


def test_kmp_basic():
    """Prueba básica del algoritmo KMP."""
    print_section("PRUEBA 1: KMP - Búsqueda Simple")
    
    text = "el cliente no esta satisfecho con el servicio"
    pattern = "cliente"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    
    matches = kmp_search(text, pattern)
    print(f"Posiciones encontradas: {matches}")
    
    if matches:
        for pos in matches:
            print(f"  -> Encontrado en indice {pos}: '{text[pos:pos+len(pattern)]}'")
    

def test_kmp_with_normalization():
    """Prueba KMP con preprocesamiento."""
    print_section("PRUEBA 2: KMP con Normalizacion")
    
    raw_text = "¡El CLIENTE no está SATISFECHO con el SERVICIO!"
    pattern = "cliente"
    
    print(f"Texto original:     '{raw_text}'")
    normalized_text = normalize_text(raw_text)
    print(f"Texto normalizado:  '{normalized_text}'")
    print(f"Patron buscado:     '{pattern}'")
    
    matches = kmp_search(normalized_text, pattern)
    print(f"Posiciones encontradas: {matches}")
    
    if matches:
        for pos in matches:
            print(f"  -> Encontrado en indice {pos}")


def test_kmp_multiple_matches():
    """Prueba KMP con múltiples coincidencias."""
    print_section("PRUEBA 3: KMP - Multiples Coincidencias")
    
    text = "problema problema problema no se resuelve"
    pattern = "problema"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    
    matches = kmp_search(text, pattern)
    print(f"Total de coincidencias: {len(matches)}")
    print(f"Posiciones: {matches}")


def test_kmp_no_match():
    """Prueba KMP sin coincidencias."""
    print_section("PRUEBA 4: KMP - Sin Coincidencias")
    
    text = "el servicio es excelente"
    pattern = "problema"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    
    matches = kmp_search(text, pattern)
    print(f"Coincidencias encontradas: {matches}")
    print(f"Resultado: {'SIN RECLAMO' if not matches else 'RECLAMO DETECTADO'}")


def test_kmp_with_special_chars():
    """Prueba KMP con caracteres especiales y normalizacion."""
    print_section("PRUEBA 5: KMP - Caracteres Especiales")
    
    raw_text = "¡NO ESTÁ CONFORME! ¿Defecto en la compra?.. Calidad MALA."
    pattern = "defecto"
    
    print(f"Texto original:     '{raw_text}'")
    normalized_text = normalize_text(raw_text)
    print(f"Texto normalizado:  '{normalized_text}'")
    print(f"Patron:             '{pattern}'")
    
    matches = kmp_search(normalized_text, pattern)
    print(f"Coincidencias: {matches}")


def test_lps_array():
    """Prueba la construcción del array LPS."""
    print_section("PRUEBA 6: Array LPS (Prefix Function)")
    
    from algorithms.kmp import build_lps
    
    patterns = ["abab", "aaaa", "abcda", "problema"]
    
    for pattern in patterns:
        lps = build_lps(pattern)
        print(f"Patron: '{pattern}'")
        print(f"LPS:    {lps}")
        print()


def test_boyer_moore_basic():
    """Prueba básica del algoritmo Boyer-Moore."""
    print_section("PRUEBA 7: Boyer-Moore - Búsqueda Simple")
    
    text = "el cliente no esta satisfecho con el servicio"
    pattern = "cliente"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    
    matches = boyer_moore_search(text, pattern)
    print(f"Posiciones encontradas: {matches}")
    
    if matches:
        for pos in matches:
            print(f"  -> Encontrado en indice {pos}: '{text[pos:pos+len(pattern)]}'")


def test_boyer_moore_with_normalization():
    """Prueba Boyer-Moore con preprocesamiento."""
    print_section("PRUEBA 8: Boyer-Moore con Normalizacion")
    
    raw_text = "¡El CLIENTE no está SATISFECHO con el SERVICIO!"
    pattern = "cliente"
    
    print(f"Texto original:     '{raw_text}'")
    normalized_text = normalize_text(raw_text)
    print(f"Texto normalizado:  '{normalized_text}'")
    print(f"Patron buscado:     '{pattern}'")
    
    matches = boyer_moore_search(normalized_text, pattern)
    print(f"Posiciones encontradas: {matches}")
    
    if matches:
        for pos in matches:
            print(f"  -> Encontrado en indice {pos}")


def test_boyer_moore_multiple_matches():
    """Prueba Boyer-Moore con multiples coincidencias."""
    print_section("PRUEBA 9: Boyer-Moore - Multiples Coincidencias")
    
    text = "problema problema problema no se resuelve"
    pattern = "problema"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    
    matches = boyer_moore_search(text, pattern)
    print(f"Total de coincidencias: {len(matches)}")
    print(f"Posiciones: {matches}")


def test_boyer_moore_no_match():
    """Prueba Boyer-Moore sin coincidencias."""
    print_section("PRUEBA 10: Boyer-Moore - Sin Coincidencias")
    
    text = "el servicio es excelente"
    pattern = "defecto"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    
    matches = boyer_moore_search(text, pattern)
    print(f"Coincidencias encontradas: {matches}")
    print(f"Resultado: {'SIN RECLAMO' if not matches else 'RECLAMO DETECTADO'}")


def test_bad_char_table():
    """Prueba la construcción de la tabla de carácter malo."""
    print_section("PRUEBA 11: Tabla de Caracter Malo (Bad Character Rule)")
    
    patterns = ["cliente", "problema", "defecto", "aaaa"]
    
    for pattern in patterns:
        bad_char = build_bad_char_table(pattern)
        print(f"Patron: '{pattern}'")
        print(f"Tabla:  {bad_char}")
        print()


def test_boyer_moore_long_pattern():
    """Prueba Boyer-Moore con patrones largos."""
    print_section("PRUEBA 12: Boyer-Moore - Patron Largo")
    
    text = "no estoy conforme con la calidad del producto entregado"
    pattern = "conforme"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    
    matches_bm = boyer_moore_search(text, pattern)
    matches_kmp = kmp_search(text, pattern)
    
    print(f"Boyer-Moore: {matches_bm}")
    print(f"KMP:         {matches_kmp}")
    print(f"Coinciden:   {'OK' if matches_bm == matches_kmp else 'FAIL'}")


def test_comparison_kmp_vs_boyer_moore():
    """Compara resultados entre KMP y Boyer-Moore."""
    print_section("PRUEBA 13: Comparacion KMP vs Boyer-Moore")
    
    test_cases = [
        ("el cliente esta feliz", "cliente"),
        ("problema problema problema", "problema"),
        ("no hay reclamos aqui", "reclamo"),
        ("defecto en el producto", "defecto"),
        ("aaaaaaaaaa", "aaa"),
    ]
    
    for text, pattern in test_cases:
        kmp_results = kmp_search(text, pattern)
        bm_results = boyer_moore_search(text, pattern)
        
        match = "OK" if kmp_results == bm_results else "FAIL"
        print(f"Texto: '{text}'")
        print(f"Patron: '{pattern}'")
        print(f"  KMP:          {kmp_results}")
        print(f"  Boyer-Moore:  {bm_results}")
        print(f"  Coinciden:    {match}\n")


def test_detector_basic():
    """Prueba básica del detector de reclamos."""
    print_section("PRUEBA 14: Detector Basico")
    
    detector = create_detector()
    
    test_messages = [
        "El producto tiene un defecto grave",
        "No funciona correctamente",
        "Estoy muy satisfecho con la compra",
        "Pedido incompleto y perdido",
    ]
    
    for msg in test_messages:
        print(f"Mensaje: '{msg}'")
        results = detector.detect(msg, algorithm="kmp")
        
        if results:
            print(f"  Patrones encontrados: {len(results)}")
            for result in results:
                print(f"    - {result.pattern} ({result.alert_level}) -> {result.alert_message}")
        else:
            print(f"  Sin reclamos detectados")
        print()


def test_detector_with_both_algorithms():
    """Prueba detector con ambos algoritmos."""
    print_section("PRUEBA 15: Detector - KMP vs Boyer-Moore")
    
    detector = create_detector()
    
    text = "Producto defectuoso, no funciona y esta roto"
    
    print(f"Analizando: '{text}'\n")
    
    kmp_results = detector.detect(text, algorithm="kmp")
    bm_results = detector.detect(text, algorithm="boyer_moore")
    
    print(f"Resultados KMP:         {len(kmp_results)} patrones")
    print(f"Resultados Boyer-Moore: {len(bm_results)} patrones")
    print(f"Coinciden:              {'OK' if len(kmp_results) == len(bm_results) else 'FAIL'}\n")
    
    if kmp_results:
        print("Patrones detectados:")
        for result in kmp_results:
            print(f"  - {result.pattern}: {result.alert_message}")


def test_detector_comprehensive():
    """Prueba completa del detector con análisis detallado."""
    print_section("PRUEBA 16: Detector Exhaustivo")
    
    detector = create_detector()
    
    messages = [
        "Producto defectuoso y roto, muy malo",
        "Entrega perdida hace una semana",
        "Servicio excelente, todo bien",
    ]
    
    for msg in messages:
        print(f"Mensaje: '{msg}'")
        analysis = detector.detect_all(msg)
        
        print(f"  Normalizado: '{analysis['normalized_text']}'")
        print(f"  Patrones encontrados: {analysis['patterns_found']}/{analysis['total_patterns_checked']}")
        print(f"  Alertas por nivel: HIGH={analysis['alert_levels']['high']}, " +
              f"MEDIUM={analysis['alert_levels']['medium']}, " +
              f"LOW={analysis['alert_levels']['low']}")
        
        if analysis['detections']:
            for detection in analysis['detections']:
                print(f"    [{detection['alert_level'].upper()}] {detection['pattern']}")
        else:
            print(f"    Sin reclamos")
        print()


def test_detector_single_pattern():
    """Prueba búsqueda de patrón único."""
    print_section("PRUEBA 17: Detector - Patron Unico")
    
    detector = create_detector()
    
    text = "El servicio es pesimo, muy malo"
    pattern = "pesimo"
    
    print(f"Texto:     '{text}'")
    print(f"Patron:    '{pattern}'")
    print()
    
    result = detector.detect_single_pattern(text, pattern, algorithm="kmp")
    result_dict = result.to_dict()
    
    print(f"Patrón encontrado:  {result_dict['found']}")
    print(f"Coincidencias:      {result_dict['match_count']}")
    print(f"Posiciones:         {result_dict['positions']}")
    print(f"Mensaje de alerta:  {result_dict['alert_message']}")


def test_benchmark_algorithms():
    """Prueba benchmark de algoritmos."""
    print_section("PRUEBA 18: Benchmark - KMP vs Boyer-Moore")
    
    test_cases = [
        ("cliente", "cliente"),
        ("el cliente no esta satisfecho", "cliente"),
        ("problema problema problema", "problema"),
        ("defecto en producto", "defecto"),
    ]
    
    print("Mediciones de rendimiento (1000 iteraciones por caso):\n")
    
    for i, (text, pattern) in enumerate(test_cases, 1):
        comparison = AlgorithmBenchmark.compare(text, pattern, iterations=1000)
        
        print(f"[Caso {i}] Texto: '{text[:30]}...' Patron: '{pattern}'")
        print(f"  KMP:           {comparison['kmp']['time_ms']:.4f} ms")
        print(f"  Boyer-Moore:   {comparison['boyer_moore']['time_ms']:.4f} ms")
        print(f"  Mas rapido:    {comparison['comparison']['faster_algorithm']}")
        print()


def test_benchmark_bulk():
    """Prueba benchmark agregado."""
    print_section("PRUEBA 19: Benchmark Bulk - Resultado Agregado")
    
    test_cases = [
        ("cliente", "cliente"),
        ("el cliente no esta satisfecho", "cliente"),
        ("problema problema problema", "problema"),
        ("defecto en producto", "defecto"),
        ("a" * 50, "a" * 5),
    ]
    
    bulk_result = AlgorithmBenchmark.benchmark_bulk(test_cases, iterations=300)
    summary = bulk_result['summary']
    
    print(f"Total de casos:       {bulk_result['total_cases']}")
    print(f"Iteraciones por caso: {bulk_result['iterations_per_case']}\n")
    
    print("Promedios:")
    print(f"  KMP:           {summary['kmp_avg_ms']:.4f} ms")
    print(f"  Boyer-Moore:   {summary['boyer_moore_avg_ms']:.4f} ms\n")
    
    print("Rango KMP:")
    print(f"  Min:  {summary['kmp_min_ms']:.4f} ms")
    print(f"  Max:  {summary['kmp_max_ms']:.4f} ms\n")
    
    print("Rango Boyer-Moore:")
    print(f"  Min:  {summary['boyer_moore_min_ms']:.4f} ms")
    print(f"  Max:  {summary['boyer_moore_max_ms']:.4f} ms")


def test_detector_timing():
    """Prueba timing del detector."""
    print_section("PRUEBA 20: Timing del Detector")
    
    detector = create_detector()
    
    messages = [
        "Producto con defecto",
        "No funciona correctamente",
        "Muy satisfecho con la compra",
    ]
    
    for msg in messages:
        print(f"Mensaje: {msg}")
        
        analysis_kmp = detector.detect_all(msg, algorithm="kmp")
        analysis_bm = detector.detect_all(msg, algorithm="boyer_moore")
        
        print(f"  KMP:           {analysis_kmp['performance']['total_execution_time_ms']:.4f} ms")
        print(f"  Boyer-Moore:   {analysis_bm['performance']['total_execution_time_ms']:.4f} ms")
        print(f"  Patrones:      {analysis_kmp['patterns_found']}")
        print()




def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "=" * 60)
    print("  SISTEMA DE DETECCION DE RECLAMOS")
    print("  Pruebas: normalize_text, KMP, Boyer-Moore, Detector")
    print("=" * 60)
    
    try:
        # Prueba de normalización
        test_normalize_text()
        
        # Pruebas KMP
        test_kmp_basic()
        test_kmp_with_normalization()
        test_kmp_multiple_matches()
        test_kmp_no_match()
        test_kmp_with_special_chars()
        test_lps_array()
        
        # Pruebas Boyer-Moore
        test_boyer_moore_basic()
        test_boyer_moore_with_normalization()
        test_boyer_moore_multiple_matches()
        test_boyer_moore_no_match()
        test_bad_char_table()
        test_boyer_moore_long_pattern()
        test_comparison_kmp_vs_boyer_moore()
        
        # Pruebas Detector
        test_detector_basic()
        test_detector_with_both_algorithms()
        test_detector_comprehensive()
        test_detector_single_pattern()
        
        # Pruebas Benchmark
        test_benchmark_algorithms()
        test_benchmark_bulk()
        test_detector_timing()
        
        print_section("TODAS LAS PRUEBAS COMPLETADAS")
        
    except Exception as e:
        print(f"\nError durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
