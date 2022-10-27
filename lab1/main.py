import numpy as np
import os
import sys

vars = (6, 13)

def p_C(v, p, t):                                                   # P(C)
    res = np.zeros(20)
    for i in range(20):
        for j in range(20):
            h = t[i][j]                                             # беремо індекс шифротексту з table_xx 
            res[h] += p[0][j]*p[1][i]                               # P(C_h) += P(k_i)*P(M_i)
    tmp = np.resize(np.append(np.arange(20), res), (2, 20))
    np.savetxt(f"lab1/p_C_var{v}.csv", tmp, delimiter=";", fmt='%.4g')
    return res

def p_MC(v, p, t):                                                  # Р(М, С)
    res = np.zeros((20, 20))
    for i in range(20):
        for j in range(20):
            res[t[j][i]][i] += p[0][i]*p[1][j]                              # P(C_table_xx[j][i], M_i) += P(M_i)*P(k_j)
    np.savetxt(f"lab1/p_MC_var{v}.csv", res, delimiter=";", fmt='%.4g')       
    return res

def p_M_C(v, c, mc):                                                # P(M | C)
    res = np.empty((20, 20))
    for i in range(20):
        res[i] = mc[i] / c[i]
    np.savetxt(f"lab1/p_M_C_var{v}.csv", res, delimiter=";", fmt='%.4g')
    return res

def opt_det(v, t):                                                  # optimal deterministic solving function 
    res = np.empty(0)
    for i in range(20):
        maxx_i = np.where(t[i] == np.max(t[i]))[0]                  # знаходимо індекси шифротексту, де рядок в P(M | C) має максимальні значення
        if maxx_i.size > 1:                                         # якщо ідексів > 1, то беремо будь-який (в данній програмнній реалізації беремо тільки перший індекс)
            res = np.append(res, maxx_i[0])
        else:
            res = np.append(res, maxx_i)
    tmp = np.resize(np.append(np.arange(20), res), (2, 20))
    np.savetxt(f"lab1/pdsf_var{v}.csv", tmp, delimiter=";", fmt='%d')
    return res    
    
def opt_stoch(v, t):                                                # optimal stochastic solving function 
    res = np.zeros((20, 20))
    for i in range(20):
        maxx_i = np.where(t[i] == np.max(t[i]))[0]                  # знаходимо індекси шифротексту, де рядок в P(M | C) має максимальні значення
        if maxx_i.size > 1:
            num = 1 / maxx_i.size
            for j in maxx_i:
                res[i][j] = num  
        else:
            res[i][maxx_i[0]] = 1
    np.savetxt(f"lab1/pssf_var{v}.csv", res, delimiter=";", fmt='%.2g')
    return res

def det_losses(v, df, t, pmc):                                      # losses for deterministic solving function
    res = np.zeros((20, 20), dtype = int)
    for i in range(20):
        for j in range(20):
            if df[t[i][j]] != i:
                res[t[i][j]][i] = 1
    print(f'Mean losses for deterministic solving function (var {v}) = {np.sum(res * pmc):.4f}')
    np.savetxt(f"lab1/pdsf_losses_var{v}.csv", res, delimiter=";", fmt='%d')
    

def stoch_losses(v, sf, t, pmc):                                    # losses for stochastic solving function
    res = np.empty((20, 20))
    r = np.arange(20, dtype = int)
    for i in range(20):
        for j in range(20):
            left_slice = sf[i][:j]
            right_slice = sf[i][j+1:]
                
            if left_slice.size == 0:
                res[i][j] = np.sum(right_slice)
            elif right_slice.size == 0:
                res[i][j] = np.sum(left_slice)
            else:
                res[i][j] = np.sum(right_slice)
                res[i][j] += np.sum(left_slice)
    print(f'Mean losses for stochastic solving function (var {v}) = {np.sum(res * pmc):.4f}')
    np.savetxt(f"lab1/pssf_losses_var{v}.csv", res, delimiter=";", fmt='%d')
    

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
        det_losses(v, pdsf, table, pmc)             # losses for deterministic solving function
        stoch_losses(v, pssf, table, pmc)           # losses for stochastic solving function
        
main()