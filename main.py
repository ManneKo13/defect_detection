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
matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt

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

    plt.show()

def plotEqualHist(img, img_name):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    equ = cv.equalizeHist(gray_img)
    plot2img(img, equ, img_name)

def plotClaheGray(img, img_name):
    clahe = Image_Preparation(img, clipLimit = 2.0, tileGridSize = (8, 8))
    plot2img(img, clahe.img_gray_histeq, img_name)

def plotClaheHSV(img, img_name):
    clahe = Image_Preparation(img, clipLimit = 2.0, tileGridSize = (8, 8))
    plot2img(img, clahe.img_hsv_histeq, img_name)

def plotClaheLab(img, img_name):
    clahe = Image_Preparation(img, clipLimit = 2.0, tileGridSize = (8, 8))
    plot2img(img, clahe.img_lab_histeq, img_name)
    
def main():
    img_pattern_files, image_names = make_img_lists('pattern')
    ''' ---------------
        Plot some image
    '''
    # cv.startWindowThread()
    # cv.namedWindow('Display Window')
    # cv.imshow('Display Window', img_pattern_files[0])
    # # Press enter in the window to close 
    # cv.waitKey(0)

    idx = randint(0, len(image_names) - 1)
    # plotHist(img_pattern_files[4], image_names[1])
    ''' ---------------
        Using some Filters
    '''
    # mod_img = cv.cvtColor(img_pattern_files[0], cv.COLOR_BGR2HSV)
    # gray_img = cv.cvtColor(img_pattern_files[0], cv.COLOR_BGR2GRAY)
    # plot2img(img_pattern_files[0], gray_img, image_names[0])
    
    # plotEqualHist(img_pattern_files[0], image_names[0])
    # for i in range(len(image_names)):
    #     plotClaheGray(img_pattern_files[i], image_names[i])
    # plotClaheHSV(img_pattern_files[idx], image_names[idx])
    plotClaheLab(img_pattern_files[idx], image_names[idx])

if __name__ == "__main__":
    main()