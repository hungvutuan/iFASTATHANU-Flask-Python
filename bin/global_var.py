import os

CURRENT_VER = "0.1.0"
ERR_PYTHON_VER_3 = 'Please use Python 3 to run this application'
FIRE = "Fire"
IMMINENT = "Imminent"
SAFE = "Safe"

FIRE_BAR = 80
IMMINENT_BAR = 50

TEMP_OFFSET = 70
SMOKE_OFFSET = 40

cur_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
cur_dir_list = cur_dir.split("/")
cur_dir_list.pop()

GLOBAL_DIR = '/'.join(map(str, cur_dir_list))

TRAINED_DATA_FILE = "val.txt"
ERROR = -1


def get_current_version():
    return CURRENT_VER


def get_error_python_version():
    return ERR_PYTHON_VER_3
