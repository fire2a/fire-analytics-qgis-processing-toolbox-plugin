# Estado migración QGIS 4 / Qt6 (sesión 2026-06-10)

## Contexto
QGIS 4.0 "Norrköping" (marzo 2026) migró de Qt5 a Qt6 (PyQt5 → PyQt6) y rompió el plugin.
QGIS 4.2 LTR sale en octubre 2026 — deadline práctico.
Guía oficial: https://plugins.qgis.org/docs/migrate-qgis4

## Hecho (en esta rama, `feature/new-branch`)

- **234 enums convertidos a forma con scope completo** en 17 archivos, mapeados por
  introspección contra QGIS 3.44 local (scripts en `/tmp/qt6_enum_map.py` y `/tmp/qt6_apply.py`).
  Renames clave: `QgsProcessing.TypeRaster` → `Qgis.ProcessingSourceType.Raster`,
  `FlagAdvanced` → `Qgis.ProcessingParameterFlag.Advanced`,
  `QgsColorRampShader.Interpolated` → `Qgis.ShaderInterpolationMethod.Linear`,
  `QgsUnitTypes.DistanceMeters` → `Qgis.DistanceUnit.Meters`.
- `QVariant.Int/.String/.Bool/.Double` → `QMetaType.Type.*` (QVariant.Type no existe en PyQt6).
- `row[j] != QVariant()` → `!= NULL` (de qgis.core) en algorithm_clusterize.py y algorithm_knapsack.py.
- Imports `PyQt5` directos → `qgis.PyQt` (algorithm_clusterize.py, assets/resources.py).
- `qmb.exec_()` → `qmb.exec()` en dependencies_handler.py.
- Imports `Qgis`/`QMetaType`/`NULL` agregados donde faltaban; `QVariant` huérfanos removidos.
- `metadata.txt`: `qgisMinimumVersion` 3.34 → **3.40** (los enums `Qgis.*` requieren ≥3.36),
  agregado `qgisMaximumVersion=4.99`, changelog v1.1.0.

## Verificado

- Compilación OK de todos los archivos modificados.
- Bajo QGIS 3.44.7 local: provider carga, **24 algoritmos** y **193 definiciones de parámetros**
  se inicializan sin errores (usando venv `/tmp/qgis4test` con fire2a-lib==0.3.13 y pyomo).
- Re-introspección: no quedan enums sin scope.

## Pendiente

1. **~15 líneas >120 caracteres** que quedaron largas por los reemplazos (estilo black del proyecto):
   `algorithm_simulator.py` (8 llamadas `logMessage`), `dependencies_handler.py` (6 ídem),
   `algorithm_raster_tutorial.py:130`. Son solo formato — envolver argumentos.
   Detectarlas: `git diff main -U0 | awk '/^\+/ && length($0)>121'`.
2. **Probar en un build real de QGIS 4** (nightly o release): cargar plugin, correr el simulador
   y un algoritmo de cada grupo. La introspección se hizo contra 3.44, no 4.x.
3. Correr la suite `test/` (pytest-qgis) — no se corrió en esta sesión.
4. `generate_polygon_treatment.py` (script de consola, usa imports implícitos) quedó con
   `QMetaType` — en la consola de QGIS 4 debería estar disponible; verificar.
5. `algorithm_scraps.py` no se importa desde ningún lado (archivo de retazos) — se convirtieron
   sus enums igual, pero no necesita más trabajo.
6. Eventualmente regenerar `assets/resources.py` con la tooling Qt6 (por ahora basta el
   import `qgis.PyQt`; el formato binario rcc v2 carga bien en Qt6).
7. Revisar el nuevo escaneo de seguridad obligatorio del repo de plugins antes de publicar.
