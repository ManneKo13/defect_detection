from lib2to3.pgen2.token import EQUAL
from tkinter import image_names
import cv2 as cv
from pathlib import Path
from src.data_preparation import DataFiles, move_figure
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

def random_image_indices(number_images, number_random):
    try:
        assert number_images >= number_random, "More random numbers desired than number of images!"
        # Indices of the images
        num_images = [x for x in range(number_images)]
        rand_num_images = []
        num = number_images
        for i in range(number_random): 
            idx = randint(0, num - 1)
            rand_num_images.append(num_images.pop(idx))
            num -= 1
    
        return rand_num_images
    except AssertionError as msg:
        print(msg)
    


def main():
    try:
        cwd = Path.cwd().as_posix()
        files = DataFiles(cwd)
        descriptions = ['Standard CLAHE', 'CLAHE in Lab', 'CLAHE in HSV']
        image_names = files.get_subdir_filenames('OK')
        files_as_images = files.make_img_list('OK')    

        rand_indices = random_image_indices(len(image_names), 4)

        idx = randint(0, len(image_names) - 1)
        img = files.get_img_from_filename('pattern', 'Muster_78.png')
        output_hsv = files.get_Clahe_img_hsv(img)
        # files.plot_specific_image(output_hsv)

        # img_bgr = cv.imread(f"{cwd}/data/points/0_0#(5755, 1774).png")
        output_yuv = files.get_Clahe_img_yuv(img)
        files.plot2img(output_hsv, output_yuv, 'Muster_78.png', 'YUV')

        # for i in rand_indices:
        #     output_gray = files.get_Clahe_img_gray(files_as_images[i])
        #     output_lab = files.get_Clahe_img_lab(files_as_images[i])
        #     output_hsv = files.get_Clahe_img_hsv(files_as_images[i])
        #     # files.plotThreeOutputs(files_as_images[i], output_gray, output_lab, output_hsv, image_names[i], descriptions)
        #     files.plot2img(files_as_images[i], output_hsv, image_names[i], 'HSV')
    except:
        print('An error occured!')
  
if __name__ == "__main__":
    main()