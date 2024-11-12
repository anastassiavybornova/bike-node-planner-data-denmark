import os
import yaml
import geopandas as gpd
from src import utils

### READ CONFIG FILES ### 

# general configs
config = yaml.load(open("../config/config.yml"), Loader=yaml.FullLoader)
proj_crs = config["proj_crs"]

# municipalities
municipalities = yaml.load(
    open("../config/config-municipalities.yml"), Loader=yaml.FullLoader
)
codes = municipalities["kommunekode"]

# GeoFA configs
config_geofa = yaml.load(open("../config/config-geofa-download.yml"), Loader=yaml.FullLoader)
wfs_version = config_geofa["geofa_wfs_version"]
node_layer_name = config_geofa["geofa_nodes_layer_name"]
stretches_layer_name = config_geofa["geofa_stretches_layer_name"]

### CREATE SUBFOLDERS ###

# make folders
sub_folders = [
    "../data/network-communication/geofa/",
    "../data/network-technical/geofa/"
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

### CREATE STUDY AREA POLYGON ###

### read in municipality boundaries & create study area polygon
gdf = gpd.read_file("../data/municipality-boundaries/municipality-boundaries.gpkg")
gdf = gdf.to_crs(proj_crs)  # make sure we have the right projected CRS
gdf = gdf[
    gdf["kommunekode"].isin(codes)
]  # filter to municipality codes indicated in config file

study_poly = gdf.union_all()
gdf_studyarea = gpd.GeoDataFrame({"geometry": [study_poly]}, crs=proj_crs)
# gdf_studyarea.to_file(
#     filename="../input-for-bike-node-planner/studyarea/studyarea.gpkg", index=False
# ) # not saving to file here

names = list(gdf["navn"])
print(f"Study area polygon created for municipalities: {names}...")

# Fetch input data from GeoFA (raw data)

url_knudepunkter = f"https://geofa.geodanmark.dk/ows/fkg/fkg/?request=GetFeature&typename={node_layer_name}&service=WFS&version={wfs_version}"
url_straekninger = f"https://geofa.geodanmark.dk/ows/fkg/fkg/?request=GetFeature&typename={stretches_layer_name}&service=WFS&version={wfs_version}"

try:
    knudepunkter = gpd.read_file(url_knudepunkter)
    straekninger = gpd.read_file(url_straekninger)
    print("GeoFA data fetched successfully.")
except:
    print("Error when fetching GeoFA data. Exiting... Please rerun the script!")
    exit()

assert len(knudepunkter) > 0, "No nodes found"
assert len(straekninger) > 0, "No stretches found"

# limit to extent of study area
assert (
    straekninger.crs == gdf_studyarea.crs
), "Crs of straekninger does not match crs of study area"
assert (
    knudepunkter.crs == gdf_studyarea.crs
), "Crs of knudepunkter does not match crs of study area"

edges_studyarea = straekninger.sjoin(gdf_studyarea, predicate="intersects").copy()
edges_studyarea.drop(columns=["index_right"], inplace=True)
nodes_studyarea = knudepunkter.clip(edges_studyarea.buffer(500).unary_union)

# remove empty geometries
edges_studyarea = edges_studyarea[edges_studyarea.geometry.notna()].reset_index(
    drop=True
)
nodes_studyarea = nodes_studyarea[nodes_studyarea.geometry.notna()].reset_index(
    drop=True
)

# assert there is one (and only one) LineString per edge geometry row
nodes_studyarea = nodes_studyarea.explode(index_parts=False).reset_index(drop=True)
assert all(
    nodes_studyarea.geometry.type == "Point"
), "Not all node geometries are Points"
assert all(nodes_studyarea.geometry.is_valid), "Not all node geometries are valid"

# assert there is one (and only one) Point per node geometry row
edges_studyarea = edges_studyarea.explode(index_parts=False).reset_index(drop=True)
assert all(
    edges_studyarea.geometry.type == "LineString"
), "Not all edge geometries are LineStrings"
assert all(edges_studyarea.geometry.is_valid), "Not all edge geometries are valid"

edges_studyarea.to_file(
    "../data/network-technical/edges.gpkg", index=False
)

nodes_studyarea.to_file(
    "../data/network-technical/nodes.gpkg", index=False
)

print("Raw data on nodes and edges for study area fetched from GeoFA and saved...")

# raw data saved to `network/raw`; simplified data (in next step) saved to `network/processed`