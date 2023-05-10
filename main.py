import cv2 as cv
from pathlib import Path

def main():
    data_root = Path.cwd().as_posix() + '/data/points/0_0#(2171, 1537).png'
    ''' ---------------
        Load some image
    '''
    img = cv.imread(data_root)
    cv.startWindowThread()
    cv.namedWindow('Display Window')
    cv.imshow('Display Window', img)
    cv.waitKey(0)

if __name__ == "__main__":
    main()