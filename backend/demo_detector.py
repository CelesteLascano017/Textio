"""
Script de demostración del detector de reclamos.
"""

import json
from services.detector import create_detector


def demo_detector():
    """Demuestra el funcionamiento del detector."""
    
    detector = create_detector()
    
    test_cases = [
        "Producto con defecto grave, no funciona",
        "Pedido incompleto y con daño en transito",
        "Muy malo, pésimo servicio",
        "Todo llegó bien, muy satisfecho",
        "Solicito ayuda con mi devolución",
    ]
    
    print("\n" + "=" * 70)
    print("  DEMO: DETECTOR DE RECLAMOS")
    print("=" * 70 + "\n")
    
    for i, text in enumerate(test_cases, 1):
        print(f"[Caso {i}] {text}\n")
        
        # Análisis con KMP
        analysis = detector.detect_all(text, algorithm="kmp")
        
        # Mostrar resultados
        print(f"  Algoritmo:              {analysis['algorithm'].upper()}")
        print(f"  Patrones encontrados:   {analysis['patterns_found']}/{analysis['total_patterns_checked']}")
        print(f"  Tiene reclamos:         {'SI' if analysis['has_complaints'] else 'NO'}")
        
        if analysis['has_complaints']:
            print(f"  Alertas por nivel:")
            print(f"    - HIGH:   {analysis['alert_levels']['high']}")
            print(f"    - MEDIUM: {analysis['alert_levels']['medium']}")
            print(f"    - LOW:    {analysis['alert_levels']['low']}")
            print(f"\n  Patrones detectados:")
            
            for detection in analysis['detections']:
                print(f"    [{detection['alert_level'].upper()}] {detection['pattern']}")
                print(f"      Mensaje: {detection['alert_message']}")
                print(f"      Posiciones: {detection['positions']}")
        
        print("\n" + "-" * 70 + "\n")
    
    # Ejemplo con JSON
    print("\n" + "=" * 70)
    print("  EJEMPLO: RESPUESTA JSON")
    print("=" * 70 + "\n")
    
    text = "Producto defectuoso, no funciona correctamente"
    analysis = detector.detect_all(text)
    
    print(f"Entrada: {text}\n")
    print("Respuesta JSON:")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    demo_detector()
