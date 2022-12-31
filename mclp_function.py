from mip import Model, xsum, maximize, BINARY
from scipy.spatial import distance_matrix
import time
import numpy as np

from utils import generate_candidate_sites
from gurobipy import GRB, quicksum

def mclp(df, K, M, radius):
    start = time.time()
    sites = generate_candidate_sites(df, M)
    I = J = sites.shape[0]
    D = distance_matrix(sites, sites)
    mask1 = D <= radius
    D[mask1] = 1
    D[~mask1] = 0

    m = Model()

    x = {}
    y = {}
    
    for i in range(I):
        y[i] = m.addVar(vtype=GRB.BINARY, name=f"y{i}")
    for j in range(J):
        x[j] = m.addVar(vtype=GRB.BINARY, name=f"x{j}")

    m.update()
    
    # 제약식 추가
    m.addConstr(quicksum(x[j] for j in range(J)) == K)

    for i in range(I):
        m.addConstr(quicksum(x[j] for j in np.where(D[i]==1)[0]) >= y[i])

    m.setObjective(quicksum(y[i]for i in range(I)),GRB.MAXIMIZE)
    m.setParam('OutputFlag', 0)
    m.optimize()
    end = time.time()
    
    solution = []
    if m.status == GRB.Status.OPTIMAL:
        for v in m.getVars():
            if v.x==1 and v.varName[0]=="x":
                solution.append(int(v.varName[1:]))
    opt_sites = sites[solution]
    return opt_sites, m.objVal