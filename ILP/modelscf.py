# -*- coding: utf-8 -*-
from gurobipy import Model, GRB, quicksum

def solve_multi_vehicle_scf(instance, m, tmax_override=None, time_limit=300, warm_start_model=None):
    V = list(instance['coords'].keys())
    N = [i for i in V if i != 1]
    A = [(i, j) for i in V for j in V if i != j]
    travel_time = instance['travel_time']
    tmax = tmax_override if tmax_override is not None else instance['tmax']
    clusters = instance['clusters']

    model = Model("MultiVehicleSCF")
    model.Params.OutputFlag = 1
    model.Params.TimeLimit = time_limit
    model.Params.Threads = 12
    model.Params.MIPFocus = 1
    model.Params.Heuristics = 0.05
    model.Params.Presolve = 2
    model.Params.Cuts = 3

    # VARIABLES
    x = model.addVars(A, vtype=GRB.BINARY, name="x")                          # arc used
    y = model.addVars(N, vtype=GRB.BINARY, name="y")                          # node visited
    z = model.addVars(len(clusters), vtype=GRB.BINARY, name="z")             # cluster covered
    f = model.addVars(A, vtype=GRB.CONTINUOUS, lb=0.0, ub=len(N), name="f")  # flow

    # OBJECTIVE
    model.setObjective(quicksum(clusters[k]["score"] * z[k] for k in range(len(clusters))), GRB.MAXIMIZE)

    # 1. DEPOT constraints
    model.addConstr(quicksum(x[1, j] for j in N) <= m, "DepotOutLimit")
    model.addConstr(quicksum(x[j, 1] for j in N) <= m, "DepotInLimit")
    model.addConstr(quicksum(x[1, j] for j in N) == quicksum(x[j, 1] for j in N), "DepotBalance")

    # 2. DEGREE constraints
    for i in N:
        model.addConstr(quicksum(x[i, j] for j in V if j != i) == y[i], f"Out_{i}")
        model.addConstr(quicksum(x[j, i] for j in V if j != i) == y[i], f"In_{i}")

    # 3. FLOW constraints
    model.addConstr(quicksum(f[1, j] for j in V if j != 1) == quicksum(y[i] for i in N), "FlowFromDepot")

    for i in N:
        model.addConstr(
            quicksum(f[j, i] for j in V if j != i) - quicksum(f[i, j] for j in V if j != i) == -y[i],
            f"FlowBalance_{i}"
        )

    for i, j in A:
        model.addConstr(f[i, j] <= len(N) * x[i, j], f"FlowCap_{i}_{j}")

    # 4. TOTAL TIME LIMIT
    model.addConstr(quicksum(travel_time[i, j] * x[i, j] for i, j in A) <= m * tmax, "TotalTime")

    # 5. CLUSTER COVERAGE
    for k, cluster in enumerate(clusters):
        model.addConstr(quicksum(y[i] for i in cluster["nodes"]) >= len(cluster["nodes"]) * z[k], f"Cluster_{k}")

    # 6. WARM START (optional)
    if warm_start_model is not None:
        for v in model.getVars():
            try:
                old_v = warm_start_model.getVarByName(v.VarName)
                if v.VType in [GRB.BINARY, GRB.INTEGER]:
                    v.Start = round(old_v.X)
                else:
                    v.Start = old_v.X
            except:
                continue

    # SOLVE
    model.optimize()

    # EXTRACT
    solution = {
        "model": model,
        "status": model.Status,
        "objective": model.ObjVal if model.SolCount > 0 else None,
        "selected_nodes": [i for i in N if y[i].X > 0.5],
        "covered_clusters": [k for k in range(len(clusters)) if z[k].X > 0.5],
        "edges_used": [(i, j) for (i, j) in A if x[i, j].X > 0.5],
        "runtime": model.Runtime,
        "vehicles_used": sum(1 for j in N if x[1, j].X > 0.5),
        "gap": None,
        "config": {
            "m": m,
            "tmax": tmax
        }
    }

    if model.SolCount > 0 and model.ObjBound != 0:
        solution["gap"] = (model.ObjBound - model.ObjVal) / model.ObjBound

    return solution
