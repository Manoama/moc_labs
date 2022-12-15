from func import *
import argparse
import pickle
from pathlib import Path


FILES_CONTENT = file_reader()


@timeit(display_args=True)
def attack_with_small_exponent(difficulty="hard"):
    rs = FILES_CONTENT["se"][difficulty]["c"]
    ds = FILES_CONTENT["se"][difficulty]["n"]
    if difficulty == "hard":
        e = 5
    if difficulty == "test":
        e = 3
    m = hastad(rs, ds, e)
    print(f"M = {hex(m)}")


@timeit(display_args=True)
def meet_in_the_middle_attack(l, difficulty, processes, step_size):

    config = Config()
    config.n = FILES_CONTENT["mitm"][difficulty]["n"]
    config.c = FILES_CONTENT["mitm"][difficulty]["c"]
    config.e = 65537
    get_x(difficulty, config.e, l, config.n, processes, step_size)
    m = find_m()
    if m is None:
        print("Вiдкритий текст не було визначено.")
    else:
        print(f"M = {hex(m)}")


@timeit(display_args=False)
def get_x(difficulty, e, l, n, processes, step_size):
    config = Config()
    config.precalculated_dir = Path(f"{config.cache_dir}/{e}_{l}_{difficulty}/")
    config.precalculated_dir.mkdir(parents=True, exist_ok=True)
    save_file = config.precalculated_dir / "x.pkl"
    if save_file.exists():
        with open(save_file, "rb") as f:
            x = pickle.load(f)
    else:
        x = calculate_x(e, l, n, processes, step_size)
        with open(save_file, "wb") as f:
            pickle.dump(x, f)
    x = sorted(x, key = lambda x: x[0])
    
    config.x = [j for (i, j, c) in x]
    config.cs = [c for (i, j, c) in x]


@timeit(display_args=False)
def calculate_x(e, l, n, processes, step_size):
    if l != 20:
        x = [
            j
            for i in some_magic(e, l, n, step_size=step_size, processes=processes)
            for j in i
        ]
    else:
        x = [
            j
            for i in some_magic(e, l, n, step_size=step_size, processes=processes)
            for j in i
        ]
    return x


def main():
    parser = argparse.ArgumentParser(
        description="Cryptoanalysis of asymmetric cryptosystems on Applying attacks on RSA cryptosystem"
    )
    parser.add_argument(
        "--processes", type=int, help="Number of processes to run", default=10
    )

    parser.add_argument(
        "--step-size", type=int, help="Stop search of L at this value", default=100000
    )

    parser.add_argument("--cache-dir", type=str, help="cache directory location", default="precalculated")
    args = parser.parse_args()

    Config().cache_dir = args.cache_dir
    for key in FILES_CONTENT["se"].keys():
        attack_with_small_exponent(key)

    for key in FILES_CONTENT["mitm"].keys():
        if key == "bonus":
            meet_in_the_middle_attack(56, key, args.processes, args.step_size)
        else:
            meet_in_the_middle_attack(20, key, args.processes, args.step_size)


if __name__ == "__main__":
    main()
