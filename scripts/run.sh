#!/bin/bash
$1 generate-input.py
export PROJ_LIB=$2 # point to QGIS' proj.db location
$1 -W ignore generate-elevation.py
echo "All done! Now you can copy-paste all subfolders of '/input-for-bike-node-planner/' into the '/data/input/' folder of bike-node-planner"