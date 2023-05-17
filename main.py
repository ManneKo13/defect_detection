from lib2to3.pgen2.token import EQUAL
from msilib.schema import Directory
from tkinter import image_names
import cv2 as cv
from pathlib import Path
from src.data_preparation import DataFiles, move_figure
import numpy as np
import os
import matplotlib
from random import randint
from matplotlib import pyplot as plt
import sys
from math import sqrt

''' ---------------
    Function returns a list of a random subset of 
    the set {0, ... ,number_images - 1}
    - number_images: upper bound for the set from which to pick
    - number_random: the size of the subset
'''
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
    except AssertionError as e:
        e.action = "in function random_image_indices()"
        raise

''' ---------------
    Saves all the images after and CLAHE transformation
    in the HSV color space. The directory for the saves 
    should be in cwd/data/transformed/subdir, if this directory
    does not exist an exception arises. Further are getting all the
    imagenames "_HSV" at the end.
    - subdir: the subdirectory with the wished images to save the 
              transformation
'''
def save_hsv_transformed_images(subdir):
    try:
        # Change the current working directory
        cwd = Path.cwd().as_posix()
        directory = cwd + '/data/transformed/' + subdir
        if Path(directory).exists():
            os.chdir(directory)
            
            # Get all the data from the subdirectory
            files = DataFiles(cwd)
            image_names = files.get_subdir_filenames(subdir)
            files_as_images = files.make_img_list(subdir)

            for i in range(len(image_names)):
                p = Path(image_names[i])
                output_name = str(p.with_stem(p.stem + '_HSV'))

                # Get transformed image
                output = files.get_Clahe_img_hsv(files_as_images[i])
                cv.imwrite(output_name, output)
        else:
            os.chdir(cwd)
            assert Path(directory).exists() == True, "No such subdirectory!"
            
    except AssertionError as e:
        e.action = "in function save_hsv_transformed_images()"
        raise

def main():
    try:
        cwd = Path.cwd().as_posix()
        files = DataFiles(cwd)
        files_img = files.make_img_list('pattern')
        files.plot_all_transfomrs(files_img[2])

    except Exception as exc:
        if getattr(exc, 'action', None):
            msg = "Error {}: {}".format(exc.action, exc)
        else:
            msg = str(exc)
        sys.exit(msg)

if __name__ == "__main__":
    main()