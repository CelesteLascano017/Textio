# Textio

Textio es una aplicación académica desarrollada para la detección automática de reclamos críticos en textos de atención al cliente, utilizando algoritmos clásicos de **Pattern Matching**: **Knuth–Morris–Pratt (KMP)** y **Boyer–Moore**.

El proyecto se enfoca en el uso correcto, eficiente y justificado de algoritmos de búsqueda de patrones, sin recurrir a técnicas de inteligencia artificial.

---

## Descripción del problema

En contextos empresariales (banca, telecomunicaciones, retail, transporte, entre otros), los clientes generan grandes volúmenes de mensajes a través de correos electrónicos, chats y formularios de soporte.  
Dentro de estos mensajes pueden existir reclamos graves, amenazas legales o intenciones de cancelación que requieren atención prioritaria.

Textio simula un sistema que permite identificar este tipo de mensajes mediante la detección de patrones textuales predefinidos, facilitando su clasificación según nivel de severidad.

---

## Objetivo del proyecto

Diseñar e implementar un prototipo que permita:

- Detectar patrones textuales relevantes en mensajes de clientes.
- Aplicar y comparar los algoritmos KMP y Boyer–Moore.
- Clasificar mensajes según el tipo de reclamo detectado.
- Analizar el rendimiento y las limitaciones de los algoritmos clásicos de búsqueda.

---

## Alcance

El sistema permite identificar patrones asociados a:

- Quejas leves  
- Reclamos  
- Reclamos críticos  
- Riesgo legal  

Los patrones son configurables y pueden ser cargados desde archivos externos, evitando que estén definidos directamente en el código.

Ejemplos de patrones:
- “pésimo servicio”
- “nunca solucionan nada”
- “cancelaré el servicio”
- “voy a demandar”
- “fraude”
- “esto es una estafa”

---

## Algoritmos implementados

### Knuth–Morris–Pratt (KMP)
Algoritmo de búsqueda eficiente que evita retrocesos innecesarios en el texto, utilizando información previa del patrón.

### Boyer–Moore
Algoritmo que compara el patrón desde el final, logrando un mejor rendimiento promedio, especialmente con patrones largos.

El sistema permite ejecutar ambos algoritmos sobre los mismos textos y comparar sus resultados y tiempos de ejecución.

---

## Flujo del sistema

1. Carga de mensajes de texto.
2. Carga de patrones desde archivo externo.
3. Ejecución de KMP o Boyer–Moore.
4. Detección de coincidencias.
5. Clasificación del mensaje según el patrón encontrado.
6. Visualización de resultados.

---

## Funcionalidades principales

- Carga de mensajes desde archivos `.txt`, `.csv` o `.xlsx`.
- Carga y edición dinámica de patrones.
- Detección de múltiples patrones en un mismo mensaje.
- Comparación de tiempos de ejecución entre algoritmos.
- Manejo de errores (archivos inexistentes, archivos vacíos, patrones no encontrados).
- Visualización clara de resultados.

---

## Pruebas

El sistema incluye casos de prueba que consideran:

- Patrones al inicio, medio y final del texto.
- Casos positivos y negativos.
- Diferencias entre mayúsculas y minúsculas.
- Presencia o ausencia de tildes.
- Variantes gramaticales.
- Detección de más de un patrón en un mismo mensaje.

---

## Limitaciones

Al basarse únicamente en búsqueda literal de patrones, el sistema presenta limitaciones como:

- No detección de sinónimos.
- Sensibilidad a errores ortográficos.
- Falta de comprensión semántica del texto.
- Posibles falsos positivos por ambigüedad del lenguaje.

Estas limitaciones forman parte del análisis crítico del proyecto.

---

## Tecnologías utilizadas

- Lenguaje de programación: Python o Java  
- Algoritmos: KMP y Boyer–Moore  
- Entrada de datos: `.txt`, `.csv`, `.xlsx`  
- Interfaz: consola o interfaz gráfica simple  

---

## Contexto académico

Proyecto desarrollado para la asignatura **Estructuras de Datos II**, con énfasis en:

- Dominio algorítmico.
- Diseño de software.
- Análisis de rendimiento.
- Evaluación crítica de soluciones clásicas.

---

## Licencia

Proyecto de uso académico y educativo.
