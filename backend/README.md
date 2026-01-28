# Sistema de Detección de Reclamos

Aplicación web para detección de patrones de reclamos en texto usando algoritmos clásicos de búsqueda: **KMP (Knuth-Morris-Pratt)** y **Boyer-Moore**.

## Características

- ✅ Algoritmo KMP con complejidad O(n+m)
- ✅ Algoritmo Boyer-Moore con bad character rule
- ✅ Preprocesamiento de texto: minúsculas, eliminación de tildes, puntuación
- ✅ 21 patrones predefinidos con categorías y niveles de alerta
- ✅ Medición de tiempo de ejecución en milisegundos
- ✅ API REST con FastAPI
- ✅ Comparación de algoritmos
- ✅ Análisis por lotes (batch processing)

## Estructura del Proyecto

```
backend/
├── algorithms/
│   ├── kmp.py              # Algoritmo KMP
│   └── boyer_moore.py      # Algoritmo Boyer-Moore
│
├── preprocessing/
│   └── normalize.py        # Normalización de texto
│
├── services/
│   └── detector.py         # Servicio central de detección
│
├── data/
│   ├── patterns.csv        # Patrones de reclamos
│   └── messages.txt        # Mensajes de prueba
│
├── api.py                  # API FastAPI
├── benchmark.py            # Medición de rendimiento
├── main.py                 # Pruebas unitarias
├── demo_detector.py        # Demostración del detector
├── demo_benchmark.py       # Demostración de benchmarks
└── test_api.py            # Pruebas de API (sin servidor)
```

## Instalación

### Requisitos
- Python 3.9+
- pip

### Dependencias

```bash
pip install fastapi uvicorn pydantic
```

O instalar desde requirements.txt (si existe):

```bash
pip install -r requirements.txt
```

## Uso

### 1. Ejecutar Pruebas Unitarias

```bash
python main.py
```

Ejecuta 20 pruebas incluyendo:
- Normalización de texto
- Búsqueda KMP y Boyer-Moore
- Detector de patrones
- Benchmarks de rendimiento

### 2. Demostración del Detector

```bash
python demo_detector.py
```

Demuestra el detector con casos de uso reales y salida en JSON.

### 3. Demostración de Benchmarks

```bash
python demo_benchmark.py
```

Compara rendimiento de KMP vs Boyer-Moore en múltiples casos.

### 4. Pruebas de API (sin servidor)

```bash
python test_api.py
```

Simula solicitudes a todos los endpoints sin ejecutar servidor.

### 5. Iniciar Servidor FastAPI

```bash
python api.py
```

El servidor estará disponible en `http://localhost:8000`

**Documentación interactiva:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### GET /
Información general de la API.

**Respuesta:**
```json
{
  "name": "Complaint Detection API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

### GET /health
Estado de salud del servicio.

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Complaint Detector",
  "version": "1.0.0",
  "patterns_loaded": 21
}
```

### POST /analyze
Analiza texto en busca de patrones de reclamos.

**Solicitud:**
```json
{
  "text": "Producto con defecto, no funciona",
  "algorithm": "kmp"
}
```

**Respuesta:**
```json
{
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
      "found": true,
      "match_count": 1
    }
  ],
  "total_patterns_checked": 21,
  "patterns_found": 1,
  "has_complaints": true,
  "alert_levels": {
    "high": 1,
    "medium": 0,
    "low": 0
  },
  "performance": {
    "total_execution_time_ms": 0.2121,
    "algorithm_used": "kmp"
  }
}
```

**Parámetros:**
- `text` (string, requerido): Texto a analizar (1-5000 caracteres)
- `algorithm` (string, opcional): "kmp" o "boyer_moore" (default: "kmp")

### POST /analyze/batch
Analiza múltiples textos en una solicitud.

**Solicitud:**
```json
{
  "texts": ["Texto 1", "Texto 2", "Texto 3"],
  "algorithm": "kmp"
}
```

**Respuesta:**
```json
{
  "total_analyzed": 3,
  "algorithm": "kmp",
  "results": [...]
}
```

### POST /compare
Compara rendimiento y resultados de KMP vs Boyer-Moore.

**Solicitud:**
```json
{
  "text": "Producto defectuoso",
  "algorithm": "kmp"
}
```

**Respuesta:**
```json
{
  "original_text": "Producto defectuoso",
  "kmp": {
    "patterns_found": 1,
    "execution_time_ms": 0.2019,
    "detections": [...]
  },
  "boyer_moore": {
    "patterns_found": 1,
    "execution_time_ms": 0.1422,
    "detections": [...]
  },
  "comparison": {
    "faster": "boyer_moore",
    "difference_ms": 0.0597
  }
}
```

### GET /patterns
Lista todos los patrones cargados.

**Respuesta:**
```json
{
  "total_patterns": 21,
  "patterns": [
    {
      "pattern": "defecto",
      "category": "producto_defectuoso",
      "alert_level": "high"
    },
    ...
  ]
}
```

## Patrones Predefinidos

El sistema incluye 21 patrones de reclamos:

| Patrón | Categoría | Nivel |
|--------|-----------|-------|
| defecto | producto_defectuoso | HIGH |
| no funciona | producto_no_funcional | HIGH |
| roto | producto_danado | HIGH |
| problema | problema_general | MEDIUM |
| incompleto | producto_incompleto | MEDIUM |
| demora | demora_entrega | MEDIUM |
| no llego | entrega_faltante | HIGH |
| perdido | entrega_perdida | HIGH |
| daño | daño | HIGH |
| calidad | problema_calidad | MEDIUM |
| insatisfecho | insatisfaccion | MEDIUM |
| pésimo | muy_malo | HIGH |
| malo | malo | MEDIUM |
| decepcion | decepcion | MEDIUM |
| refund | devolucion | MEDIUM |
| cambio | cambio_producto | MEDIUM |
| no recomiendo | desconfianza | MEDIUM |
| fraude | fraude | HIGH |
| engaño | engaño | HIGH |
| no entiendo | confuso | LOW |
| ayuda | solicitud_ayuda | LOW |

## Ejemplo de Uso con cURL

### Analizar texto
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Producto defectuoso, no funciona",
    "algorithm": "kmp"
  }'
```

### Comparar algoritmos
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Producto defectuoso",
    "algorithm": "kmp"
  }'
```

### Listar patrones
```bash
curl "http://localhost:8000/patterns"
```

### Verificar salud
```bash
curl "http://localhost:8000/health"
```

## Ejemplo de Uso con Python

```python
import requests

# Solicitud al endpoint /analyze
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "text": "Producto con defecto",
        "algorithm": "kmp"
    }
)

result = response.json()
print(f"Patrones encontrados: {result['patterns_found']}")
print(f"Tiempo de ejecución: {result['performance']['total_execution_time_ms']:.4f} ms")
print(f"Detecciones: {[d['pattern'] for d in result['detections']]}")
```

## Niveles de Alerta

- **HIGH**: Reclamos críticos (defecto, no funciona, roto, fraude, etc.)
- **MEDIUM**: Reclamos importantes (problema, incompleto, demora, etc.)
- **LOW**: Reclamos menores (ayuda, confuso)

## Normalización de Texto

El sistema normaliza automáticamente:
1. Convierte a minúsculas
2. Elimina acentos/tildes (é → e, ñ → n)
3. Elimina signos de puntuación (!, ?, .)
4. Normaliza espacios

Ejemplo:
```
"¡PÉSIMO Servicio!" → "pesimo servicio"
```

## Rendimiento

Mediciones típicas (tiempo por búsqueda en ms):

| Algoritmo | Tiempo Promedio |
|-----------|-----------------|
| KMP | 0.006-0.008 ms |
| Boyer-Moore | 0.003-0.005 ms |

Boyer-Moore es generalmente más rápido para patrones cortos en textos largos.

## Notas Técnicas

- **KMP**: Usa tabla LPS (Longest Proper Prefix which is also Suffix)
- **Boyer-Moore**: Usa regla de carácter malo (Bad Character Rule)
- **Medición**: `time.perf_counter()` para máxima precisión
- **Validación**: Modelos Pydantic para solicitudes/respuestas
- **Documentación**: Swagger UI generada automáticamente

## Licencia

Proyecto académico para fines educativos.
