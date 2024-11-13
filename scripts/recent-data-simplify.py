import os
import yaml
import sgeop
import geopandas as gpd
from src import utils

### READ GENERAL CONFIGS ###
config = yaml.load(open("./config/config.yml"), Loader=yaml.FullLoader)
proj_crs = config["proj_crs"]

### CREATE SUBFOLDERS ###
sub_folders = [
    "./data/network-communication/geofa/",
]

for sub_folder in sub_folders:
    os.makedirs(sub_folder, exist_ok=True)

print("Subfolders created...")

### CLEAN DATA FOLDER ###

# remove previous output
utils.remove_output_data(
    sub_folders,
    remove_previous_output=True,
    verbose=True,
)

### READ (TECHNICAL) EDGE DATA ###

edges = gpd.read_file(
    "./data/network-technical/geofa/cykelknudepunktsstraekninger.gpkg"
)

### preprocess edges for sgeop input ###
edges = edges[["geometry"]]
edges = edges.to_crs(proj_crs)
edges = gpd.GeoDataFrame(
    {
        "geometry": edges.geometry.explode()
    },
    crs = proj_crs
)
# removing duplicated and overlapping geoms
edges = edges[~edges.geometry.duplicated()].reset_index(drop=True)
edges_union = edges.union_all()
edge_geoms = [g for g in edges_union.geoms]
edges = gpd.GeoDataFrame(
    {
        "geometry": edge_geoms,
    },
    crs = proj_crs
)

print("Edges read in and preprocessed.")

# simplify
print("Simplifying network...")
edges_simp = sgeop.simplify_network(
    roads=edges,
    artifact_threshold=12 # set manually!
)

# save to file
print("Saving to file...")
edges_simp.to_file(
    "./data/network-communication/geofa/edges.gpkg"
)

print("Done!")