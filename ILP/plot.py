#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualize MTZ solution with vehicle-separated colors and cluster highlights.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.cm as cm
from collections import defaultdict
from modelmtz import solve_multi_vehicle_mtz
from data import read_data_file
from collections import defaultdict, deque

def extract_vehicle_paths(edges, depot=1):
    """
    Infer vehicle tours from a set of directed edges.
    Returns list of paths (each path is a list of node IDs).
    """
    outgoing = defaultdict(list)
    incoming = defaultdict(list)

    for i, j in edges:
        outgoing[i].append(j)
        incoming[j].append(i)

    visited = set()
    paths = []

    # Start at depot → identify m starting arcs
    queue = deque(j for j in outgoing[depot])

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        path = [depot, current]
        visited.add(depot)
        visited.add(current)

        while current in outgoing:
            next_nodes = [j for j in outgoing[current] if j not in visited]
            if not next_nodes:
                break
            next_node = next_nodes[0]
            path.append(next_node)
            visited.add(next_node)
            current = next_node

        paths.append(path)

    return paths



def plot_solution_with_clusters(instance, solution, title=None):
    coords = instance["coords"]
    edges = solution["edges_used"]
    visited = set(solution["selected_nodes"])
    clusters = instance["clusters"]
    depot = 1

    plt.figure(figsize=(9, 7))
    ax = plt.gca()

    # Cluster colors
    cluster_colors = cm.tab20.colors
    node_cluster_map = {}
    for idx, cluster in enumerate(clusters):
        for node in cluster["nodes"]:
            node_cluster_map.setdefault(node, []).append(idx)

    # Assign each visited node a color based on one of its clusters
    node_colors = {}
    for node in visited:
        cluster_ids = node_cluster_map.get(node, [])
        color = cluster_colors[cluster_ids[0] % len(cluster_colors)] if cluster_ids else 'blue'
        node_colors[node] = color

    # Plot nodes
    for node, (x, y) in coords.items():
        if node == depot:
            plt.plot(x, y, 'rs', markersize=10, label="Depot")
        elif node in visited:
            plt.plot(x, y, 'o', markersize=6, color=node_colors.get(node, 'blue'))
        else:
            plt.plot(x, y, 'ko', markersize=4)

    # Reconstruct paths per vehicle and assign edge colors
    paths = extract_vehicle_paths(edges, depot)
    color_map = cm.get_cmap("tab10")

    for i, path in enumerate(paths):
        color = color_map(i % 10)
        for u, v in zip(path[:-1], path[1:]):
            x1, y1 = coords[u]
            x2, y2 = coords[v]
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                    arrowstyle='-|>',
                                    mutation_scale=12,
                                    linewidth=2,
                                    color=color,
                                    alpha=0.8,
                                    connectionstyle="arc3,rad=0.05")
            ax.add_patch(arrow)

    # Annotate node IDs
    for i, (x, y) in coords.items():
        plt.text(x + 0.5, y + 0.5, str(i), fontsize=9)

    plt.title(title or f"MTZ Directed Tours — Score: {solution.get('objective', '?')}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


# === CONFIG ===
data_file = "instances/eil15s3.data"
m = 2
tmax_factor = 1.0
time_limit = 300

# === LOAD AND SOLVE ===
instance = read_data_file(data_file)
tmax_scaled = round(instance["tmax"] * tmax_factor)
solution = solve_multi_vehicle_mtz(instance, m=m, tmax_override=tmax_scaled, time_limit=time_limit)

# === PLOT ===
plot_solution_with_clusters(instance, solution, title=f"{os.path.basename(data_file)} — MTZ Tours")
