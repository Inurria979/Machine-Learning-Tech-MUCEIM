# Lean Network Challenge — First Practical Laboratory (MUCEIM, Machine Learning Technologies)

Objetivo: encontrar la red totalmente conectada (MLP) con menos parámetros cuya accuracy de test
(media de 3 semillas) quede a menos de 1 punto porcentual de la del modelo de referencia.

## Ficheros

- `First Practical Laboratory - Machine Learning Technologies - MUCEIM.pdf`: enunciado. Es la fuente de verdad.
- `First_Practical_Laboratory_Template.ipynb`: plantilla original. **No se modifica**; se trabaja sobre una copia (`Lean_Network_Challenge.ipynb`).
- Entregables: notebook de Colab ejecutado de principio a fin + informe PDF.

## Reglas del reto (no negociables)

1. **Referencia intacta**: MLP 512-512 ReLU, Adam 1e-3, 20 épocas, batch 128. La celda de la sección 4 no se toca. Se entrena una sola vez.
2. **Objetivo**: `target_acc = ref_test_acc - 0.01`. Cuenta la **media de test sobre 3 semillas** del modelo final.
3. **Parámetros**: `model.count_params()` (todos los pesos y sesgos, incluidos los no entrenables, p. ej. BatchNorm).
4. **Uso justo de los datos**: todas las decisiones de diseño se toman con validación (10 % de train, semilla 42). El conjunto de test solo se usa para la referencia y para el modelo lean final. Nunca se elige entre candidatos mirando test.
5. **Solo redes totalmente conectadas** (Dense). Nada de convoluciones. Cualquier técnica de las Unidades 1 y 2 vale.
6. **Al menos 3 experimentos**, variando **un factor cada vez**: anchura, profundidad, activaciones, regularización, optimización, tamaño de entrada.
7. Cada modelo entrenado se registra con `record(...)`; cada experimento lleva hipótesis previa, curvas de entrenamiento/validación y análisis.
8. Gráfica resumen: accuracy de validación frente a parámetros, eje X logarítmico.
9. El notebook debe ejecutarse sin errores con "Restart and run all" en Google Colab (TensorFlow/Keras, sin instalación adicional).

## Rúbrica

| Criterio | Peso |
| --- | --- |
| Rigor experimental (hipótesis, un factor cada vez, validación/test, 3 semillas) | 40 % |
| Análisis e insight (explicar el *porqué* con conceptos de la Unidad 2) | 30 % |
| Calidad y reproducibilidad del código | 20 % |
| Claridad y profesionalidad del informe | 10 % |

El tamaño final de la red no puntúa directamente: un estudio cuidadoso que no alcance el objetivo puede sacar la nota máxima.

## Convenciones

- Notebook e informe en **inglés** (idioma de la asignatura). La conversación con el estudiante, en español.
- Nunca se inventan resultados: toda cifra del análisis o del informe debe salir de una salida real de celda.
- Semillas fijadas con `keras.utils.set_random_seed(...)` antes de construir cada modelo.
- El estudiante debe poder explicar cada línea y cada decisión: código simple y comentado antes que ingenioso.
- El uso de asistentes de IA se documenta con honestidad (sección 10 del notebook y sección del informe).

## Flujo de trabajo con los agentes

El `orchestrator` (Opus, esfuerzo medio) coordina y es el agente principal de la sesión (`.claude/settings.json`).

1. `experiment-designer` (Opus, medio) → plan de experimentos con hipótesis y presupuestos de parámetros.
2. `notebook-engineer` (Sonnet) → implementa y ejecuta las celdas.
3. `results-analyst` (Opus, medio) → redacta los análisis en markdown a partir de las salidas reales.
4. `rigor-reviewer` (Opus, medio) → audita contra las reglas y la rúbrica (repetir 2–4 hasta que pase).
5. `report-writer` (Sonnet) → informe PDF.
6. `lab-tutor` (Opus, medio) → prepara al estudiante para justificar el trabajo.

Apoyo:
- `researcher` (Haiku) → búsquedas en ficheros e internet.
- `fable-wildcard` (Fable) → comodín para bloqueos. **Solo hasta el 2026-11-16 incluido**; después, no usarlo.
