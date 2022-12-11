from pathlib import Path

var = "13"

if var < "10":
    var = "0" + var

PATH = {
    "se": {
        "hard": Path(f"SE_vars/SE_RSA_1024_5_hard/{var}.txt"),
        "test": Path(f"SE_vars/test_SE_RSA_256_3_for_dummy_dummies/{var}.txt"),
    },
    "mitm": {
        "regular": Path(f"MitM_vars/MitM_RSA_2048_20_regular/{var}.txt"),
        "test": Path(f"MitM_vars/test_MitM_RSA_512_20_for_dummy_dummies/{var}.txt"),
        "bonus": Path(f"MitM_vars/bonus_MitM_RSA_2048_56_hard/{var}.txt"),
    },
}
