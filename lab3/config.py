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
            'regular' : f"lab3\MitM_vars\MitM_RSA_2048_20_regular\{var}.txt",
            'test' : f"lab3\MitM_vars\/test_MitM_RSA_512_20_for_dummy_dummies\{var}.txt",
            'bonus' : f"lab3\MitM_vars\/bonus_MitM_RSA_2048_56_hard\{var}.txt"
        }
}
