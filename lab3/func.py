import gmpy2
import pickle
from config import *
from functools import wraps
import time
from multiprocessing import Pool
import sys
import numpy as np

gmpy2.get_context().precision = 2048
sys.setrecursionlimit(1000000000)


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class Config(Singleton):
    precalculated_dir: Path
    cache_dir: str
    x: list
    c: int
    n: int
    cs: list
    e : int


def egcd(a, b):
    """
    Розширений евклідів gcd. Повертає g,x,y такі, що ax+by=g=gcd(a,b)
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def mod_inv(a, m):
    """
    Повертає r таке, що a*r mod m = 1.
    """
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m


def chinese_remainder(ds, rs):
    """
    Китайська теорема про залишок
    ds: масив дільників
    rs: масив остач
    Повертає число s таке, що s mod ds[i] = rs[i]
    """
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
        s += rs[i] * mod_inv(p, ds[i]) * p
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


def timeit(display_args):
    def decorator(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            msg = func.__name__
            msg += f"({args})" if display_args else "()"
            print(
                f"Час виконання функції {msg} в секундах становить {total_time:.4f} секунд."
            )
            return result

        return timeit_wrapper

    return decorator


def file_reader():
    file = {}
    for k1 in PATH.keys():
        file[k1] = {}
        for k2 in PATH[k1].keys():
            file[k1][k2] = {}
            if k1 == "se":
                file[k1][k2]["c"] = []
                file[k1][k2]["n"] = []
            else:
                file[k1][k2]["c"] = 0
                file[k1][k2]["n"] = 0
            with open(PATH[k1][k2], mode="r") as f:
                text = f.read().lower().strip().split()
                res = [int(text[i], 16) for i in range(2, len(text), 3)]
                if k1 == "se":
                    file[k1][k2]["c"] = [res[i] for i in range(0, len(res), 2)]
                    file[k1][k2]["n"] = [res[i] for i in range(1, len(res), 2)]

                else:
                    file[k1][k2]["c"] = res[0]
                    file[k1][k2]["n"] = res[1]

    return file


def calc_range_window(range_start, range_end, step):
    start = range_start
    while start < range_end:
        end = start + step
        if end > range_end:
            end = range_end
        yield start, end
        start = end + 1


def calculate_cs(x, c, n):
    return (c * mod_inv(x, n)) % n


@timeit(display_args=False)
def find_m(config = Config()):
    x, cs = config.x, config.cs
    similiar = list(set(x)&set(cs))
    ind = [x.index(i)+1 for i in similiar]
    return np.prod(ind)


@timeit(display_args=False)
def some_magic(e, l, n, step_size=1000, processes=4):
    x1 = np.arange(1, pow(2, l // 2) + 1)
    pool = Pool(processes=processes)
    sub_processes = []
    for start, end in calc_range_window(0, x1.size - 1, step_size):
        r = pool.apply_async(x_gen, [x1[start : end + 1], e, n, Config()])
        sub_processes.append(r)
    pool.close()
    pool.join()
    return [r.get() for r in sub_processes]


def x_gen(a, e, n, config):
    save_file = config.precalculated_dir / f"x-{a[0]}-{a[-1]}.pkl"
    if save_file.exists():
        with open(save_file, "rb") as f:
            x = pickle.load(f)
    else:

        x2 = [pow(int(i), e, n) for i in a]
        cs = [calculate_cs(i, config.c, n)  for i in x2]
        x = [(int(i), hash(str(j)), hash(str(k))) for (i, j, k) in zip(a, x2, cs)]

        with open(save_file, "wb") as f:
            pickle.dump(x, f)
    return x
