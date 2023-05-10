import cv2 as cv
from pathlib import Path
from src.data_preparation import Filenames
import numpy as np
from os import listdir
from os import path

def main():
    cwd = Path.cwd().as_posix()
    
    filenames = Filenames(cwd)
    num_pattern_files = len(filenames.subdir_filenames['pattern'])
    img_pattern_files = []
    for i in range(num_pattern_files):
        filename = filenames.subdir_paths['pattern'] + '/' + filenames.subdir_filenames['pattern'][i] 
        img = cv.imread(filename)
        img_pattern_files.append(img)

    ''' ---------------
        Load some image
    '''
    cv.startWindowThread()
    cv.namedWindow('Display Window')
    cv.imshow('Display Window', img_pattern_files[1])
    # Press enter in the window to close 
    cv.waitKey(0)


if __name__ == "__main__":
    main()