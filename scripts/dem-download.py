# based on https://geoscripting-wur.github.io/PythonRaster/

# %%
from owslib.wcs import WebCoverageService
import os
import geopandas as gpd
import numpy as np
import yaml
from shapely.geometry import Polygon

# load configs
configs = yaml.load(open("../config/config.yml"), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]
datafordeler_username = configs["datafordeler_username"]
datafordeler_password = configs["datafordeler_password"]

studyarea_fp = "../input-for-bike-node-planner/studyarea/studyarea.gpkg"

wcs_url = f"https://services.datafordeler.dk/DHMNedboer/dhm_wcs/1.0.0/WCS?username={datafordeler_username}&password={datafordeler_password}&service=WCS&request=GetCapabilities"

dem_intermediate_folder = "../data/DEM"

if not os.path.exists(dem_intermediate_folder):
    os.mkdir(dem_intermediate_folder)

sa = gpd.read_file(studyarea_fp)
assert sa.crs == proj_crs

# %%
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

assert width < 10000  # max size allowed
assert height < 10000

xmin, ymin, xmax, ymax = sa.total_bounds

cols = list(np.arange(xmin, xmax + size, size))
rows = list(np.arange(ymin, ymax + size, size))
bboxes = []

for x in cols:
    for y in rows:
        box = (x, y, x + size, y + size)
        bboxes.append(box)

assert len(bboxes) == len(cols) * len(rows)

# %%
# make sure that no bboxes are outside of the main bounding box for the data set

# get the bounding box of the data set
lon_min, lat_min, lon_max, lat_max = wcs["dhm_terraen"].boundingBoxWGS84

bbox_limit_gdf = gpd.GeoDataFrame(
    geometry=[
        Polygon(
            [
                (lon_min, lat_min),
                (lon_max, lat_min),
                (lon_max, lat_max),
                (lon_min, lat_max),
            ]
        )
    ],
    crs="EPSG:4326",
)
bbox_limit_gdf.to_crs(proj_crs, inplace=True)

# check that none of the bboxes are outside of the bounding box
valid_bboxes = []
for i, bbox in enumerate(bboxes):
    bbox_gdf = gpd.GeoDataFrame(
        geometry=[
            Polygon(
                [
                    (bbox[0], bbox[1]),
                    (bbox[2], bbox[1]),
                    (bbox[2], bbox[3]),
                    (bbox[0], bbox[3]),
                ]
            )
        ],
        crs=proj_crs,
    )
    if bbox_gdf.within(bbox_limit_gdf.geometry[0]).all():
        valid_bboxes.append(bbox)

bboxes = valid_bboxes

# %%

while True:
    try:
        for i, bbox in enumerate(bboxes):
            try:
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
                    timeout=120,
                )

                with open(
                    dem_intermediate_folder + f"/{coverage_name}_{i}.tif", "wb"
                ) as file:
                    file.write(response.read())

            except Exception as e:
                print(f"Error with bbox {bbox}: {e}")
                print(f"Skipping bbox {i}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # print("Finished processing all bboxes.")
        break

# %%
