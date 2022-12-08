import gmpy2
from config import *
from functools import wraps
import time
from multiprocessing import Pool
import sys

gmpy2.get_context().precision=2048
sys.setrecursionlimit(1000000000)
def egcd(a, b):
    '''
    Розширений евклідів gcd. Повертає g,x,y такі, що ax+by=g=gcd(a,b)
    '''
    if a == 0: 
        return (b, 0, 1)
    else:
        g, y, x = egcd(b%a, a)
        return (g, x-(b//a)*y, y)

def modInv(a, m):
    '''
    Повертає r таке, що a*r mod m = 1.
    '''
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m
 
 
def chinese_remainder(ds, rs):
    '''
    Китайська теорема про залишок
    ds: масив дільників
    rs: масив остач
    Повертає число s таке, що s mod ds[i] = rs[i]
    '''
    length = len(ds)
    if not length == len(rs):
        print("Довжина обох повинна бути однаковою")
        return None

    prod = 1 
    s = 0
    for i in range(length):
        prod *= ds[i]
    for i in range(length):
        p = prod // ds[i]
        s += (rs[i] * modInv(p, ds[i]) * p)
    return s % prod

def get_root(a, n):
    r00t = int(gmpy2.root(a, n))
    return r00t
    
def hastad(cs, ns, e):
    crt = chinese_remainder(ns, cs)
    r00t = get_root(crt, e)
    if r00t:
        return r00t
    else:
        print(f"Не вдається знайти {e}-й корінь з {hex(crt)}")


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        print(f'Час виконання функції {func.__name__}({args}) в секундах становить {total_time:.4f} секунд.')
        return result
    return timeit_wrapper


def file_reader():
    FILE = {}
    for k1 in PATH.keys():
        FILE[k1] = {}
        for k2 in PATH[k1].keys():
            FILE[k1][k2] = {}
            if k1 == 'se':
                FILE[k1][k2]['c'] = []
                FILE[k1][k2]['n'] = []
            else:
                FILE[k1][k2]['c'] = 0
                FILE[k1][k2]['n'] = 0
            with open(PATH[k1][k2], mode = 'r') as file:  
                text = file.read().lower().strip().split()
                res = [int(text[i], 16) for i in range(2, len(text), 3)]
                if k1 == 'se':
                    FILE[k1][k2]['c'] = [res[i] for i in range(0, len(res), 2)]
                    FILE[k1][k2]['n'] = [res[i] for i in range(1, len(res), 2)]
                    
                else:
                    FILE[k1][k2]['c'] = res[0]
                    FILE[k1][k2]['n'] = res[1]

    return FILE

def calc_range_window(range_start, range_end, step):
    start = range_start
    while start < range_end:
        end = start + step
        if end > range_end:
            end = range_end
        yield start, end
        start = end + 1

def some_magic(e, l, n, step_size=1000,  processes = 2):
    pool = Pool(processes=processes)
    sub_processes = []
    for start, end in calc_range_window(1, 2**(l//2), step_size):
        r = pool.apply_async(x_gen, [e, n, start, end])
        sub_processes.append(r)
        yield r.get()
    pool.close()
    pool.join()

def x_gen(e, n, start, end):
    x = [(i, i**e % n) for i in range(start, end+1)]
    return x


