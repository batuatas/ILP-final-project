#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pickle
from gurobipy import GRB
from data import load_all_data_files
from modelmtz import solve_multi_vehicle_mtz  

# Import feasibility checker
from checkmtz import check_mtz_solution  

# Configurable parameters
m_values = [1, 2, 3, 4]
tmax_factors = [0.5, 0.8, 1.0, 1.2, 1.5]
time_limit = 900

# Load instances
instances = load_all_data_files("instances")

# Create output folder
os.makedirs("results_mtz", exist_ok=True)

# Run all combinations
for inst in instances:
    name = inst["filename"].replace(".data", "")
    tmax_original = inst["tmax"]

    for m in m_values:
        for factor in tmax_factors:
            tmax_scaled = round(factor * tmax_original)
            print(f"\nSolving {name} with m={m}, tmax={tmax_scaled} ({factor}×)")

            try:
                # Override tmax manually inside instance copy
                inst_copy = inst.copy()
                inst_copy["tmax"] = tmax_scaled

                result = solve_multi_vehicle_mtz(inst_copy, m=m, time_limit=time_limit)

                # Run feasibility check
                feasible, reason = check_mtz_solution(inst_copy, result)

                if feasible:
                    print(f"Feasible solution found. Score: {result['objective']}")
                else:
                    print(f"Infeasible solution detected: {reason}")

                # Strip Gurobi model before saving
                result_to_save = result.copy()
                if "model" in result_to_save:
                    del result_to_save["model"]
                result_to_save["feasibility_check"] = {
                    "passed": feasible,
                    "reason": reason
                }

                # Save
                suffix = f"m{m}_tmax{tmax_scaled}"
                filename = f"{name}_mtz_{suffix}.pkl"
                with open(os.path.join("results_mtz", filename), "wb") as f:
                    pickle.dump(result_to_save, f)

                print(f"Saved: {filename}")

            except Exception as e:
                print(f"Error solving {name} (m={m}, tmax={tmax_scaled}): {e}")
