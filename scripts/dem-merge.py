# from https://www.giscourse.com/automatically-merge-raster-files-using-pyqgis/
from pathlib import Path
from osgeo import gdal
import os
import yaml

gdal.UseExceptions()

os.environ["PROJ_LIB"] = "/Applications/QGIS-LTR.app/Contents/Resources/proj"

# load configs
configs = yaml.load(open("../config/config.yml"), Loader=yaml.FullLoader)

dem_output_folder = "../input-for-bike-node-planner/dem"

if not os.path.exists(dem_output_folder):
    os.mkdir(dem_output_folder)

# input rasters
input_path = f"../data/dem/"

output_path = dem_output_folder + "/dem.tif"

folder = Path(input_path)

l = []

for f in folder.glob("**/*.tif"):
    f_path = f.as_posix()
    l.append(f_path)

vrt_path = os.path.join(input_path, "prov_vrt.vrt")
vrt = gdal.BuildVRT(vrt_path, l)

gdal.Translate(output_path, vrt, format="GTiff")