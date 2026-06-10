#!/usr/bin/env python3
"""Apply Qt6/QGIS4 scoped-enum replacements to plugin sources."""
import re
from pathlib import Path

MAPPING = {
    "QImage.Format_ARGB32_Premultiplied": "QImage.Format.Format_ARGB32_Premultiplied",
    "QImage.Format_ARGB32": "QImage.Format.Format_ARGB32",
    "QMessageBox.No": "QMessageBox.StandardButton.No",
    "QMessageBox.Warning": "QMessageBox.Icon.Warning",
    "QMessageBox.Yes": "QMessageBox.StandardButton.Yes",
    "QProcess.CrashExit": "QProcess.ExitStatus.CrashExit",
    "QProcess.Crashed": "QProcess.ProcessError.Crashed",
    "QProcess.FailedToStart": "QProcess.ProcessError.FailedToStart",
    "QProcess.ForwardedInputChannel": "QProcess.InputChannelMode.ForwardedInputChannel",
    "QProcess.NormalExit": "QProcess.ExitStatus.NormalExit",
    "QProcess.NotRunning": "QProcess.ProcessState.NotRunning",
    "QProcess.ReadError": "QProcess.ProcessError.ReadError",
    "QProcess.Running": "QProcess.ProcessState.Running",
    "QProcess.SeparateChannels": "QProcess.ProcessChannelMode.SeparateChannels",
    "QProcess.Starting": "QProcess.ProcessState.Starting",
    "QProcess.Timedout": "QProcess.ProcessError.Timedout",
    "QProcess.UnknownError": "QProcess.ProcessError.UnknownError",
    "QProcess.WriteError": "QProcess.ProcessError.WriteError",
    # QVariant.Type does not exist in PyQt6 -> QMetaType.Type (accepted by QgsField since 3.38)
    "QVariant.Bool": "QMetaType.Type.Bool",
    "QVariant.Double": "QMetaType.Type.Double",
    "QVariant.Int": "QMetaType.Type.Int",
    "QVariant.String": "QMetaType.Type.QString",
    "Qgis.CInt16": "Qgis.DataType.CInt16",
    "Qgis.Critical": "Qgis.MessageLevel.Critical",
    "Qgis.Float32": "Qgis.DataType.Float32",
    "Qgis.Info": "Qgis.MessageLevel.Info",
    "Qgis.Int16": "Qgis.DataType.Int16",
    "Qgis.Success": "Qgis.MessageLevel.Success",
    "Qgis.Warning": "Qgis.MessageLevel.Warning",
    "QgsColorRampShader.Interpolated": "Qgis.ShaderInterpolationMethod.Linear",
    "QgsFeatureRequest.GeometrySkipInvalid": "Qgis.InvalidGeometryCheck.SkipInvalid",
    "QgsFeatureSink.FastInsert": "QgsFeatureSink.Flag.FastInsert",
    "QgsProcessing.TypeFile": "Qgis.ProcessingSourceType.File",
    "QgsProcessing.TypeRaster": "Qgis.ProcessingSourceType.Raster",
    "QgsProcessing.TypeVectorAnyGeometry": "Qgis.ProcessingSourceType.VectorAnyGeometry",
    "QgsProcessing.TypeVectorLine": "Qgis.ProcessingSourceType.VectorLine",
    "QgsProcessing.TypeVectorPoint": "Qgis.ProcessingSourceType.VectorPoint",
    "QgsProcessing.TypeVectorPolygon": "Qgis.ProcessingSourceType.VectorPolygon",
    "QgsProcessingParameterDateTime.Time": "Qgis.ProcessingDateTimeParameterDataType.Time",
    "QgsProcessingParameterDefinition.FlagAdvanced": "Qgis.ProcessingParameterFlag.Advanced",
    "QgsProcessingParameterField.Numeric": "Qgis.ProcessingFieldParameterDataType.Numeric",
    "QgsProcessingParameterField.String": "Qgis.ProcessingFieldParameterDataType.String",
    "QgsProcessingParameterFile.File": "Qgis.ProcessingFileParameterBehavior.File",
    "QgsProcessingParameterFile.Folder": "Qgis.ProcessingFileParameterBehavior.Folder",
    "QgsProcessingParameterNumber.Double": "Qgis.ProcessingNumberParameterType.Double",
    "QgsProcessingParameterNumber.Integer": "Qgis.ProcessingNumberParameterType.Integer",
    "QgsRasterBandStats.All": "Qgis.RasterBandStatistic.All",
    "QgsTask.Complete": "QgsTask.TaskStatus.Complete",
    "QgsTask.OnHold": "QgsTask.TaskStatus.OnHold",
    "QgsTask.Queued": "QgsTask.TaskStatus.Queued",
    "QgsTask.Running": "QgsTask.TaskStatus.Running",
    "QgsTask.Terminated": "QgsTask.TaskStatus.Terminated",
    "QgsUnitTypes.DistanceMeters": "Qgis.DistanceUnit.Meters",
    "QgsWkbTypes.MultiLineString": "Qgis.WkbType.MultiLineString",
    "QgsWkbTypes.Point": "Qgis.WkbType.Point",
}

patterns = [(re.compile(rf"\b{re.escape(old)}\b(?!\.)"), new) for old, new in MAPPING.items()]

changed = {}
for f in Path("fireanalyticstoolbox").rglob("*.py"):
    if f.name == "resources.py":
        continue
    text = orig = f.read_text()
    count = 0
    for pat, new in patterns:
        text, n = pat.subn(new, text)
        count += n
    if text != orig:
        f.write_text(text)
        changed[str(f)] = count

for f, n in sorted(changed.items()):
    print(f"{n:4d}  {f}")
print(f"total: {sum(changed.values())} replacements in {len(changed)} files")
