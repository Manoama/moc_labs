from func import *

FILES_CONTENT = file_reader()

@timeit
def task1(diff = 'hard'):
    rs = FILES_CONTENT['se'][diff]['c']
    ds = FILES_CONTENT['se'][diff]['n']
    m = hastad(rs, ds, e)
    print(f"M = {m}")


if __name__ == "__main__":
    for key in FILES_CONTENT['se'].keys():
        task1(key)

