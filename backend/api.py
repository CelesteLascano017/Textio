"""
API web para detección de reclamos.
Usa FastAPI para servir endpoints de análisis de patrones.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import json

from services.detector import create_detector
from preprocessing.normalize import normalize_text


# ==================== MODELOS PYDANTIC ====================

class AnalyzeRequest(BaseModel):
    """Modelo de solicitud de análisis."""
    text: str = Field(..., min_length=1, max_length=5000, description="Texto a analizar")
    algorithm: str = Field(default="kmp", description="Algoritmo: 'kmp' o 'boyer_moore'")
    
    class Config:
        example = {
            "text": "Producto con defecto, no funciona",
            "algorithm": "kmp"
        }


class DetectionInfo(BaseModel):
    """Información de un patrón detectado."""
    pattern: str
    category: str
    alert_level: str
    alert_message: str
    positions: List[int]
    found: bool
    match_count: int


class AnalyzeResponse(BaseModel):
    """Modelo de respuesta de análisis."""
    original_text: str
    normalized_text: str
    algorithm: str
    detections: List[DetectionInfo]
    total_patterns_checked: int
    patterns_found: int
    has_complaints: bool
    alert_levels: dict
    performance: dict
    
    class Config:
        example = {
            "original_text": "Producto defectuoso",
            "normalized_text": "producto defectuoso",
            "algorithm": "kmp",
            "detections": [],
            "total_patterns_checked": 21,
            "patterns_found": 1,
            "has_complaints": True,
            "alert_levels": {"high": 1, "medium": 0, "low": 0},
            "performance": {
                "total_execution_time_ms": 0.2345,
                "algorithm_used": "kmp"
            }
        }


class HealthResponse(BaseModel):
    """Modelo de respuesta de salud."""
    status: str
    service: str
    version: str
    patterns_loaded: int


# ==================== INSTANCIA FASTAPI ====================

app = FastAPI(
    title="API de Detección de Reclamos",
    description="API para detectar patrones de reclamos usando KMP y Boyer-Moore",
    version="1.0.0",
)

# Configurar CORS para permitir peticiones del frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar detector globalmente
try:
    detector = create_detector()
    PATTERNS_COUNT = len(detector.patterns)
except Exception as e:
    print(f"Error al cargar patrones: {e}")
    detector = None
    PATTERNS_COUNT = 0


# ==================== ENDPOINTS ====================

@app.get("/", tags=["Info"])
def root():
    """Endpoint raíz con información de la API."""
    return {
        "name": "Complaint Detection API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Info"])
def health():
    """Endpoint de salud."""
    return HealthResponse(
        status="healthy" if detector else "error",
        service="Complaint Detector",
        version="1.0.0",
        patterns_loaded=PATTERNS_COUNT
    )


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
def analyze(request: AnalyzeRequest):
    """
    Analiza texto en busca de patrones de reclamos.
    
    - **text**: Texto a analizar (máximo 5000 caracteres)
    - **algorithm**: Algoritmo de búsqueda ("kmp" o "boyer_moore")
    
    Retorna estructura con detecciones, tiempos y análisis.
    """
    if not detector:
        raise HTTPException(
            status_code=503,
            detail="Detector not available"
        )
    
    # Validar algoritmo
    if request.algorithm not in ["kmp", "boyer_moore"]:
        raise HTTPException(
            status_code=400,
            detail="Algoritmo debe ser 'kmp' o 'boyer_moore'"
        )
    
    try:
        # Realizar análisis
        analysis = detector.detect_all(request.text, algorithm=request.algorithm)
        
        # Convertir a modelo de respuesta
        response = AnalyzeResponse(
            original_text=analysis["original_text"],
            normalized_text=analysis["normalized_text"],
            algorithm=analysis["algorithm"],
            detections=[DetectionInfo(**d) for d in analysis["detections"]],
            total_patterns_checked=analysis["total_patterns_checked"],
            patterns_found=analysis["patterns_found"],
            has_complaints=analysis["has_complaints"],
            alert_levels=analysis["alert_levels"],
            performance=analysis["performance"]
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante análisis: {str(e)}"
        )


@app.post("/analyze/batch", tags=["Analysis"])
def analyze_batch(texts: List[str], algorithm: str = "kmp"):
    """
    Analiza múltiples textos en una solicitud.
    
    Retorna lista de análisis con resultados y tiempos.
    """
    if not detector:
        raise HTTPException(
            status_code=503,
            detail="Detector not available"
        )
    
    if not texts or len(texts) == 0:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar al menos un texto"
        )
    
    if len(texts) > 100:
        raise HTTPException(
            status_code=400,
            detail="Máximo 100 textos por solicitud"
        )
    
    try:
        results = []
        for text in texts:
            analysis = detector.detect_all(text, algorithm=algorithm)
            results.append(analysis)
        
        return {
            "total_analyzed": len(results),
            "algorithm": algorithm,
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante análisis batch: {str(e)}"
        )


@app.get("/patterns", tags=["Info"])
def get_patterns():
    """
    Retorna lista de patrones cargados.
    """
    if not detector:
        raise HTTPException(
            status_code=503,
            detail="Detector not available"
        )
    
    return {
        "total_patterns": len(detector.patterns),
        "patterns": [
            {
                "pattern": p["pattern"],
                "category": p["category"],
                "alert_level": p["alert_level"]
            }
            for p in detector.patterns
        ]
    }


@app.post("/compare", tags=["Analysis"])
def compare_algorithms(request: AnalyzeRequest):
    """
    Compara resultado y tiempo de ejecución entre KMP y Boyer-Moore.
    """
    if not detector:
        raise HTTPException(
            status_code=503,
            detail="Detector not available"
        )
    
    try:
        analysis_kmp = detector.detect_all(request.text, algorithm="kmp")
        analysis_bm = detector.detect_all(request.text, algorithm="boyer_moore")
        
        return {
            "original_text": request.text,
            "kmp": {
                "patterns_found": analysis_kmp["patterns_found"],
                "execution_time_ms": analysis_kmp["performance"]["total_execution_time_ms"],
                "detections": analysis_kmp["detections"]
            },
            "boyer_moore": {
                "patterns_found": analysis_bm["patterns_found"],
                "execution_time_ms": analysis_bm["performance"]["total_execution_time_ms"],
                "detections": analysis_bm["detections"]
            },
            "comparison": {
                "faster": "kmp" if analysis_kmp["performance"]["total_execution_time_ms"] < 
                         analysis_bm["performance"]["total_execution_time_ms"] else "boyer_moore",
                "difference_ms": abs(
                    analysis_kmp["performance"]["total_execution_time_ms"] -
                    analysis_bm["performance"]["total_execution_time_ms"]
                )
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante comparación: {str(e)}"
        )


# ==================== PATTERN CRUD ENDPOINTS ====================

class PatternRequest(BaseModel):
    """Modelo para crear/actualizar patrón."""
    pattern: str = Field(..., min_length=1, max_length=100, description="Patrón de texto")
    category: str = Field(..., min_length=1, max_length=50, description="Categoría del patrón")
    alert_level: str = Field(default="medium", description="Nivel: 'high', 'medium', 'low'")
    alert_message: str = Field(default="", max_length=200, description="Mensaje de alerta")


@app.post("/patterns", tags=["Patterns"])
def create_pattern(request: PatternRequest):
    """
    Crea un nuevo patrón.
    """
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not available")
    
    if request.alert_level not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="alert_level debe ser 'high', 'medium' o 'low'")
    
    try:
        result = detector.add_pattern(
            pattern=request.pattern,
            category=request.category,
            alert_level=request.alert_level,
            alert_message=request.alert_message or f"Patrón '{request.pattern}' detectado"
        )
        detector.save_patterns()
        return {"success": True, "pattern": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear patrón: {str(e)}")


@app.put("/patterns/{index}", tags=["Patterns"])
def update_pattern(index: int, request: PatternRequest):
    """
    Actualiza un patrón existente por índice.
    """
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not available")
    
    if request.alert_level not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="alert_level debe ser 'high', 'medium' o 'low'")
    
    try:
        result = detector.update_pattern(
            index=index,
            pattern=request.pattern,
            category=request.category,
            alert_level=request.alert_level,
            alert_message=request.alert_message or f"Patrón '{request.pattern}' detectado"
        )
        detector.save_patterns()
        return {"success": True, "pattern": result}
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar patrón: {str(e)}")


@app.delete("/patterns/{index}", tags=["Patterns"])
def delete_pattern(index: int):
    """
    Elimina un patrón por índice.
    """
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not available")
    
    try:
        result = detector.delete_pattern(index)
        detector.save_patterns()
        return {"success": True, "deleted": result}
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar patrón: {str(e)}")


@app.post("/patterns/save", tags=["Patterns"])
def save_all_patterns():
    """
    Guarda todos los patrones actuales al archivo CSV.
    """
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not available")
    
    try:
        detector.save_patterns()
        return {"success": True, "patterns_saved": len(detector.patterns)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar patrones: {str(e)}")


@app.post("/patterns/reload", tags=["Patterns"])
def reload_patterns():
    """
    Recarga patrones desde el archivo CSV.
    """
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not available")
    
    try:
        count = detector.reload_patterns()
        return {"success": True, "patterns_loaded": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recargar patrones: {str(e)}")


# ==================== SETUP CONFIG ENDPOINTS ====================

# Simple in-memory config storage (could be replaced with database)
_setup_config = {
    "text_name": "",
    "pattern_group": "Claims",
    "algorithm": "kmp"
}


class SetupConfigRequest(BaseModel):
    """Modelo de configuración del setup."""
    text_name: str = Field(default="", max_length=100)
    pattern_group: str = Field(default="Claims", description="Grupo: 'Claims', 'Complaints', 'Custom'")
    algorithm: str = Field(default="kmp", description="Algoritmo: 'kmp' o 'boyer_moore'")


@app.get("/setup/config", tags=["Setup"])
def get_setup_config():
    """
    Obtiene la configuración actual del setup.
    """
    return _setup_config


@app.post("/setup/config", tags=["Setup"])
def save_setup_config(request: SetupConfigRequest):
    """
    Guarda la configuración del setup.
    """
    global _setup_config
    
    if request.pattern_group not in ["Claims", "Complaints", "Custom"]:
        raise HTTPException(status_code=400, detail="pattern_group debe ser 'Claims', 'Complaints' o 'Custom'")
    
    if request.algorithm not in ["kmp", "boyer_moore"]:
        raise HTTPException(status_code=400, detail="algorithm debe ser 'kmp' o 'boyer_moore'")
    
    _setup_config = {
        "text_name": request.text_name,
        "pattern_group": request.pattern_group,
        "algorithm": request.algorithm
    }
    
    return {"success": True, "config": _setup_config}


# ==================== MANEJO DE ERRORES ====================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return {
        "detail": str(exc),
        "type": "validation_error"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Ejecutar servidor
    print("\n" + "=" * 70)
    print("  API DE DETECCION DE RECLAMOS")
    print("=" * 70)
    print(f"\nPatrones cargados: {PATTERNS_COUNT}")
    print("\nIniciando servidor en http://localhost:8000")
    print("Documentación: http://localhost:8000/docs")
    print("\n" + "=" * 70 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
