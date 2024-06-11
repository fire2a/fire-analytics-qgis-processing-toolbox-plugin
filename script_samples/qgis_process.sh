#!bash

# if using without a Desktop Environment (DE), for example via ssh
export QT_QPA_PLATFORM=offscreen

# sample command to run the fire2a:scar process
sourceFolder=~/InstanceDirectory/results
targetFolder=${sourceFolder}/processed
scarPolygon = ${targetFolder}scars.gpkg

qgis_process run fire2a:scar \ 
    --distance_units=meters --area_units=m2 --ellipsoid=EPSG:7030 \
    --BaseLayer=${sourceFolder}fuels.asc \
    --SampleScarFile=${targetFolder}Grids/Grids1/ForestGrid0.csv \
    --BurnProbability=TEMPORARY_OUTPUT \
    --ScarPolygon=${scarPolygon} \
    --ScarRaster=${targetFolder}scarRaster.tif
