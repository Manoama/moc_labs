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
    e = 65537
    c = FILES_CONTENT["mitm"][difficulty]["c"]
    n = FILES_CONTENT["mitm"][difficulty]["n"]
    x = get_x(difficulty, e, l, n, processes, step_size)
    break_out_flag = False
    for i in x:
        cs = c * mod_inv(i[1], n) % n
        for j in x:
            if cs == j[1]:
                print(f'M = {hex(i[0] * j[0])}')
                break_out_flag = True
                break
        if break_out_flag:
            break
    else:
        print("Вiдкритий текст не було визначено.")


@timeit(display_args=False)
def get_x(difficulty, e, l, n, processes, step_size):
    config = Config()
    config.precalculated_dir = Path(f"precalculated/{e}_{l}_{difficulty}/")
    config.precalculated_dir.mkdir(parents=True, exist_ok=True)
    save_file = config.precalculated_dir / "x.pkl"
    if save_file.exists():
        with open(save_file, "rb") as f:
            x = pickle.load(f)
    else:
        x = calculate_x(e, l, n, processes, step_size)
        with open(save_file, "wb") as f:
            pickle.dump(x, f)
    return x


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
        "--processes", type=int, help="Number of processes to run", default=12
    )

    parser.add_argument(
        "--step-size", type=int, help="Stop search of L at this value", default=100000
    )
    args = parser.parse_args()

    for key in FILES_CONTENT["se"].keys():
        attack_with_small_exponent(key)

    for key in FILES_CONTENT["mitm"].keys():
        if key == "bonus":
            meet_in_the_middle_attack(56, key, args.processes, args.step_size)
        else:
            meet_in_the_middle_attack(20, key, args.processes, args.step_size)


if __name__ == "__main__":
    main()
