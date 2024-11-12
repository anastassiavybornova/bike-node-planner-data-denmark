# insert simplification script here (python 310 or above, with sgeop)
# using data from data/network-technical/geofa/edges.gpkg (and -nodes.gpkg)


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
# print("GeoFA data fetching not implemented yet")
# exit()