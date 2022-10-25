import numpy as np
import pandas as pd
import os
import sys

vars = (6, 13)

def p_C(v, p, t):                                           # P(C)
    res = np.zeros(20)
    for i in range(20):
        for j in range(20):
            c = t[i][j]
            res[c] += p[0][j]*p[1][i]
    tmp = np.resize(np.append(np.arange(20), res), (2, 20))
    np.savetxt(f"lab1/p_C_var{v}.csv", tmp, delimiter=";", fmt='%.4g')
    return res

def p_MC(v, p, t):                                          # Р(М, С)
    res = np.zeros((20, 20))
    _t = t.T
    for i in range(20):
        m_i = _t[i]
        for ii in range(20):
            res[m_i[ii]][i] += p[1][ii]*p[0][i]     
    np.savetxt(f"lab1/p_MC_var{v}.csv", res, delimiter=";", fmt='%.4g')       
    return res

def p_M_C(v, c, mc):                                        # P(M | C)
    res = np.empty((20, 20))
    for i in range(20):
        res[i] = mc[i] / c[i]
    np.savetxt(f"lab1/p_M_C_var{v}.csv", res, delimiter=";", fmt='%.4g')
    return res

def opt_det(v, t):                                          # optimal deterministic solving function 
    res = np.arange(20, dtype = int)
    for i in range(20):
        maxx_i = np.where(t[i] == np.max(t[i]))[0]
        if maxx_i.size > 1:
            res = np.append(res, maxx_i[0])
        else:
            res = np.append(res, maxx_i)
    res = np.resize(res, (2, 20))
    np.savetxt(f"lab1/pdsf_var{v}.csv", res, delimiter=";", fmt='%d')
    return res    
    
def opt_stoch(v, t):                                        # optimal stochastic solving function 
    res = np.zeros((20, 20))
    for i in range(20):
        maxx_i = np.where(t[i] == np.max(t[i]))[0]
        if maxx_i.size > 1:
            num = 1 / maxx_i.size
            for j in maxx_i:
                res[i][j] = num  
        else:
            res[i][maxx_i[0]] = 1
    np.savetxt(f"lab1/pssf_var{v}.csv", res, delimiter=";", fmt='%.2g')
    return res

def det_losses(v, df, t, pmc):                                  # losses for deterministic objective function
    res = np.zeros((20, 20), dtype = int)
    df = df[1]
    for i in range(20):
        for j in range(20):
            if df[t[i][j]] != i:
                res[t[i][j]][i] = 1
    print(f'Mean losses for deterministic objective function (var {v}) = {np.sum(res * pmc):.4f}')
    np.savetxt(f"lab1/pdsf_losses_var{v}.csv", res, delimiter=";", fmt='%d')
    return res


def main():
    dir_name = "lab1/"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".csv"):
            os.remove(os.path.join(dir_name, item))
    
    for v in vars:
        if v == 6:
            if sys.platform == "linux":
                prob = np.genfromtxt("lab1/csv/prob_06.csv", delimiter=',')
                table =  np.genfromtxt("lab1/csv/table_06.csv", delimiter=',', dtype=int)
            else:
                prob = np.genfromtxt("lab1\csv\/prob_06.csv", delimiter=',')
                table =  np.genfromtxt("lab1\csv\/table_06.csv", delimiter=',', dtype=int)
        elif v == 13:
            if sys.platform == "linux":
                prob = np.genfromtxt("lab1/csv/prob_13.csv", delimiter=',')
                table =  np.genfromtxt("lab1/csv/table_13.csv", delimiter=',', dtype=int)
            else:
                prob = np.genfromtxt("lab1\csv\/prob_13.csv", delimiter=',')
                table =  np.genfromtxt("lab1\csv\/table_13.csv", delimiter=',', dtype=int)
            
        pc = p_C(v, prob, table)                    # P(C)
        pmc = p_MC(v, prob, table)                  # Р(М, С)
        pmc2 = p_M_C(v, pc, pmc)                    # P(M | C)
        pdsf = opt_det(v, pmc2)                     # optimal deterministic solving function 
        pssf = opt_stoch(v, pmc2)                   # optimal stochastic solving function 
        dlosses = det_losses(v, pdsf, table, pmc)   # losses for deterministic objective function

        
main()