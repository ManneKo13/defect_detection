import os
import glob
import cv2 as cv

class Filenames():
    def __init__(self, cwd: str) -> None:
        data_dir = cwd + '/data'
        data_subdir = os.listdir(data_dir)

        # Only subdirectories?
        subdir_names = []

        for i in range(len(data_subdir)):
            if os.path.isdir(data_dir + '/' + data_subdir[i]):
                # subdir_names_slash.append('/' + data_subdir[i])
                subdir_names.append(data_subdir[i])

        self.subdir_names = subdir_names

        subdir_paths = {}
        for i in range(len(subdir_names)):
            subdir_paths[subdir_names[i]] = data_dir + '/' + subdir_names[i]
        
        self.subdir_paths = subdir_paths

        # self.subdir_names_slash = subdir_names_slash

        subdir_filenames = {}
        for i in range(len(subdir_names)):
            subdir_filenames[subdir_names[i]] = [os.path.basename(x) for x in glob.glob(self.subdir_paths[subdir_names[i]] + '/*.png')]
        
        self.subdir_filenames = subdir_filenames
             
        # # List of filenames in directory points
        # self.fn_area = [os.path.basename(x) for x in glob.glob(data_dir + ls_subdir_data[0] + '/*.png')]
        # # List of filenames in directory points
        # self.fn_ok = [os.path.basename(x) for x in glob.glob(data_dir + ls_subdir_data[1] + '/*.png')]
        # # List of filenames in directory points
        # self.fn_pattern = [os.path.basename(x) for x in glob.glob(data_dir + ls_subdir_data[2] + '/*.png')]
        # # List of filenames in directory points
        # self.fn_points = [os.path.basename(x) for x in glob.glob(data_dir + ls_subdir_data[3] + '/*.png')]

class Image_Preparation():
    def __init__(self, 
                 image, 
                 image_name, 
                 clipLimit, 
                 tileGridSize) -> None:
        # Instantiate a Clahe opjekt 
        clahe = cv.createCLAHE(clipLimit = clipLimit,
                               tileGridSize = tileGridSize)
        
        # Convert the BGR images into the desiered color spaces 
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        lab_image = cv.cvtColor(image, cv.COLOR_BGR2Lab)

        # Attributes without using Histogram Equalization
        self.image = image
        self.image_name = image_name
        self.img_gray_histeq = clahe.apply(gray_image)
        
        ''' ---------------
            Applying limited adaptive Histogram Equalization onto the
            layer which are describing the intensity of the image, in the
            corresponding color space.
        ''' 
        hsv_image[:,:,2] = clahe.apply(hsv_image[:,:,2])
        lab_image[:,:,0] = clahe.apply(lab_image[:,:,0])

        self.img_hsv_histeq = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
        self.img_lab_histeq = cv.cvtColor(lab_image, cv.COLOR_Lab2BGR)
