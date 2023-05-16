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

# def plotClaheGray(img, img_name):
#     clahe = Image_Preparation(img, img_name, clipLimit = 2.0, tileGridSize = (8, 8))
#     plot2img(img, clahe.img_gray_histeq, clahe.image_name)

# def plotClaheHSV(img, img_name):
#     clahe = Image_Preparation(img, img_name, clipLimit = 2.0, tileGridSize = (8, 8))
#     plot2img(img, clahe.img_hsv_histeq, clahe.image_name)

# def plotClaheLab(img, img_name):
#     clahe = Image_Preparation(img, img_name, clipLimit = 2.0, tileGridSize = (8, 8))
#     plot2img(img, clahe.img_lab_histeq, clahe.image_name)
    
def main():
    # try:
    cwd = Path.cwd().as_posix()
    module = DataFiles(cwd)

    image_names = module.get_subdir_filenames('pattern')
    files_as_images = module.make_img_list('pattern')    

    idx = randint(0, len(image_names) - 1)
    # img_prep = Image_Preparation(img_pattern_files[idx], 
    #                              image_names[idx],
    #                              clipLimit = 2.0, 
    #                              tileGridSize = (4, 4))

    # plotEqualHist(img_pattern_files[0], image_names[0])
    # plotClaheGray(files_as_images[idx], image_names[idx])
    
    # plotClaheHSV(files_as_images[idx], image_names[idx])
    # plotClaheLab(files_as_images[idx], image_names[idx])
    # module.plotMultipleOutputs(files_as_images[0], files_as_images[1], files_as_images[2], files_as_images[3], image_names[0])
    # for i in range(len(image_names)):
    #     img_prep = Image_Preparation(img_pattern_files[i], 
    #                                  image_names[i],
    #                                  clipLimit = 2.0, 
    #                                  tileGridSize = (4, 4))

    #     plotMultipleOutputs(img_bgr = img_prep.image, 
    #                         img_clahe_gray_bgr = img_prep.img_gray_histeq,
    #                         img_clahe_hsv_bgr = img_prep.img_hsv_histeq,
    #                         img_clahe_lab_bgr = img_prep.img_lab_histeq,
    #                         img_name = img_prep.image_name)
    # except:
    #     print('An error occured!')

if __name__ == "__main__":
    main()