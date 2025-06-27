#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 16:09:26 2025

@author: batuhanatas
"""

import os
import math

def read_data_file(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Header
    num_nodes, num_clusters, tmax = map(int, lines[0].split())

    # Section indices
    node_start = lines.index("NODE_COORD_SECTION") + 1
    set_start = lines.index("SET_SECTION")

    # Nodes
    coords = {}
    for line in lines[node_start:set_start]:
        node_id, x, y = map(int, line.split())
        coords[node_id] = (x, y)
    
    # Clusters
    clusters = []
    for line in lines[set_start + 1:]:
        parts = list(map(int, line.split()))
        cluster_id, score, *members = parts
        clusters.append({
            "id": cluster_id,
            "score": score,
            "nodes": members
        })
    
    # Travel times
    travel_time = {}
    for i in coords:
        for j in coords:
            if i == j:
                travel_time[(i, j)] = 0
            else:
                xi, yi = coords[i]
                xj, yj = coords[j]
                dist = math.ceil(math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2))
                travel_time[(i, j)] = dist
    
    return {
        "filename": os.path.basename(file_path),
        "num_nodes": num_nodes,
        "num_clusters": num_clusters,
        "tmax": tmax,
        "coords": coords,
        "clusters": clusters,
        "travel_time": travel_time
    }

# Load all .data files from a folder
def load_all_data_files(folder_path="instances"):
    data_files = [f for f in os.listdir(folder_path) if f.endswith('.data')]
    instances = []
    for fname in data_files:
        path = os.path.join(folder_path, fname)
        try:
            instance = read_data_file(path)
            instances.append(instance)
        except Exception as e:
            print(f"❌ Error in {fname}: {e}")
    return instances

# Print summary
def print_instance_summary(instances):
    for inst in instances:
        print(f"\n File: {inst['filename']}")
        print(f"  → Nodes: {inst['num_nodes']}, Clusters: {inst['num_clusters']}, Tmax: {inst['tmax']}")
        print(f"  → First cluster (if any): {inst['clusters'][0] if inst['clusters'] else 'None'}")




