e = 65537

# var = input('Введіть номер варіанта: ')

var = '13'

if var < '10':
    var = '0' + var

PATH = {
    'se': 
        {
            'hard': f"lab3\SE_vars\SE_RSA_1024_5_hard\{var}.txt",
            'test': f"lab3\SE_vars\/test_SE_RSA_256_3_for_dummy_dummies\{var}.txt"
        },
    'mitm' : 
        {
            'bonus' : f"lab3\MitM_vars\/bonus_MitM_RSA_2048_56_hard\{var}.txt",
            'regular' : f"lab3\MitM_vars\MitM_RSA_2048_20_regular\{var}.txt",
            'test' : f"lab3\MitM_vars\/test_MitM_RSA_512_20_for_dummy_dummies\{var}.txt"
        }
}

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
                    FILE[k1][k2]['c'] = tuple([res[i] for i in range(0, len(res), 2)])
                    FILE[k1][k2]['n'] = tuple([res[i] for i in range(1, len(res), 2)])
                    FILE[k1][k2]['cn'] = tuple([(i, j) for i, j in zip(FILE[k1][k2]['c'], FILE[k1][k2]['n'])])
                else:
                    FILE[k1][k2]['c'] = res[0]
                    FILE[k1][k2]['n'] = res[1]

    return FILE


