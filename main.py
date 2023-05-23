from fileinput import filename
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

def save_hsv_blurred_images(subdir):
    try:
        # Change the current working directory
        cwd = Path.cwd().as_posix()
        directory = cwd + '/data/test/' + subdir
        if Path(directory).exists():
            os.chdir(directory)
            
            # Get all the data from the subdirectory
            files = DataFiles(cwd)
            image_names = files.get_subdir_filenames(subdir)
            files_as_images = files.make_img_list(subdir)

            p = Path(image_names[3])
            output_name = str(p.with_stem(p.stem + '_HSV_blurred'))

            # Get transformed image
            img_hsv = files.get_Clahe_img_hsv(files_as_images[3])
            output = files.get_Gaussian_blurred_img(img_hsv)
            cv.imwrite(output_name, output)

            files.plot2img(files_as_images[3], output, True, 'CLAHE with filtering')

        else:
            os.chdir(cwd)
            assert Path(directory).exists() == True, "No such subdirectory!"
            
    except AssertionError as e:
        e.action = "in function save_hsv_transformed_images()"
        raise

# # defining a function for the task
# def create_dirtree_without_files(src, dst):
   
#     # getting the absolute path of the source
#     # directory
#     src = os.path.abspath(src)
     
#     # making a variable having the index till which
#     # src string has directory and a path separator
#     src_prefix = len(src) + len(os.path.sep)
     
#     # making the destination directory
#     os.makedirs(dst)
     
#     # doing os walk in source directory
#     for root, dirs, files in os.walk(src):
#         for dirname in dirs:
           
#             # here dst has destination directory,
#             # root[src_prefix:] gives us relative
#             # path from source directory
#             # and dirname has folder names
#             dirpath = os.path.join(dst, root[src_prefix:], dirname)
             
#             # making the path which we made by
#             # joining all of the above three
#             os.mkdir(dirpath)
# # calling the above function
# create_dirtree_without_files('C:/Users/markorb/git/defect_detection/data/Basis_Bereinigt',
#                      'C:/Users/markorb/git/defect_detection/data/transformed/Basis_Bereinigt')

def img_transform(path, dst, file_name):
    clahe = cv.createCLAHE(clipLimit = 2.0,
                            tileGridSize = (8, 8))
    
    img = cv.imread(str(path))
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    ''' ---------------
        Applying limited adaptive Histogram Equalization onto the
        layer which are describing the intensity of the image, in the
        corresponding color space.
    ''' 
    hsv_image[:,:,2] = clahe.apply(hsv_image[:,:,2])
    hsv_image = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)

    img_blurred = cv.GaussianBlur(hsv_image, ksize = (3, 3), sigmaX = 0.5, sigmaY = 0.5)
    output_name = Path(file_name).with_stem(Path(file_name).stem + '_HSV_blurred')
    # if Path(dst).exists():
    #     os.chdir(dst) 
    cv.imwrite(str(dst.joinpath(output_name)), img_blurred)
    
    

def walk(path):
    copy_target = Path('data/transformed')
    cwd = Path.cwd()
    dst = cwd.joinpath(copy_target)
    for p in Path(path).iterdir():
        if p.is_dir():
            dir_path = dst.joinpath(p.relative_to(*p.parts[:1]))
            if not dir_path.exists():
                Path.mkdir(dir_path)
            yield from walk(p)
            continue
        if p.is_file() and p.suffix == '.png':
            file_name = p.stem + p.suffix
            file_path_with_name = dst.joinpath(p.relative_to(*p.parts[:1]))
            file_path = file_path_with_name.parent
            img_transform(p, file_path, file_name)
        yield p.resolve()

def main():
    try:
        cwd = Path.cwd()
        parent_path = Path('data/Eindeutig_NIO_Bereinigt')
        work_path = cwd.joinpath(parent_path)
        dst = Path(cwd).joinpath(Path('data/transformed/Eindeutig_NIO_Bereinigt'))
        if not dst.exists():
            Path.mkdir(dst)
        # files = DataFiles(cwd)
        # files_img = files.make_img_list('points')
        # filenames = files.get_subdir_filenames('points')
        # files.plot_all_transfomrs(files_img[2])
        # img_hsv = files.get_Clahe_img_hsv(files_img[2])
        # img_hsv_blur = files.get_Gaussian_blurred_img(img_hsv, kernel_size = (3, 3), std_dev_x = 0.5, std_dev_y = 0.5)
        # files.plot2img(img_hsv, img_hsv_blur, filenames[2], 'Gaussian Blur')
        # save_hsv_blurred_images('points')
        # root_directory = Path(cwd)
        # for path_object in root_directory.rglob('*.png'):
        #     if path_object.is_file():
        #         print(f"hi, I'm a file: {path_object}")
        #     elif path_object.is_dir():
        #         print(f"hi, I'm a dir: {path_object}")
        for p in walk(parent_path):
            print(p)
        # save_hsv_blurred_images('pattern')

         

    except Exception as exc:
        if getattr(exc, 'action', None):
            msg = "Error {}: {}".format(exc.action, exc)
        else:
            msg = str(exc)
        sys.exit(msg)

if __name__ == "__main__":
    main()