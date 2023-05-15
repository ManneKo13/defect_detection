import cv2 as cv
from pathlib import Path
from src.data_preparation import Filenames
import numpy as np
from os import listdir
from os import path
import matplotlib
matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt

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

def plot2img(img1, img2):
    fig = plt.figure(figsize = (15, 10))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.imshow(img1), ax1.set_title('Original')
    ax2.imshow(img2), ax2.set_title('Output')
    plt.show()

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

    ''' ---------------
        Histogram for blue pixels
        - hist is a 256x1 array, each value corresponds to number of pixels
          in that image with its corresponding pixel value.    
    '''
    # rgb_img = cv.cvtColor(img_pattern_files[0], cv.COLOR_BGR2RGB)
    # plt.subplot(121), plt.imshow(rgb_img), plt.title('Original')
    # plt.xticks([]), plt.yticks([])  
    # hist = cv.calcHist([img_pattern_files[0]], [0], None, [256], [0, 256])
    # plt.subplot(122), plt.plot(hist, 'b')
    # plt.xlim([0, 256])
    # # color = ('b', 'g', 'r')
    # # for i, col in enumerate(color):
    # #     hist = cv.calcHist([img_pattern_files[0]], [i], None, [256], [0, 256])
    # #     plt.plot(hist, color = col)
    # #     plt.xlim([0, 256])
    # plt.show()

    ''' ---------------
        Using some Filters
    '''
    rgb_img = cv.cvtColor(img_pattern_files[0], cv.COLOR_BGR2RGB)
    laplacian = cv.Laplacian(rgb_img, , 5)
    plot2img(rgb_img, laplacian)
    

if __name__ == "__main__":
    main()