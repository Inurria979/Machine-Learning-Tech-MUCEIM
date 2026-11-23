# First Practical Laboratory — The Lean Network Challenge

## El enunciado (resumen propio)

La práctica plantea la pregunta contraria a la tendencia habitual del deep learning: en lugar de escalar, **¿cuánto se puede reducir una red neuronal sin que deje de funcionar?**

- Se parte de un **modelo de referencia** fijo: un perceptrón multicapa con dos capas ocultas de 512 neuronas ReLU, entrenado con Adam durante 20 épocas. Se entrena una sola vez y se anotan sus parámetros y su accuracy de test.
- Hay que encontrar la **red totalmente conectada (MLP) con menos parámetros** cuya accuracy de test, **promediada sobre tres semillas**, no quede más de **1 punto porcentual** por debajo de la referencia. Los parámetros se cuentan con `model.count_params()`.
- Se elige un dataset de clasificación de imágenes entre varias opciones (MNIST, Fashion-MNIST, Kuzushiji-MNIST, CIFAR-10 u otro público justificado).
- **Uso justo de los datos**: todas las decisiones de diseño se toman con un conjunto de validación sacado del entrenamiento; el test solo se usa para la referencia y para el modelo final.
- Solo se permiten MLP y técnicas vistas en las Unidades 1 y 2 (nada de convoluciones).
- Hay que hacer **al menos tres experimentos controlados**, cambiando un factor cada vez: anchura, profundidad, funciones de activación, regularización, optimizador o tamaño de la entrada.
- Para cada experimento: hipótesis previa, curvas de entrenamiento y validación, y análisis. Además, una gráfica resumen de accuracy de validación frente a número de parámetros (eje logarítmico) y una **Lean Network Card** con el resultado final.
- **Entregables**: un notebook de Google Colab ejecutado de principio a fin y un informe PDF (introducción, diseño experimental, resultados, Lean Network Card, uso de asistentes de IA, conclusiones y enlace al notebook).
- **Evaluación**: rigor experimental 40 %, análisis 30 %, calidad y reproducibilidad del código 20 %, claridad del informe 10 %. El tamaño final de la red no puntúa directamente.

## Resultado

Dataset elegido: **Fashion-MNIST** (54.000 train / 6.000 validación / 10.000 test).

| | Referencia | Red lean |
|---|---|---|
| Arquitectura | 784-512-512-10 | **196-64-64-10** (entrada 14x14 por promedio de áreas) |
| Parámetros | 669.706 | **17.418** |
| Accuracy de test | 0,8833 | **0,8737** (media de 3 semillas, sd 0,0008) |
| Objetivo | — | ≥ 0,8733 → **cumplido** |
| Compresión | — | **38,4x** (97,4 % menos parámetros) |

Experimentos realizados: anchura (E1), tamaño y método de reducción de la entrada (E2), anchura con entrada reducida (E3, E3b), profundidad (E4, E4b) y optimizador × regularización (E5). La clave fue reducir la entrada: el 60 % de los parámetros de la referencia está en la primera capa.

También se ejecutó el notebook completo en Google Colab (GPU T4) como comprobación de reproducibilidad: las cifras cambian ligeramente, pero se llega al mismo modelo final y también cumple el objetivo (0,8753).

## Contenido

| Fichero | Descripción |
|---|---|
| `Network Local.ipynb` | Notebook principal, ejecutado en local (CPU). Todo el análisis sale de esta ejecución. |
| `Network Collab.ipynb` | Ejecución completa en Google Colab (GPU T4), para comparar reproducibilidad. |
| `report/InurriaPorreroJ.pdf` | Informe final entregado. |
| `report/lean_network_challenge.md` | Fuente del informe. |
| `report/build.py`, `report/report.html`, `report/figures/` | Script que genera el PDF a partir del Markdown, HTML intermedio y figuras. |
| `tools/dump_notebook.py` | Utilidad que vuelca celdas y figuras del notebook a texto/PNG. |
| `pyproject.toml`, `uv.lock`, `.python-version` | Entorno de Python (gestionado con `uv`). |
| `.claude/` | Configuración y agentes de Claude Code usados como asistentes en la práctica. |

## Ejecutar

En Colab: abrir cualquiera de los notebooks y usar `Runtime > Restart and run all` (no requiere instalar nada).

En local:

```bash
uv sync
uv run jupyter lab
```
