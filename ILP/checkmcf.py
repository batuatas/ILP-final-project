#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 20:53:45 2025

@author: batuhanatas
"""

def check_mcf_solution(instance, solution):
    V = list(instance['coords'].keys())
    N = [i for i in V if i != 1]
    travel_time = instance['travel_time']
    tmax = solution['config']['tmax']
    m = solution['config']['m']
    clusters = instance['clusters']
    y_nodes = set(solution['selected_nodes'])
    x_edges = set(solution['edges_used'])

    # Degree constraints
    for i in N:
        out_deg = sum(1 for j in V if (i, j) in x_edges)
        in_deg = sum(1 for j in V if (j, i) in x_edges)
        if i in y_nodes:
            if out_deg != 1 or in_deg != 1:
                return False, f"MCF: Node {i} visited but degree incorrect"
        else:
            if out_deg != 0 or in_deg != 0:
                return False, f"MCF: Node {i} not visited but has arcs"

    # Travel time constraint
    total_time = sum(travel_time[i, j] for (i, j) in x_edges)
    if total_time > m * tmax:
        return False, f"MCF: Time exceeded: {total_time} > {m * tmax}"

    # Cluster check
    for k, cluster in enumerate(clusters):
        if k in solution['covered_clusters']:
            if not set(cluster['nodes']).issubset(y_nodes):
                return False, f"MCF: Cluster {k} claimed but incomplete node visit"

    return True, "MCF solution is feasible"
