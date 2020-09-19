import os

CURRENT_VER = "0.1.0"
ERR_PYTHON_VER_3 = 'Please use Python 3 to run this application'
FIRE_DATASET = "/Dataset/fire.csv"
NON_FIRE_DATASET = "/Dataset/non_fire.csv"
TRAINED_DATA_FILE = "val.txt"

FIRE, IMMINENT, SAFE = "Fire", "Imminent", "Safe"
MESS_ERROR, MESS_INFO, MESS_WARNING, MESS_SUCCESS = "[ERROR]", "[INFO]", "[WARNING]", "[SUCCESS]"

FIRE_BAR = 90
IMMINENT_BAR = 50

TEMP_OFFSET = 40
SMOKE_OFFSET = 70
SUCCESS_CODE, ERROR_CODE = 1, -1

cur_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
cur_dir_list = cur_dir.split("/")
cur_dir_list.pop()

GLOBAL_DIR = '/'.join(map(str, cur_dir_list))


def get_current_version():
    return CURRENT_VER


def get_error_python_version():
    return ERR_PYTHON_VER_3
