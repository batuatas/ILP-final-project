from gurobipy import Model, GRB, quicksum

def solve_multi_vehicle_mtz(instance, m,tmax_override=None, time_limit=300, warm_start_model=None):
    V = list(instance['coords'].keys())
    N = [i for i in V if i != 1]  # non-depot nodes
    A = [(i, j) for i in V for j in V if i != j]
    travel_time = instance['travel_time']
    tmax = tmax_override if tmax_override is not None else instance['tmax']
    clusters = instance['clusters']
    n = len(N)

    model = Model("MultiVehicleMTZ_Stable")
    model.Params.OutputFlag = 1
    model.Params.TimeLimit = time_limit
    model.Params.Threads = 12
    model.Params.MIPFocus = 1
    model.Params.Heuristics = 0.05
    model.Params.Presolve = 2
    model.Params.Cuts = 3

    # VARIABLES
    x = model.addVars(A, vtype=GRB.BINARY, name="x")                     # tour arcs
    y = model.addVars(N, vtype=GRB.BINARY, name="y")                     # node visited
    z = model.addVars(len(clusters), vtype=GRB.BINARY, name="z")        # cluster covered
    u = model.addVars(N, vtype=GRB.CONTINUOUS, lb=0, ub=n - 1, name="u") # visit position

    # OBJECTIVE: maximize total score of covered clusters
    model.setObjective(quicksum(clusters[k]["score"] * z[k] for k in range(len(clusters))), GRB.MAXIMIZE)

    # 1. DEPOT constraints
    model.addConstr(quicksum(x[1, j] for j in N) <= m, "DepotOutLimit")
    model.addConstr(quicksum(x[j, 1] for j in N) <= m, "DepotInLimit")
    model.addConstr(quicksum(x[1, j] for j in N) == quicksum(x[j, 1] for j in N), "DepotBalance")

    # 2. DEGREE constraints + u[i] = 0 if not visited
    for i in N:
        model.addConstr(quicksum(x[i, j] for j in V if j != i) == y[i], f"Out_{i}")
        model.addConstr(quicksum(x[j, i] for j in V if j != i) == y[i], f"In_{i}")
        model.addConstr(u[i] <= (n - 1) * y[i], f"Deactivate_u_{i}")

    # 3. STABLE MTZ order constraints
    for i in N:
        for j in N:
            if i != j:
                model.addConstr(u[i] + 1 <= u[j] + (n - 1) * (1 - x[i, j]), f"MTZ_Order_{i}_{j}")

    # 4. TOTAL TIME constraint
    model.addConstr(quicksum(travel_time[i, j] * x[i, j] for i, j in A) <= m * tmax, "TotalTime")

    # 5. CLUSTER COVERAGE constraints
    for k, cluster in enumerate(clusters):
        model.addConstr(quicksum(y[i] for i in cluster["nodes"]) >= len(cluster["nodes"]) * z[k], f"Cluster_{k}")

    # 6. WARM START (optional)
    if warm_start_model is not None:
        for v in model.getVars():
            try:
                old_v = warm_start_model.getVarByName(v.VarName)
                v.Start = round(old_v.X) if v.VType in [GRB.BINARY, GRB.INTEGER] else old_v.X
            except:
                continue

    # SOLVE
    model.optimize()

    # RESULT
    solution = {
        "model": model,
        "status": model.Status,
        "objective": model.ObjVal if model.SolCount > 0 else None,
        "selected_nodes": [i for i in N if y[i].X > 0.5],
        "covered_clusters": [k for k in range(len(clusters)) if z[k].X > 0.5],
        "edges_used": [(i, j) for (i, j) in A if x[i, j].X > 0.5],
        "runtime": model.Runtime,
        "vehicles_used": sum(1 for j in N if x[1, j].X > 0.5),
        "gap": (model.ObjBound - model.ObjVal) / model.ObjBound if model.SolCount > 0 and model.ObjBound != 0 else None,
        "config": {
            "m": m,
            "tmax": tmax
        }
    }

    return solution
