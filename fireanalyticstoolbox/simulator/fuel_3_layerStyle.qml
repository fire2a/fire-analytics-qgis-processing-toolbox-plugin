<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.40.0-Bratislava" styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|Diagrams|GeometryOptions|Relations|Legend">
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" name="name" value=""/>
      <Option name="properties"/>
      <Option type="QString" name="type" value="collection"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" zoomedInResamplingMethod="nearestNeighbour" maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer type="paletted" opacity="1" nodataColor="" band="1" alphaBand="-1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry color="#226633" label="GR3" alpha="255" value="213"/>
        <paletteEntry color="#700cf2" label="GR8" alpha="255" value="223"/>
        <paletteEntry color="#70a800" label="GR5" alpha="255" value="221"/>
        <paletteEntry color="#83c795" label="GR4" alpha="255" value="211"/>
        <paletteEntry color="#897044" label="GS2" alpha="255" value="226"/>
        <paletteEntry color="#ac66ed" label="GR7" alpha="255" value="227"/>
        <paletteEntry color="#ae017e" label="SH3" alpha="255" value="237"/>
        <paletteEntry color="#c4bd97" label="GS1" alpha="255" value="224"/>
        <paletteEntry color="#c4bd97" label="GS3" alpha="255" value="225"/>
        <paletteEntry color="#d1ff73" label="GR1" alpha="255" value="214"/>
        <paletteEntry color="#d1ff73" label="GR2" alpha="255" value="212"/>
        <paletteEntry color="#dfb8e6" label="GR6" alpha="255" value="222"/>
        <paletteEntry color="#e6e600" label="SH5" alpha="255" value="235"/>
        <paletteEntry color="#f768a1" label="SH2" alpha="255" value="233"/>
        <paletteEntry color="#fbbeb9" label="GS4" alpha="255" value="234"/>
        <paletteEntry color="#ffaa00" label="SH7" alpha="255" value="231"/>
        <paletteEntry color="#ffd37f" label="SH6" alpha="255" value="232"/>
        <paletteEntry color="#ffffbe" label="SH4" alpha="255" value="236"/>
        <paletteEntry color="#ffffff" label="Non-fuel" alpha="255" value="0"/>
      </colorPalette>
      <colorramp type="randomcolors" name="[source]">
        <Option/>
      </colorramp>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation saturation="0" colorizeRed="255" colorizeGreen="128" invertColors="0" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
