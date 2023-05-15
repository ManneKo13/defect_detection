from lib2to3.pgen2.token import EQUAL
from tkinter import image_names
import cv2 as cv
from pathlib import Path
from src.data_preparation import Filenames, Image_Preparation
import numpy as np
from os import listdir
from os import path
import matplotlib
from random import randint
from matplotlib import pyplot as plt

def move_figure(f, x, y):
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        f.canvas.manager.window.move(x, y)

''' ---------------
    Function to get lists of the desired files in given subdirectory
    - img_pattern_files: list of images represented as numpy-arrays
    - img_names: list of the names of the images as string
'''
def make_img_lists(subdir_name: str) -> list:
    cwd = Path.cwd().as_posix()
    
    filenames = Filenames(cwd)
    img_names = filenames.subdir_filenames[subdir_name]
    num_pattern_files = len(filenames.subdir_filenames[subdir_name])
    img_pattern_files = []
    for i in range(num_pattern_files):
        # Get the whole path-filename 
        filename = filenames.subdir_paths[subdir_name] + '/' + filenames.subdir_filenames[subdir_name][i] 
        img = cv.imread(filename)
        img_pattern_files.append(img)

    return img_pattern_files, img_names

''' ---------------
    Function to plot two images, where the images should
    be represented as numpy-arrays. This function should be
    used to compare those two images.
    - img1: the original image
    - img2: the modified image
'''
def plot2img(img1, img2, img_name):
    rgb_img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
    rgb_img2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
    fig = plt.figure(figsize = (15, 10))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.imshow(rgb_img1), ax1.set_title('Original (%s)' % img_name)
    ax2.imshow(rgb_img2), ax2.set_title('Output')
    move_figure(fig, 0, 0)
    plt.show()

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

def plotEqualHist(img, img_name):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    equ = cv.equalizeHist(gray_img)
    plot2img(img, equ, img_name)

def plotClaheGray(img, img_name):
    clahe = Image_Preparation(img, img_name, clipLimit = 2.0, tileGridSize = (8, 8))
    plot2img(img, clahe.img_gray_histeq, clahe.image_name)

def plotClaheHSV(img, img_name):
    clahe = Image_Preparation(img, img_name, clipLimit = 2.0, tileGridSize = (8, 8))
    plot2img(img, clahe.img_hsv_histeq, clahe.image_name)

def plotClaheLab(img, img_name):
    clahe = Image_Preparation(img, img_name, clipLimit = 2.0, tileGridSize = (8, 8))
    plot2img(img, clahe.img_lab_histeq, clahe.image_name)

def plotMultipleOutputs(img_bgr, 
                        img_clahe_gray_bgr, 
                        img_clahe_hsv_bgr, 
                        img_clahe_lab_bgr,
                        img_name):
    img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
    img_clahe_gray = cv.cvtColor(img_clahe_gray_bgr, cv.COLOR_BGR2RGB)
    img_clahe_hsv = cv.cvtColor(img_clahe_hsv_bgr, cv.COLOR_BGR2RGB)
    img_clahe_lab = cv.cvtColor(img_clahe_lab_bgr, cv.COLOR_BGR2RGB)
    
    figure = plt.figure(figsize = (15, 10))
    ax = figure.subplots(2, 2)
    ax[0, 0].imshow(img_rgb), ax[0, 0].set_title('Original (%s)' % img_name)
    ax[0 ,1].imshow(img_clahe_gray), ax[0 ,1].set_title('Output (Gray)')
    ax[1, 0].imshow(img_clahe_hsv), ax[1, 0].set_title('Output (HSV space)')
    ax[1, 1].imshow(img_clahe_lab), ax[1, 1].set_title('Output (Lab space)')
    move_figure(figure, 0, 0)
    plt.show()
    
def main():
    img_pattern_files, image_names = make_img_lists('pattern')
    
    idx = randint(0, len(image_names) - 1)

    img_prep = Image_Preparation(img_pattern_files[idx], 
                                 image_names[idx],
                                 clipLimit = 2.0, 
                                 tileGridSize = (4, 4))

    # plotEqualHist(img_pattern_files[0], image_names[0])
    # plotClaheGray(img_pattern_files[idx], image_names[idx])
    # plotClaheHSV(img_pattern_files[idx], image_names[idx])
    # plotClaheLab(img_pattern_files[idx], image_names[idx])

    for i in range(len(image_names)):
        img_prep = Image_Preparation(img_pattern_files[i], 
                                     image_names[i],
                                     clipLimit = 2.0, 
                                     tileGridSize = (4, 4))

        plotMultipleOutputs(img_bgr = img_prep.image, 
                            img_clahe_gray_bgr = img_prep.img_gray_histeq,
                            img_clahe_hsv_bgr = img_prep.img_hsv_histeq,
                            img_clahe_lab_bgr = img_prep.img_lab_histeq,
                            img_name = img_prep.image_name)

if __name__ == "__main__":
    main()