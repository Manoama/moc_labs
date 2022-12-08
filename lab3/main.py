from func import *

FILES_CONTENT = file_reader()

@timeit
def attack_with_small_exponent(diff = 'hard'):
    rs = FILES_CONTENT['se'][diff]['c']
    ds = FILES_CONTENT['se'][diff]['n']
    if diff == 'hard':
        e = 5
    if diff == 'test':
        e = 3
    m = hastad(rs, ds, e)
    print(f"M = {hex(m)}")

if __name__ == "__main__":
    for key in FILES_CONTENT['se'].keys():
        attack_with_small_exponent(key)

