#!/bin/bash

### read in command-line arguments
while [ $# -gt 0 ]; do
    if [[ $1 == "--"* ]]; then
        v="${1/--/}"
        declare "$v"="$2"
        shift
    fi
    shift
done

echo "Running worflow with settings:"
echo "download_elevation: '$download_elevation'"
echo "python path: '$python_path'"
echo "proj.db fiona path: '$projdb_path'"

$python_path generate-input.py

export PROJ_LIB=$projdb_path # point to QGIS' proj.db location

if [ "$download_elevation" == "1" ] ; then 
    $python_path -W ignore generate-elevation.py
else 
    echo "Elevation data download was not requested. Please provide your own elevation raster."; 
fi

echo "All done! Now you can copy-paste all subfolders of '/input-for-bike-node-planner/' into the '/data/input/' folder of bike-node-planner"