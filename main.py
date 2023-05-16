from lib2to3.pgen2.token import EQUAL
from tkinter import image_names
import cv2 as cv
from pathlib import Path
from src.data_preparation import DataFiles, Image_Preparation, move_figure
import numpy as np
from os import listdir
from os import path
import matplotlib
from random import randint
from matplotlib import pyplot as plt

def plotHist(img, img_name):
    ''' ---------------
        Histogram for blue pixels
        - hist is a 256x1 array, each value corresponds to number of pixels
          in that image with its corresponding pixel value.    
    '''
    rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    fig = plt.figure(figsize = (15, 10))
    ax1 = fig.add_subplot(121) 
    ax1.imshow(rgb_img), ax1.set_title('Original (%s)' % img_name)
    # plt.xticks([]), plt.yticks([])  
    # hist = cv.calcHist([rgb_img], [channel], None, [256], [0, 256])
    ax2 = fig.add_subplot(122) 
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        hist = cv.calcHist([rgb_img], [i], None, [256], [0, 256])
        ax2 = plt.plot(hist, color = col)
        plt.xlim([0, 256])

    move_figure(fig, 0, 0)
    plt.show()

# def plotEqualHist(img, img_name):
#     gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     equ = cv.equalizeHist(gray_img)
#     plot2img(img, equ, img_name)

# def plotClaheLab(img, img_name):
#     clahe = Image_Preparation(img, img_name, clipLimit = 2.0, tileGridSize = (8, 8))
#     plot2img(img, clahe.img_lab_histeq, clahe.image_name)
    
def main():
    try:
        cwd = Path.cwd().as_posix()
        files = DataFiles(cwd)

        image_names = files.get_subdir_filenames('pattern')
        files_as_images = files.make_img_list('pattern')    

        idx = randint(0, len(image_names) - 1)
        
        output = files.get_Clahe_img_hsv(files_as_images[idx])
        files.plot2img(files_as_images[idx], output, image_names[idx], 'CLAHE in HSV')

    except:
        print('An error occured!')

if __name__ == "__main__":
    main()