from func import *
import argparse

FILES_CONTENT = file_reader()
gmpy2.get_context().precision=2048
@timeit
def attack_with_small_exponent(difficulty = 'hard'):
    rs = FILES_CONTENT['se'][difficulty]['c']
    ds = FILES_CONTENT['se'][difficulty]['n']
    if difficulty == 'hard':
        e = 5
    if difficulty == 'test':
        e = 3
    m = hastad(rs, ds, e)
    print(f"M = {hex(m)}")

@timeit
def meet_in_the_middle_attack(l, difficulty, processes, step_size):
    e = 65537
    c = FILES_CONTENT['mitm'][difficulty]['c']
    n = FILES_CONTENT['mitm'][difficulty]['n']
    if l != 20:
        x = [j for i in some_magic(e, l, n, step_size=step_size,  processes = processes) for j in i]
    else:
        x = [j for i in some_magic(e, l, n, step_size=step_size,  processes = processes) for j in i]
    break_out_flag = False
    for i in x:
        cs = c*modInv(i[1], n) % n
        for j in x:
            if cs == j[1]:
                print(hex(j[1]*i[1]))
                break_out_flag = True
                break
        if break_out_flag:
            break
    else:
        print("Вiдкритий текст не було визначено.")

def main():
    parser = argparse.ArgumentParser(description="Cryptoanalysis of asymmetric cryptosystems on Applying attacks on RSA cryptosystem")
    parser.add_argument(
        "--processes", type=int, help="Number of processes to run", default=4
    )
  
    parser.add_argument(
        "--step-size", type=int, help="Stop search of L at this value", default=1000
    )
    args = parser.parse_args()

    for key in FILES_CONTENT['se'].keys():
        attack_with_small_exponent(key)
  
    for key in FILES_CONTENT['mitm'].keys():
        if key == 'bonus':
            meet_in_the_middle_attack(56, key, args.processes, args.step_size)
        else:
            meet_in_the_middle_attack(20, key, args.processes, args.step_size)
    

if __name__ == "__main__":
    main()