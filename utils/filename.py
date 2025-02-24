from utils.params import *

"""
    Filename conversion utilities.
"""

def filename_to_code(filename):
    car_code, angle_code = filename.split('.')[0].split('_')
    return car_code, angle_code

def code_to_filename(car_code, angle_code, mask = False):
    return car_code + '_' + angle_code + ('_mask.gif' if mask else '.jpg')

def get_full_path(filename, mask = False, test=False):
    if mask is True:
        return TRAIN_MASKS_PATH + '/' + filename
    elif test is True:
        return TEST_DIR_PATH + '/' + filename
    else :
        return TRAIN_PATH + '/' + filename
    
def get_filepath_from_code(car_code, angle_code, mask = False, test=False):
    return get_full_path(code_to_filename(car_code, angle_code, mask), mask, test)