import numpy as np
import pandas as pd
import os



vars = (6, 13)


def p_C(v, p, t):                           # P(C)
    res = np.zeros(20)
    for i in range(20):
        for j in range(20):
            c = t[i][j]
            res[c] += p[0][j]*p[1][i]
    np.savetxt(f"lab1/p_C_var{v}.csv", res, delimiter=";", fmt='%.6g')
  
    return res

def p_MC(v, p, t):                      # Р(М, С)
    res = np.zeros((20, 20))
    _t = t.T
    for i in range(20):
        m_i = _t[i]
        for ii in range(20):
            res[i][m_i[ii]] += p[1][ii]*p[0][i]
            
    np.savetxt(f"lab1/p_MC_var{v}.csv", res, delimiter=";", fmt='%.6g')       
    return res

def p_M_C(v, c, mc):                                                  # P(M | C)
    res = np.empty((20, 20))
    for i in range(20):
        res[i] = mc[i] / c[i]
    np.savetxt(f"lab1/p_M_C_var{v}.csv", res, delimiter=";", fmt='%.2g')
    return res

def main():
    dir_name = "lab1/"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".csv"):
            os.remove(os.path.join(dir_name, item))
    
    for v in vars:
        if v == 6:
            prob = np.genfromtxt("lab1\csv\prob_06.csv", delimiter=',')
            table =  np.genfromtxt("lab1\csv\/table_06.csv", delimiter=',', dtype=int)
        elif v == 13:
            prob = np.genfromtxt("lab1\csv\prob_13.csv", delimiter=',')
            table =  np.genfromtxt("lab1\csv\/table_13.csv", delimiter=',', dtype=int)
            
        pc = p_C(v, prob, table)
        pmc = p_MC(v, prob, table)
        pmc2 = p_M_C(v, pc, pmc.T)
        
        print(pc)
        print()
        print(pmc)
        print()
        print(pmc2)
      
main()