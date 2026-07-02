# Estado migración QGIS 4 / Qt6 (actualizado 2026-06-16)

## Contexto
QGIS 4.0 "Norrköping" (marzo 2026) migró de Qt5 a Qt6 (PyQt5 → PyQt6) y rompió el plugin.
QGIS 4.2 LTR sale en octubre 2026 — deadline práctico.
Guía oficial: https://plugins.qgis.org/docs/migrate-qgis4

## Hecho (rama `feature/new-branch`, HEAD 6e66e2d)

- **234 enums convertidos a forma con scope completo** en 17 archivos, mapeados por
  introspección contra QGIS 3.44 local (scripts `qt6_enum_map.py` / `qt6_apply.py` en la raíz).
  Renames clave: `QgsProcessing.TypeRaster` → `Qgis.ProcessingSourceType.Raster`,
  `FlagAdvanced` → `Qgis.ProcessingParameterFlag.Advanced`,
  `QgsColorRampShader.Interpolated` → `Qgis.ShaderInterpolationMethod.Linear`,
  `QgsUnitTypes.DistanceMeters` → `Qgis.DistanceUnit.Meters`.
- `QVariant.Int/.String/.Bool/.Double` → `QMetaType.Type.*` (QVariant.Type no existe en PyQt6).
- `row[j] != QVariant()` → `!= NULL` (de qgis.core) en algorithm_clusterize.py y algorithm_knapsack.py.
- Imports `PyQt5` directos → `qgis.PyQt` (algorithm_clusterize.py, assets/resources.py).
- `qmb.exec_()` → `qmb.exec()` en dependencies_handler.py.
- Imports `Qgis`/`QMetaType`/`NULL` agregados donde faltaban; `QVariant` huérfanos removidos.
- `metadata.txt`: `qgisMinimumVersion` 3.34 → **3.40**, `qgisMaximumVersion=4.99`, changelog v1.1.0.
- Líneas >120 alargadas por los renames: **envueltas** (commit 7ccc70e).
- **`QProcess.pid()` → `processId()`** (commit 6e66e2d). Método REMOVIDO en Qt6 — lo detectó
  Felipe corriendo el simulador en QGIS 4. Lección: Qt6 también remueve/renombra MÉTODOS y
  señales, no solo enums; los enum-sweeps no los atrapan y fallan solo en runtime.

## Verificado

- Compila OK; provider carga con **24 algoritmos / 193 parámetros** (QGIS 3.44 local).
- **QGIS 4.0.3 / Qt 6.11 real (Felipe, Windows)**: plugin carga, algoritmos abren,
  simulador corre y lanza el binario. (El fix de pid() salió de aquí.)
- **Barrido completo de APIs Qt5 removidas/renombradas en Qt6** — todo limpio:
  QProcess.pid (corregido), QFontMetrics.width, QDesktopWidget/.desktop(), QRegExp,
  qrand/qsrand, QTextCodec/setCodec, Qt.MidButton, toTime_t, QSignalMapper.mapped,
  QWheelEvent.delta, exec_(), setResizeMode, toAscii.
- `QgsField(type=QMetaType.Type.*)` construye OK en keyword y posicional (rutas de
  creación de campos: knapsack, treatment, postsimulation, deprecated).

## Releases
- `v1.1.0-beta1` (publicado) — **tiene el bug de pid(), NO usar**.
- `v1.1.0-beta2` (publicado, pre-release) — con el fix. ZIP con binarios todas plataformas.
- Se generan solos vía CI (`release.yml`) al empujar un tag `vX.Y.Z[-sufijo]`. Los binarios
  (Cell2Fire de fire2a/C2F-W + CBC de coin-or/Cbc) NO viven en git: CI los baja al taggear.

## Pendiente

1. **Confirmación end-to-end de Felipe con beta2**: que la simulación corra completa y
   cargue resultados en QGIS 4. Si aparece otro error de runtime Qt6, mismo patrón: traza → fix → beta3.
2. Correr la suite `test/` (requiere pytest-qgis; son tests de integración pesada: descargan
   datos + corren binario). No corrida.
3. `assets/resources.py`: por ahora basta el import `qgis.PyQt` (el rcc v2 carga en Qt6);
   regenerar con tooling Qt6 es opcional.
4. Revisar el escaneo de seguridad obligatorio del repo oficial de plugins antes de publicar la final.
5. Merge de `feature/new-branch` → `main` y release final `v1.1.0` cuando Felipe dé el OK.
