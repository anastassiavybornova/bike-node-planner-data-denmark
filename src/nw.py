import momepy
from shapely.geometry import LineString
import networkx as nx

def unzip_line(geom, coordnum = 30):
    longline = [c for c in geom.coords]
    if len(longline)%coordnum == 1:
        coordnum+=1
    linestrings = []
    current_linestring = []
    for c in longline:
        current_linestring.append(c)
        if len(current_linestring) > coordnum:
            linestrings.append(LineString(current_linestring))
            del current_linestring
            current_linestring = [c]
    if current_linestring:
        linestrings.append(LineString(current_linestring))
    return linestrings

def drop_dangling_edges_iter(gdf_network, my_danglefactor, my_buffer, iters=5):
    G = momepy.gdf_to_nx(gdf_network=gdf_network, multigraph = False, integer_labels=True)
    for _ in range(iters):
        degree_one = [n for n in G.nodes if nx.degree(G, n)==1]
        degree_one_to_remove = []
        for n in degree_one:
            if G.edges[list(G.edges(n))[0]]["mm_len"] < my_danglefactor * my_buffer:
                degree_one_to_remove.append(n)
        G.remove_nodes_from(degree_one_to_remove)
    edges = momepy.nx_to_gdf(G, points=False, lines=True)
    edges_rem = momepy.remove_false_nodes(edges)
    edges_rem["i"] = edges_rem.index
    return edges_rem