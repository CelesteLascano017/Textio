"""
Script para demostrar cómo usar la API.
Proporciona ejemplos de código cliente.
"""

import json


def show_curl_examples():
    """Muestra ejemplos con cURL."""
    
    print("\n" + "=" * 70)
    print("  EJEMPLOS DE SOLICITUDES CON cURL")
    print("=" * 70 + "\n")
    
    examples = [
        {
            "title": "1. Analizar texto (KMP)",
            "command": '''curl -X POST "http://localhost:8000/analyze" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Producto defectuoso, no funciona",
    "algorithm": "kmp"
  }' '''
        },
        {
            "title": "2. Analizar texto (Boyer-Moore)",
            "command": '''curl -X POST "http://localhost:8000/analyze" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Pedido incompleto con daño",
    "algorithm": "boyer_moore"
  }' '''
        },
        {
            "title": "3. Comparar algoritmos",
            "command": '''curl -X POST "http://localhost:8000/compare" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Producto defectuoso"
  }' '''
        },
        {
            "title": "4. Listar patrones",
            "command": 'curl "http://localhost:8000/patterns"'
        },
        {
            "title": "5. Verificar salud",
            "command": 'curl "http://localhost:8000/health"'
        },
        {
            "title": "6. Análisis por lotes",
            "command": '''curl -X POST "http://localhost:8000/analyze/batch" \\
  -H "Content-Type: application/json" \\
  -d '{
    "texts": ["Producto con defecto", "Muy satisfecho", "No funciona"],
    "algorithm": "kmp"
  }' '''
        },
    ]
    
    for example in examples:
        print(f"{example['title']}")
        print("-" * 70)
        print(example['command'])
        print()


def show_python_examples():
    """Muestra ejemplos con Python/requests."""
    
    print("\n" + "=" * 70)
    print("  EJEMPLOS DE CÓDIGO PYTHON")
    print("=" * 70 + "\n")
    
    examples = [
        {
            "title": "1. Importar y usar detector localmente",
            "code": '''from services.detector import create_detector

detector = create_detector()
analysis = detector.detect_all("Producto defectuoso", algorithm="kmp")

print(f"Patrones: {analysis['patterns_found']}")
print(f"Tiempo: {analysis['performance']['total_execution_time_ms']:.4f} ms")
'''
        },
        {
            "title": "2. Cliente HTTP con requests",
            "code": '''import requests

url = "http://localhost:8000/analyze"
payload = {
    "text": "Producto con defecto",
    "algorithm": "kmp"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Status: {response.status_code}")
print(f"Patrones encontrados: {result['patterns_found']}")
'''
        },
        {
            "title": "3. Comparar algoritmos",
            "code": '''import requests

url = "http://localhost:8000/compare"
payload = {"text": "Producto defectuoso"}

response = requests.post(url, json=payload)
data = response.json()

print(f"KMP: {data['kmp']['execution_time_ms']:.4f} ms")
print(f"Boyer-Moore: {data['boyer_moore']['execution_time_ms']:.4f} ms")
print(f"Más rápido: {data['comparison']['faster']}")
'''
        },
        {
            "title": "4. Análisis por lotes",
            "code": '''import requests

url = "http://localhost:8000/analyze/batch"
payload = {
    "texts": ["Defecto", "Muy bueno", "No funciona"],
    "algorithm": "kmp"
}

response = requests.post(url, json=payload)
data = response.json()

for result in data['results']:
    print(f"{result['original_text']}: {result['patterns_found']} patrones")
'''
        },
        {
            "title": "5. Obtener lista de patrones",
            "code": '''import requests

response = requests.get("http://localhost:8000/patterns")
data = response.json()

print(f"Total de patrones: {data['total_patterns']}")
for p in data['patterns'][:5]:
    print(f"  - {p['pattern']} ({p['alert_level']})")
'''
        },
    ]
    
    for example in examples:
        print(f"{example['title']}")
        print("-" * 70)
        print(example['code'])
        print()


def show_startup_instructions():
    """Muestra instrucciones de inicio."""
    
    print("\n" + "=" * 70)
    print("  INSTRUCCIONES DE INICIO")
    print("=" * 70 + "\n")
    
    print("1. Instalar dependencias:")
    print("   pip install -r requirements.txt\n")
    
    print("2. Ejecutar servidor:")
    print("   python api.py\n")
    
    print("3. Acceder a documentación:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc\n")
    
    print("4. Probar desde otra terminal:")
    print("   curl http://localhost:8000/health\n")
    
    print("5. Ejecutar pruebas (sin servidor):")
    print("   python test_api.py\n")


def show_response_example():
    """Muestra ejemplo de respuesta."""
    
    print("\n" + "=" * 70)
    print("  EJEMPLO DE RESPUESTA JSON")
    print("=" * 70 + "\n")
    
    example_response = {
        "original_text": "Producto con defecto, no funciona",
        "normalized_text": "producto con defecto no funciona",
        "algorithm": "kmp",
        "detections": [
            {
                "pattern": "defecto",
                "category": "producto_defectuoso",
                "alert_level": "high",
                "alert_message": "Posible defecto detectado en el producto",
                "positions": [18],
                "found": True,
                "match_count": 1
            },
            {
                "pattern": "no funciona",
                "category": "producto_no_funcional",
                "alert_level": "high",
                "alert_message": "Producto no funciona correctamente",
                "positions": [27],
                "found": True,
                "match_count": 1
            }
        ],
        "total_patterns_checked": 21,
        "patterns_found": 2,
        "has_complaints": True,
        "alert_levels": {
            "high": 2,
            "medium": 0,
            "low": 0
        },
        "performance": {
            "total_execution_time_ms": 0.2500,
            "algorithm_used": "kmp"
        }
    }
    
    print(json.dumps(example_response, indent=2, ensure_ascii=False))
    print()


if __name__ == "__main__":
    show_startup_instructions()
    show_curl_examples()
    show_python_examples()
    show_response_example()
