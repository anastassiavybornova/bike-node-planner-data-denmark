### START MESSAGE ###
print("Starting to generate input data for BikeNodePlanner.")

### IMPORT LIBRARIES AND FUNCTIONS ###

# import libraries
import os
import shutil
import yaml
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString

### HELPER FUNCTIONS

def _drop_multiple_joins(joined_nodes):

    joined_nodes.reset_index(inplace=True)

    v = joined_nodes.edge_id.value_counts()
    grouped = joined_nodes[joined_nodes.edge_id.isin(v.index[v.gt(1)])].groupby(
        "edge_id"
    )

    drop_joined = []
    for edge_id, g in grouped:
        node_id = g.node_id.max()
        drop_joined.append((edge_id, node_id))

    for d in drop_joined:
        joined_nodes.drop(
            joined_nodes[
                (joined_nodes.edge_id == d[0]) & (joined_nodes.node_id == d[1])
            ].index,
            inplace=True,
        )

    return joined_nodes


def assign_edges_start_end_nodes(edges, nodes, max_distance=5):
    """
    Assign node ids of start and end nodes for edges in an edge geodataframe, based on the closest nodes in a node geodataframe

    Arguments:
        edges (gdf): network edges
        nodes (gdf): network nodes

    Returns:
        edges (gdf): edges with u column with start node id and v column with end node id
    """

    # Extract start and end coordinates of each linestring
    first_coord = edges.geometry.apply(lambda g: Point(g.coords[0]))
    last_coord = edges.geometry.apply(lambda g: Point(g.coords[-1]))

    # Add start and end as columns to the gdf
    edges["start_coord"] = first_coord
    edges["end_coord"] = last_coord

    start_coords = edges[["edge_id", "start_coord"]].copy()
    start_coords.set_geometry("start_coord", inplace=True, crs=edges.crs)

    end_coords = edges[["edge_id", "end_coord"]].copy()
    end_coords.set_geometry("end_coord", inplace=True, crs=edges.crs)

    # join start and end coors to nearest node
    start_joined = start_coords.sjoin_nearest(
        nodes[["geometry", "node_id"]],
        how="left",
        distance_col="distance",
        max_distance=max_distance,
    )
    end_joined = end_coords.sjoin_nearest(
        nodes[["geometry", "node_id"]],
        how="left",
        distance_col="distance",
        max_distance=max_distance,
    )
    start_joined = _drop_multiple_joins(start_joined)
    end_joined = _drop_multiple_joins(end_joined)

    assert len(start_joined) == len(edges)
    assert len(end_joined) == len(edges)

    edges.drop(["start_coord", "end_coord"], axis=1, inplace=True)

    # Merge with edges
    new_edges = edges.merge(
        start_joined[["edge_id", "node_id"]], left_on="edge_id", right_on="edge_id"
    )
    new_edges.rename({"node_id": "u"}, inplace=True, axis=1)

    new_edges = new_edges.merge(
        end_joined[["edge_id", "node_id"]], left_on="edge_id", right_on="edge_id"
    )
    new_edges.rename({"node_id": "v"}, inplace=True, axis=1)

    assert len(new_edges) == len(edges)

    return new_edges


def find_parallel_edges(edges):
    """
    Check for parallel edges in a pandas DataFrame with edges, including columns u with start node index and v with end node index.
    If two edges have the same u-v pair, the column 'key' is updated to ensure that the u-v-key combination can uniquely identify an edge.
    Note that (u,v) is not considered parallel to (v,u)

    Arguments:
        edges (gdf): network edges

    Returns:
        edges (gdf): edges with updated key index
    """

    # Find edges with duplicate node pairs
    parallel = edges[edges.duplicated(subset=["u", "v"])]

    edges.loc[parallel.index, "key"] = 1  # Set keys to 1

    k = 1

    while len(edges[edges.duplicated(subset=["u", "v", "key"])]) > 0:
        k += 1

        parallel = edges[edges.duplicated(subset=["u", "v", "key"])]

        edges.loc[parallel.index, "key"] = k  # Set keys to 1

    assert (
        len(edges[edges.duplicated(subset=["u", "v", "key"])]) == 0
    ), "Edges not uniquely indexed by u,v,key!"

    edges["key"].fillna(0, inplace=True)

    return edges


def order_edge_nodes(gdf):

    # gdf = gdf[gdf.u.notna() & gdf.v.notna()]

    for index, row in gdf[gdf.u.notna() & gdf.v.notna()].iterrows():
        org_u = row.u
        org_v = row.v

        gdf.loc[index, "u"] = min(org_u, org_v)
        gdf.loc[index, "v"] = max(org_u, org_v)

    return gdf

# define helper function to clean data folders
def remove_output_data(output_folders, remove_previous_output: bool = False, verbose: bool = False):

    if remove_previous_output:
        for f in output_folders:
            if os.path.exists(f):
                shutil.rmtree(f)

                os.makedirs(f)
    if verbose:
        print("Data folder cleaned...")

print("Libraries and functions imported...")

### IMPORT CONFIGURATIONS ###

# read config files
config = yaml.load(
    open("../config.yml"), 
    Loader=yaml.FullLoader)
proj_crs = config["proj_crs"]
wfs_version = config["geofa_wfs_version"]
node_layer_name = config["geofa_nodes_layer_name"]
stretches_layer_name = config["geofa_stretches_layer_name"]

municipalities = yaml.load(
    open("../config-municipalities.yml"), 
    Loader=yaml.FullLoader)
codes = municipalities["kommunekode"]

geomtypes = ["point", "linestring", "polygon"]
config_layers = {}
for geomtype in geomtypes:
    config_layers[geomtype] = yaml.load(
        open(f"../config-layers-{geomtype}.yml"), 
        Loader=yaml.FullLoader)
    
print("Configurations imported...")

### CREATE SUBFOLDERS ###

# make folders
main_folder = "../input-for-bike-node-planner/"
os.makedirs(main_folder, exist_ok=True)

sub_folders = [
    "dem",
    "elevation",
    "linestring",
    "network",
    "point",
    "polygon",
    "studyarea"
]

for sub_folder in sub_folders:
    os.makedirs(main_folder + sub_folder, exist_ok=True)

print("Subfolders created...")

### CLEAN DATA FOLDER ###

# remove previous output
remove_output_data(
    [
        "../data/dem",
        "../input-for-bike-node-planner/dem",
        "../input-for-bike-node-planner/elevation",
        "../input-for-bike-node-planner/linestring/",
        "../input-for-bike-node-planner/network/",
        "../input-for-bike-node-planner/point/",
        "../input-for-bike-node-planner/polygon/",
        "../input-for-bike-node-planner/studyarea/"        
    ],
    remove_previous_output=True,
    verbose=True
)

### CREATE STUDY AREA POLYGON ###

### read in municipality boundaries & create study area polygon
gdf = gpd.read_file("../data/municipality-boundaries/municipality-boundaries.gpkg")
gdf = gdf.to_crs(proj_crs) # make sure we have the right projected CRS
gdf = gdf[gdf["kommunekode"].isin(codes)] # filter to municipality codes indicated in config file

gdf_studyarea = gpd.GeoDataFrame(
    {
        "geometry": [gdf.unary_union]
    },
    crs = proj_crs
)
gdf_studyarea.to_file(
    filename = "../input-for-bike-node-planner/studyarea/studyarea.gpkg", 
    index = False)
print(f"Study area polygon created for municipalities: {codes}...")
del gdf

### FETCH AND SAVE RAW NETWORK DATA FROM GEOFA ###

# Fetch input data from GeoFA (raw data)

url = f"https://geofa.geodanmark.dk/ows/fkg/fkg/?request=GetFeature&typename={node_layer_name}&service=WFS&version={wfs_version}"

knudepunkter = gpd.read_file(url)

url = f"https://geofa.geodanmark.dk/ows/fkg/fkg/?request=GetFeature&typename={stretches_layer_name}&service=WFS&version={wfs_version}"

straekninger = gpd.read_file(url)

assert len(knudepunkter) > 0, "No nodes found"
assert len(straekninger) > 0, "No stretches found"

# limit to extent of study area
assert straekninger.crs == gdf_studyarea.crs
assert knudepunkter.crs == gdf_studyarea.crs

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
assert all(nodes_studyarea.geometry.type == "Point")
assert all(nodes_studyarea.geometry.is_valid)

# assert there is one (and only one) Point per node geometry row
edges_studyarea = edges_studyarea.explode(index_parts=False).reset_index(drop=True)
assert all(edges_studyarea.geometry.type == "LineString")
assert all(edges_studyarea.geometry.is_valid)

# save
os.makedirs(
    "../input-for-bike-node-planner/network/raw/", 
    exist_ok = True
)

edges_studyarea.to_file(
    "../input-for-bike-node-planner/network/raw/edges.gpkg", index=False
)

nodes_studyarea.to_file(
    "../input-for-bike-node-planner/network/raw/nodes.gpkg", index=False
)

print("Raw data on nodes and edges for study area fetched and saved...")

### PROCESS (CLEAN) AND SAVE NETWORK DATA ###

edges_studyarea["edge_id"] = edges_studyarea.id_cykelknudepunktsstraekning
assert len(edges_studyarea) == len(edges_studyarea["edge_id"].unique())

nodes_studyarea["node_id"] = nodes_studyarea.id_cykelknudepkt
assert len(nodes_studyarea) == len(nodes_studyarea["node_id"].unique())

processed_edges = assign_edges_start_end_nodes(edges_studyarea, nodes_studyarea)

processed_edges = order_edge_nodes(processed_edges)

processed_edges = find_parallel_edges(processed_edges)

assert len(processed_edges) == len(edges_studyarea)

processed_nodes = nodes_studyarea.loc[
    nodes_studyarea["node_id"].isin(processed_edges["u"])
    | nodes_studyarea["node_id"].isin(processed_edges["v"])
]

# save to files
os.makedirs(
    "../input-for-bike-node-planner/network/processed/",
    exist_ok=True
)

processed_nodes.to_file(
    "../input-for-bike-node-planner/network/processed/nodes.gpkg", index=False
)

processed_edges.to_file(
    "../input-for-bike-node-planner/network/processed/edges.gpkg", index=False
)

print("Data on nodes and edges for study area processed and saved...")

### CREATE EVALUATION LAYERS ###

# create a dictionary of evaluation layers (based on config file inputs)

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
        for layer in (set(vdict.values())):
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
                        gdf = pd.concat(
                            [
                                gdf,
                                gdf_muni
                            ]
                        )

            # if at least one of the municipalities has data from this data source,
            # add it to final gdf
            if not gdf.empty:
                final_gdf = pd.concat(
                    [
                        final_gdf,
                        gdf[gdf["type"].isin(v)]
                    ]
                )

        # save evaluation layer to file, if not empty
        if not final_gdf.empty:
            final_gdf = final_gdf.reset_index(drop=True)
            final_gdf.to_file(
                f"../input-for-bike-node-planner/{geomtype}/{layername}.gpkg", 
                index = False
            )
            print("\t \t", f"{layername} layer saved")
        else:
            print("\t \t", f"No data found for {layername} layer")
    
print("Generation of evaluation layers ended successfully...")