#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 20:53:02 2025

@author: batuhanatas
"""

def check_mtz_solution(instance, solution):
    V = list(instance['coords'].keys())
    N = [i for i in V if i != 1]
    travel_time = instance['travel_time']
    tmax = solution['config']['tmax']
    m = solution['config']['m']
    clusters = instance['clusters']
    x_edges = set(solution['edges_used'])
    y_nodes = set(solution['selected_nodes'])

    # Check degree constraints
    for i in N:
        out_deg = sum(1 for j in V if (i, j) in x_edges)
        in_deg = sum(1 for j in V if (j, i) in x_edges)
        if i in y_nodes:
            if out_deg != 1 or in_deg != 1:
                return False, f"Node {i} visited but degree violation (in={in_deg}, out={out_deg})"
        else:
            if out_deg != 0 or in_deg != 0:
                return False, f"Node {i} not visited but degree violation (in={in_deg}, out={out_deg})"

    # Time constraint
    total_time = sum(travel_time[i, j] for (i, j) in x_edges)
    if total_time > m * tmax:
        return False, f"Total travel time {total_time} exceeds limit {m * tmax}"

    # Cluster check
    for k, cluster in enumerate(clusters):
        cluster_nodes = set(cluster['nodes'])
        if k in solution['covered_clusters'] and not cluster_nodes.issubset(y_nodes):
            return False, f"Cluster {k} counted but not all nodes visited"

    return True, "MTZ solution is feasible"
