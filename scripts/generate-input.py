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
wfs_version = config["geofa_wfs_version"]
node_layer_name = config["geofa_nodes_layer_name"]
stretches_layer_name = config["geofa_stretches_layer_name"]
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

    # # Fetch input data from GeoFA (raw data)

    # url_knudepunkter = f"https://geofa.geodanmark.dk/ows/fkg/fkg/?request=GetFeature&typename={node_layer_name}&service=WFS&version={wfs_version}"
    # url_straekninger = f"https://geofa.geodanmark.dk/ows/fkg/fkg/?request=GetFeature&typename={stretches_layer_name}&service=WFS&version={wfs_version}"

    # try:
    #     knudepunkter = gpd.read_file(url_knudepunkter)
    #     straekninger = gpd.read_file(url_straekninger)
    #     print("GeoFA data fetched successfully.")
    # except:
    #     print("Error when fetching GeoFA data. Exiting... Please rerun the script!")
    #     exit()

    # assert len(knudepunkter) > 0, "No nodes found"
    # assert len(straekninger) > 0, "No stretches found"

    # # limit to extent of study area
    # assert (
    #     straekninger.crs == gdf_studyarea.crs
    # ), "Crs of straekninger does not match crs of study area"
    # assert (
    #     knudepunkter.crs == gdf_studyarea.crs
    # ), "Crs of knudepunkter does not match crs of study area"

    # edges_studyarea = straekninger.sjoin(gdf_studyarea, predicate="intersects").copy()
    # edges_studyarea.drop(columns=["index_right"], inplace=True)
    # nodes_studyarea = knudepunkter.clip(edges_studyarea.buffer(500).unary_union)

    # # remove empty geometries
    # edges_studyarea = edges_studyarea[edges_studyarea.geometry.notna()].reset_index(
    #     drop=True
    # )
    # nodes_studyarea = nodes_studyarea[nodes_studyarea.geometry.notna()].reset_index(
    #     drop=True
    # )

    # # assert there is one (and only one) LineString per edge geometry row
    # nodes_studyarea = nodes_studyarea.explode(index_parts=False).reset_index(drop=True)
    # assert all(
    #     nodes_studyarea.geometry.type == "Point"
    # ), "Not all node geometries are Points"
    # assert all(nodes_studyarea.geometry.is_valid), "Not all node geometries are valid"

    # # assert there is one (and only one) Point per node geometry row
    # edges_studyarea = edges_studyarea.explode(index_parts=False).reset_index(drop=True)
    # assert all(
    #     edges_studyarea.geometry.type == "LineString"
    # ), "Not all edge geometries are LineStrings"
    # assert all(edges_studyarea.geometry.is_valid), "Not all edge geometries are valid"

    # # save
    # os.makedirs("../input-for-bike-node-planner/network/raw/", exist_ok=True)

    # edges_studyarea.to_file(
    #     "../input-for-bike-node-planner/network/raw/edges.gpkg", index=False
    # )

    # nodes_studyarea.to_file(
    #     "../input-for-bike-node-planner/network/raw/nodes.gpkg", index=False
    # )

    # print("Raw data on nodes and edges for study area fetched from GeoFA and saved...")

    # # TODO (FR) add here the simplification step on municipality level (feature request)
    # # will replace processing step below.
    # # raw data saved to `network/raw`; simplified data saved to `network/processed`

    # edges_studyarea["edge_id"] = edges_studyarea.id_cykelknudepunktsstraekning
    # assert len(edges_studyarea) == len(
    #     edges_studyarea["edge_id"].unique()
    # ), "Edge ids are not unique"

    # nodes_studyarea["node_id"] = nodes_studyarea.id_cykelknudepkt
    # assert len(nodes_studyarea) == len(
    #     nodes_studyarea["node_id"].unique()
    # ), "Node ids are not unique"

    # processed_edges = utils.assign_edges_start_end_nodes(edges_studyarea, nodes_studyarea)

    # processed_edges = utils.order_edge_nodes(processed_edges)

    # processed_edges = utils.find_parallel_edges(processed_edges)

    # assert len(processed_edges) == len(
    #     edges_studyarea
    # ), "The number of edges has changed (processed_edges not same length as edges_studyarea)"

    # processed_nodes = nodes_studyarea.loc[
    #     nodes_studyarea["node_id"].isin(processed_edges["u"])
    #     | nodes_studyarea["node_id"].isin(processed_edges["v"])
    # ]

    # # save to files
    # os.makedirs("../input-for-bike-node-planner/network/processed/", exist_ok=True)

    # processed_nodes.to_file(
    #     "../input-for-bike-node-planner/network/processed/nodes.gpkg", index=False
    # )

    # processed_edges.to_file(
    #     "../input-for-bike-node-planner/network/processed/edges.gpkg", index=False
    # )

    # print("Data on nodes and edges for study area processed and saved...")
    print("GeoFA data fetching not implemented yet")
    exit()

else:

    # create directoriy for saving
    os.makedirs("../input-for-bike-node-planner/network/processed/", exist_ok=True)

    ### network edges
    print("Generating network edges...")
    # read in all available edges for DK (already simplified)
    edges_all = gpd.read_file("../data/network-communication/edges.gpkg")

    # get only edges that intersect study area
    edges = edges_all.loc[edges_all.sindex.query(study_poly, predicate="intersects")].copy().reset_index(drop=True)

    # keep only relevant (geometry) colum
    edges = edges[["geometry"]]

    # # add unique edge ID (index) # TODO: do we need this?
    # edges["edge_id"] = edges.index

    # derive nodes & node IDs of edges through momepy
    G = momepy.gdf_to_nx(edges)
    nodes, edges = momepy.nx_to_gdf(G)

    edges.to_file(
        "../input-for-bike-node-planner/network/processed/edges.gpkg", index=False
    )
    
    print("Network edges generated and saved.")

    ### network nodes

    # add "raw node" ID to node gdf
    nodes_raw = gpd.read_file(f"../data/network-technical/cykelknudepunkter/cykelknudepunkter.gpkg")
    nodes_raw = nodes_raw.explode()
    nodes_raw = nodes_raw.to_crs(proj_crs)

    assert nodes.crs == nodes_raw.crs
    
    # for each node in raw data set, find the nearest node in simplified data set
    nodes_raw["node_id"] = nodes_raw.apply(lambda x: nodes.sindex.nearest(x.geometry)[1][0], axis = 1)
    d = {}
    for n, group in nodes_raw.groupby("node_id"):
        d[n] = list(group["id_cykelknudepkt"]) 

    id_cykelknudepkt = []
    for nodeID in nodes.nodeID:
        if nodeID in d:
            id_cykelknudepkt.append(d[nodeID])
        else:
            id_cykelknudepkt.append(None)

    nodes["id_cykelknudepkt"] = id_cykelknudepkt

    nodes.to_file(
        "../input-for-bike-node-planner/network/processed/nodes.gpkg",
        index=False
    )

    # save raw nodes for this area
    raw_node_ids = [item for sublist in d.values() for item in sublist]
    nodes_raw_studyarea = nodes_raw[nodes_raw.id_cykelknudepkt.isin(raw_node_ids)].copy().reset_index(drop=True)
    nodes_raw_studyarea.to_file(
        "../input-for-bike-node-planner/network/processed/nodes_raw.gpkg",
        index=False
    )

    print("Network nodes generated and saved.")
    

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