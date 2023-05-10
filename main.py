import cv2 as cv
from pathlib import Path
from src.filenames import Filenames
import numpy as np

def main():
    ''' ---------------
        Load some image
    '''
    # img = cv.imread(data_root)
    # cv.startWindowThread()
    # cv.namedWindow('Display Window')
    # cv.imshow('Display Window', img)
    # cv.waitKey(0)

    filenames = Filenames(Path.cwd().as_posix())
    pattern_files = filenames.fn_pattern
    img = cv.imread('')
    pass

if __name__ == "__main__":
    main()