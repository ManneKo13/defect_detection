import cv2 as cv
from pathlib import Path
from src.data_preparation import Filenames
import numpy as np
from os import listdir
from os import path

def make_img_list(subdir_name: str) -> list:
    cwd = Path.cwd().as_posix()
    
    filenames = Filenames(cwd)
    num_pattern_files = len(filenames.subdir_filenames[subdir_name])
    img_pattern_files = []
    for i in range(num_pattern_files):
        filename = filenames.subdir_paths[subdir_name] + '/' + filenames.subdir_filenames[subdir_name][i] 
        img = cv.imread(filename)
        img_pattern_files.append(img)

    return img_pattern_files


def main():
    img_pattern_files = make_img_list('pattern')
    ''' ---------------
        Plot some image
    '''
    # cv.startWindowThread()
    # cv.namedWindow('Display Window')
    # cv.imshow('Display Window', img_pattern_files[0])
    # # Press enter in the window to close 
    # cv.waitKey(0)

if __name__ == "__main__":
    main()