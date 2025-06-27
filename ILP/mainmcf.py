#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 20:55:27 2025
Updated on Fri Jun 27 2025 — includes feasibility checks
@author: batuhanatas
"""

import os
import pickle
from gurobipy import GRB
from data import load_all_data_files
from modelmcf import solve_multi_vehicle_mcf
from checkmcf import check_mcf_solution 

# Fixed parameters
m = 3
tmax_factor = 1.0
time_limit = 900

# Load all instances
instances = load_all_data_files("instances")

# Create output folder
os.makedirs("results_mcf", exist_ok=True)

# Run with fixed config
for inst in instances:
    name = inst["filename"].replace(".data", "")
    tmax_original = inst["tmax"]
    tmax_scaled = round(tmax_factor * tmax_original)

    print(f"\nSolving {name} with m={m}, tmax={tmax_scaled} ({tmax_factor}×)")

    try:
        inst_copy = inst.copy()
        inst_copy["tmax"] = tmax_scaled

        result = solve_multi_vehicle_mcf(inst_copy, m=m, tmax_override=tmax_scaled, time_limit=time_limit)

        # Feasibility check
        feasible, reason = check_mcf_solution(inst_copy, result)
        if feasible:
            print(f"Feasible solution found. Score: {result['objective']}")
        else:
            print(f"⚠️ Infeasible solution detected: {reason}")

        # Clean model object before saving
        result_to_save = result.copy()
        if "model" in result_to_save:
            del result_to_save["model"]
        result_to_save["feasibility_check"] = {
            "passed": feasible,
            "reason": reason
        }

        # Save result
        suffix = f"m{m}_tmax{int(tmax_scaled)}"
        filename = f"{name}_mcf_{suffix}.pkl"
        path = os.path.join("results_mcf", filename)

        with open(path, "wb") as f:
            pickle.dump(result_to_save, f)

        print(f"Saved: {filename}")

    except Exception as e:
        print(f"Error solving {name} (m={m}, tmax={tmax_scaled}): {e}")
