### START MESSAGE ###
print("Starting to generate input data for BikeNodePlanner.")

### IMPORT LIBRARIES AND FUNCTIONS ###

# import libraries
import os
import yaml
import geopandas as gpd
import pandas as pd
import warnings
import momepy
from src import utils

warnings.filterwarnings("ignore")

### HELPER FUNCTIONS

print("Libraries and functions imported...")

### IMPORT CONFIGURATIONS ###

# read config files
config = yaml.load(open("../config/config.yml"), Loader=yaml.FullLoader)
proj_crs = config["proj_crs"]
geofa = bool(config["geofa"])

municipalities = yaml.load(
    open("../config/config-municipalities.yml"), Loader=yaml.FullLoader
)

codes = municipalities["kommunekode"]

geomtypes = [
    "point",
    # "linestring", # TODO
    "polygon",
]

config_layers = {}
for geomtype in geomtypes:
    config_layers[geomtype] = yaml.load(
        open(f"../config/config-layers-{geomtype}.yml"), Loader=yaml.FullLoader
    )

print("Configurations imported...")

### CREATE SUBFOLDERS ###

# make folders
main_folder = "../input-for-bike-node-planner/"
os.makedirs(main_folder, exist_ok=True)

sub_folders = [
    "dem",
    # "linestring", # TODO
    "network",
    "point",
    "polygon",
    "studyarea",
]

for sub_folder in sub_folders:
    os.makedirs(main_folder + sub_folder, exist_ok=True)

print("Subfolders created...")

### CLEAN DATA FOLDER ###

# remove previous output
utils.remove_output_data(
    [
        "../data/dem",
        "../input-for-bike-node-planner/dem",
        # "../input-for-bike-node-planner/linestring/", # TODO
        "../input-for-bike-node-planner/network/",
        "../input-for-bike-node-planner/point/",
        "../input-for-bike-node-planner/polygon/",
        "../input-for-bike-node-planner/studyarea/",
    ],
    remove_previous_output=True,
    verbose=True,
)

### CREATE NETWORK FOLDERS ###
os.makedirs("../input-for-bike-node-planner/network/raw/", exist_ok=True)
os.makedirs("../input-for-bike-node-planner/network/processed/", exist_ok=True)

### CREATE STUDY AREA POLYGON ###

### read in municipality boundaries & create study area polygon
gdf = gpd.read_file("../data/municipality-boundaries/municipality-boundaries.gpkg")
gdf = gdf.to_crs(proj_crs)  # make sure we have the right projected CRS
gdf = gdf[
    gdf["kommunekode"].isin(codes)
]  # filter to municipality codes indicated in config file

study_poly = gdf.union_all()
gdf_studyarea = gpd.GeoDataFrame({"geometry": [study_poly]}, crs=proj_crs)
gdf_studyarea.to_file(
    filename="../input-for-bike-node-planner/studyarea/studyarea.gpkg", index=False
)

names = list(gdf["navn"])
print(f"Study area polygon created for municipalities: {names}...")

del gdf

### FETCH AND SAVE RAW NETWORK DATA FROM GEOFA ###
if geofa:
    mydatasource = "geofa"
else:
    mydatasource = "bikenodeplanner"

utils.get_edges_and_nodes(
    datasource=mydatasource,
    proj_crs=proj_crs,
    study_poly=study_poly,
    gdf_studyarea=gdf_studyarea,
)

### CREATE EVALUATION LAYERS ###

# create a dictionary of evaluation layers (based on config file inputs)

print("Reading in evaluation layer configurations")

layer_dict = {}

for geomtype in geomtypes:

    layer_dict[geomtype] = {}

    # determine evaluation layers
    layers = []
    for v in config_layers[geomtype].values():
        layers += list(set(v.values()))
    layers = list(set(layers))

    # determine data sets that go into each layer

    # key is name of merged output layer, value is a dict
    for layer in layers:
        layer_dict[geomtype][layer] = {}

    # adding data source as key to dictindict IF relevant to layer
    for datasource, vdict in config_layers[geomtype].items():
        for layer in set(vdict.values()):
            layer_dict[geomtype][layer][datasource] = []

    for datasource, vdict in config_layers[geomtype].items():
        for k, v in vdict.items():
            layer_dict[geomtype][v][datasource] += [k]

for geomtype in geomtypes:
    if "ignore" in layer_dict[geomtype]:
        del layer_dict[geomtype]["ignore"]

# for each layer type (point/linestring/polygon),

print("Generation of evaluation layers started...")

for geomtype in geomtypes:

    # go through all evaluation layers for that geomtype...
    for layername, datadict in layer_dict[geomtype].items():

        final_gdf = gpd.GeoDataFrame()

        # go through each data source for that evaluation layer...
        for k, v in datadict.items():

            gdf = gpd.GeoDataFrame()

            # and fetch it for each municipality
            for code in codes:
                # for each code, check if file exists, if yes: read it in, if not empty: concatenate
                fp = f"../data/{geomtype}/{code}/{k}.gpkg"
                if os.path.exists(fp):
                    gdf_muni = gpd.read_file(fp)
                    if not gdf_muni.empty:
                        gdf = pd.concat([gdf, gdf_muni])

            # if at least one of the municipalities has data from this data source,
            # add it to final gdf
            if not gdf.empty:
                final_gdf = pd.concat([final_gdf, gdf[gdf["type"].isin(v)]])

        # save evaluation layer to file, if not empty
        if not final_gdf.empty:
            final_gdf = final_gdf.reset_index(drop=True)
            final_gdf.to_file(
                f"../input-for-bike-node-planner/{geomtype}/{layername}.gpkg",
                index=False,
            )
            print("\t \t", f"{layername} layer saved")
        else:
            print("\t \t", f"No data found for {layername} layer")

print("Generation of evaluation layers ended successfully...")
