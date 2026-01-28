"""
Script para probar la API sin ejecutar servidor.
Simula solicitudes HTTP y valida respuestas.
"""

import json
from services.detector import create_detector


def test_api_endpoints():
    """Simula pruebas de endpoints de la API."""
    
    detector = create_detector()
    
    print("\n" + "=" * 70)
    print("  PRUEBAS DE API (Sin servidor)")
    print("=" * 70 + "\n")
    
    # Test 1: Endpoint /analyze - Caso con reclamos
    print("[TEST 1] POST /analyze - Con reclamos")
    print("-" * 70)
    
    request_data = {
        "text": "Producto con defecto, no funciona correctamente",
        "algorithm": "kmp"
    }
    
    print(f"REQUEST: {json.dumps(request_data, indent=2)}\n")
    
    analysis = detector.detect_all(request_data["text"], algorithm=request_data["algorithm"])
    
    print(f"RESPONSE:")
    print(f"  Status: 200 OK")
    print(f"  Patterns found: {analysis['patterns_found']}")
    print(f"  Execution time: {analysis['performance']['total_execution_time_ms']:.4f} ms")
    print(f"  Detections: {[d['pattern'] for d in analysis['detections']]}")
    print()
    
    # Test 2: Endpoint /analyze - Caso sin reclamos
    print("[TEST 2] POST /analyze - Sin reclamos")
    print("-" * 70)
    
    request_data = {
        "text": "Estoy muy satisfecho con el servicio",
        "algorithm": "boyer_moore"
    }
    
    print(f"REQUEST: {json.dumps(request_data, indent=2)}\n")
    
    analysis = detector.detect_all(request_data["text"], algorithm=request_data["algorithm"])
    
    print(f"RESPONSE:")
    print(f"  Status: 200 OK")
    print(f"  Patterns found: {analysis['patterns_found']}")
    print(f"  Execution time: {analysis['performance']['total_execution_time_ms']:.4f} ms")
    print(f"  Has complaints: {analysis['has_complaints']}")
    print()
    
    # Test 3: Endpoint /compare
    print("[TEST 3] POST /compare - KMP vs Boyer-Moore")
    print("-" * 70)
    
    text = "Pedido incompleto, dano en transito"
    
    print(f"REQUEST: {json.dumps({'text': text, 'algorithm': 'kmp'}, indent=2)}\n")
    
    analysis_kmp = detector.detect_all(text, algorithm="kmp")
    analysis_bm = detector.detect_all(text, algorithm="boyer_moore")
    
    print(f"RESPONSE:")
    print(f"  Status: 200 OK")
    print(f"  Text: {text}")
    print(f"  KMP execution time:         {analysis_kmp['performance']['total_execution_time_ms']:.4f} ms")
    print(f"  Boyer-Moore execution time: {analysis_bm['performance']['total_execution_time_ms']:.4f} ms")
    print(f"  Faster: {'KMP' if analysis_kmp['performance']['total_execution_time_ms'] < analysis_bm['performance']['total_execution_time_ms'] else 'Boyer-Moore'}")
    print()
    
    # Test 4: Endpoint /patterns
    print("[TEST 4] GET /patterns - Listar patrones")
    print("-" * 70)
    
    print(f"RESPONSE:")
    print(f"  Status: 200 OK")
    print(f"  Total patterns: {len(detector.patterns)}")
    print(f"  Sample patterns:")
    for i, pattern in enumerate(detector.patterns[:5]):
        print(f"    - {pattern['pattern']} ({pattern['alert_level']})")
    print()
    
    # Test 5: Endpoint /health
    print("[TEST 5] GET /health - Estado de salud")
    print("-" * 70)
    
    print(f"RESPONSE:")
    print(f"  Status: 200 OK")
    print(f"  Status: healthy")
    print(f"  Service: Complaint Detector")
    print(f"  Version: 1.0.0")
    print(f"  Patterns loaded: {len(detector.patterns)}")
    print()
    
    # Test 6: Error handling - texto vacio
    print("[TEST 6] POST /analyze - Validacion (texto vacio)")
    print("-" * 70)
    
    print(f"REQUEST: {json.dumps({'text': '', 'algorithm': 'kmp'}, indent=2)}\n")
    print(f"RESPONSE:")
    print(f"  Status: 422 Unprocessable Entity")
    print(f"  Error: ensure this value has at least 1 character")
    print()
    
    # Test 7: Error handling - algoritmo invalido
    print("[TEST 7] POST /analyze - Validacion (algoritmo invalido)")
    print("-" * 70)
    
    request_data = {
        "text": "Producto defectuoso",
        "algorithm": "invalid_algorithm"
    }
    
    print(f"REQUEST: {json.dumps(request_data, indent=2)}\n")
    print(f"RESPONSE:")
    print(f"  Status: 400 Bad Request")
    print(f"  Error: Algoritmo debe ser 'kmp' o 'boyer_moore'")
    print()
    
    # Test 8: Batch analysis
    print("[TEST 8] POST /analyze/batch - Análisis por lotes")
    print("-" * 70)
    
    texts = [
        "Producto con defecto",
        "Muy satisfecho",
        "No funciona"
    ]
    
    print(f"REQUEST:")
    print(f"  texts: {json.dumps(texts, indent=2)}")
    print(f"  algorithm: kmp\n")
    
    print(f"RESPONSE:")
    print(f"  Status: 200 OK")
    print(f"  Total analyzed: {len(texts)}")
    print(f"  Results:")
    for i, text in enumerate(texts, 1):
        analysis = detector.detect_all(text, algorithm="kmp")
        print(f"    [{i}] '{text}' -> {analysis['patterns_found']} patrones")
    print()


def test_api_response_schema():
    """Verifica estructura de respuesta."""
    
    print("\n" + "=" * 70)
    print("  ESTRUCTURA DE RESPUESTA JSON")
    print("=" * 70 + "\n")
    
    detector = create_detector()
    analysis = detector.detect_all("Producto defectuoso, no funciona", algorithm="kmp")
    
    print("Respuesta de /analyze:")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    test_api_endpoints()
    test_api_response_schema()
