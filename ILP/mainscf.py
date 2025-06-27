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
from modelscf import solve_multi_vehicle_scf
from checkscf import check_scf_solution 

# Configurable parameters
m_values = [1, 2, 3, 4]
tmax_factors = [0.5, 0.8, 1.0, 1.2, 1.5]
time_limit = 900

# Load all instances
instances = load_all_data_files("instances")

# Create output folder
os.makedirs("results_scf", exist_ok=True)

# Run all combinations
for inst in instances:
    name = inst["filename"].replace(".data", "")
    tmax_original = inst["tmax"]

    for m in m_values:
        for factor in tmax_factors:
            tmax_scaled = round(factor * tmax_original)
            print(f"\n🔁 Solving {name} with m={m}, tmax={tmax_scaled} ({factor}×)")

            try:
                inst_copy = inst.copy()
                inst_copy["tmax"] = tmax_scaled

                result = solve_multi_vehicle_scf(inst_copy, m=m, tmax_override=tmax_scaled, time_limit=time_limit)

                # Feasibility check
                feasible, reason = check_scf_solution(inst_copy, result)
                if feasible:
                    print(f"Feasible solution found. Score: {result['objective']}")
                else:
                    print(f"Infeasible solution detected: {reason}")

                # Remove Gurobi model from result
                result_to_save = result.copy()
                if "model" in result_to_save:
                    del result_to_save["model"]
                result_to_save["feasibility_check"] = {
                    "passed": feasible,
                    "reason": reason
                }

                # Save with config-based filename
                suffix = f"m{m}_tmax{int(tmax_scaled)}"
                filename = f"{name}_scf_{suffix}.pkl"
                path = os.path.join("results_scf", filename)

                with open(path, "wb") as f:
                    pickle.dump(result_to_save, f)

                print(f"Saved: {filename}")

            except Exception as e:
                print(f"Error solving {name} (m={m}, tmax={tmax_scaled}): {e}")
