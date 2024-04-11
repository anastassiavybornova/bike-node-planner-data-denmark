### DOWNLOAD AND MERGE ELEVATION DATA ###

# import libraries
import os
import yaml
import geopandas as gpd
import numpy as np

from pathlib import Path

from owslib.wcs import WebCoverageService
from osgeo import gdal

gdal.UseExceptions()

# start download workflow
print(
    "Downloading and merging elevation data. This can take up to several minutes per municipality."
)
# based on https://geoscripting-wur.github.io/PythonRaster/

# load configs
configs = yaml.load(open("../config.yml"), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]
datafordeler_username = configs["datafordeler_username"]
datafordeler_password = configs["datafordeler_password"]

studyarea_fp = "../input-for-bike-node-planner/studyarea/studyarea.gpkg"

wcs_url = f"https://services.datafordeler.dk/DHMNedboer/dhm_wcs/1.0.0/WCS?username={datafordeler_username}&password={datafordeler_password}&service=WCS&request=GetCapabilities"

dem_intermediate_folder = "../data/DEM"

if not os.path.exists(dem_intermediate_folder):
    os.mkdir(dem_intermediate_folder)

sa = gpd.read_file(studyarea_fp)
assert sa.crs == proj_crs, "Study area crs must be the same as the project crs"

# Access the WCS by proving the url and optional arguments
wcs = WebCoverageService(
    "https://services.datafordeler.dk/DHMNedboer/dhm_wcs/1.0.0/WCS?username=MAKKFGPILT&password=Testing23!&service=WCS&request=GetCapabilities",
    version="1.0.0",
)

coverage_name = "dhm_terraen"

size = 5000  # dimensions km
resx = 10  # pixel size
resy = 10
width = int(size / resx)  # dimensions of tif
height = int(size / resy)

assert width < 10000, "width is too large"  # max size allowed
assert height < 10000, "height is too large"  # max size allowed

xmin, ymin, xmax, ymax = sa.total_bounds

cols = list(np.arange(xmin, xmax + size, size))
rows = list(np.arange(ymin, ymax + size, size))
bboxes = []

for x in cols:
    for y in rows:
        box = (x, y, x + size, y + size)
        bboxes.append(box)

assert len(bboxes) == len(cols) * len(rows), "Error in generation of bounding boxes"


try:
    for i, bbox in enumerate(bboxes):
        # Request the DSM data from the WCS
        response = wcs.getCoverage(
            identifier=coverage_name,
            bbox=bbox,
            format="GTiff",
            crs=f"urn:ogc:def:crs:{proj_crs}",
            resx=0.4,
            resy=0.4,
            width=width,
            height=height,
        )

        with open(dem_intermediate_folder + f"/{coverage_name}_{i}.tif", "wb") as file:
            file.write(response.read())

except:
    i = i - 1

    for i, bbox in enumerate(bboxes[i:]):
        # Request the DSM data from the WCS
        response = wcs.getCoverage(
            identifier=coverage_name,
            bbox=bbox,
            format="GTiff",
            crs=f"urn:ogc:def:crs:{proj_crs}",
            resx=0.4,
            resy=0.4,
            width=width,
            height=height,
        )

        with open(dem_intermediate_folder + f"/{coverage_name}_{i}.tif", "wb") as file:
            file.write(response.read())

print("\t Elevation data downloaded...")
print("\t Merging data...")

# from https://www.giscourse.com/automatically-merge-raster-files-using-pyqgis/
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

print("Elevation data ready...")
