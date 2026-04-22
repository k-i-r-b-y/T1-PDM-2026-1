## Tarea 1

Repositorio preparado para desarrollar la tarea en dos frentes:

- Parte 1: pipeline ETL reproducible para construir un warehouse en esquema estrella.
- Parte 2: analítica manual con MapReduce en Python sobre los archivos generados por el warehouse.

## Estructura

```text
data/
  raw/                  # CSV de entrada
  warehouse/            # Salida del ETL
  analytics/            # Resultados analíticos si luego se persisten
scripts/
  run_etl.py            # Ejecuta el pipeline ETL completo
  run_analytics.py      # Ejecuta una analítica puntual sobre fact_news
src/
  etl/                  # Limpieza, dimensiones, fact table, particionado y validaciones
  mapreduce/            # Implementaciones manuales de map/reduce para la parte 2
  utils/                # Utilidades transversales
tests/                  # Smoke tests iniciales
```

## ETL

El ETL quedó organizado para seguir el flujo pedido en el enunciado:

1. lectura del CSV crudo
2. limpieza y normalización
3. enriquecimiento con región
4. construcción de dimensiones
5. generación de `fact_news`
6. validaciones base
7. escritura del warehouse particionado por `year` y `month`

Ejecución esperada:

```bash
python scripts/run_etl.py
```

Para una corrida acotada de prueba:

```bash
python scripts/run_etl.py --limit 1000
```

## Analítica MapReduce

La parte analítica quedó separada en módulos independientes para implementar:

- top-k de términos por mes
- distribución regional de palabras
- divergencia de vocabulario por fuente
- detección de peaks diarios

Ejecución esperada:

```bash
python scripts/run_analytics.py --analysis top_k_terms
python scripts/run_analytics.py --analysis region_word_distribution
python scripts/run_analytics.py --analysis source_divergence
python scripts/run_analytics.py --analysis daily_peaks
```

Cada análisis puede correrse también con `--limit` para pruebas rápidas.

## Estado actual

Esta primera intervención deja el esqueleto ejecutable, las firmas principales y una base mínima de transformación y validación. Falta completar la lógica final de negocio, endurecer las reglas de desambiguación regional y terminar las salidas analíticas requeridas por la entrega.
