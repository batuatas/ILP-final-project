#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 20:53:19 2025

@author: batuhanatas
"""

def check_scf_solution(instance, solution):
    V = list(instance['coords'].keys())
    N = [i for i in V if i != 1]
    travel_time = instance['travel_time']
    tmax = solution['config']['tmax']
    m = solution['config']['m']
    clusters = instance['clusters']
    x_edges = set(solution['edges_used'])
    y_nodes = set(solution['selected_nodes'])

    # Degree constraints
    for i in N:
        out_deg = sum(1 for j in V if (i, j) in x_edges)
        in_deg = sum(1 for j in V if (j, i) in x_edges)
        if i in y_nodes:
            if out_deg != 1 or in_deg != 1:
                return False, f"Node {i} visited but degree violation"
        else:
            if out_deg != 0 or in_deg != 0:
                return False, f"Node {i} not visited but has arcs"

    # Time constraint
    total_time = sum(travel_time[i, j] for (i, j) in x_edges)
    if total_time > m * tmax:
        return False, f"Time exceeded: {total_time} > {m * tmax}"

    # Cluster check
    for k, cluster in enumerate(clusters):
        cluster_nodes = set(cluster['nodes'])
        if k in solution['covered_clusters'] and not cluster_nodes.issubset(y_nodes):
            return False, f"Cluster {k} claimed covered but not all nodes visited"

    return True, "SCF solution is feasible"
