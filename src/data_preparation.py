import os
import glob
import cv2 as cv

''' ---------------
    This class manages the directory "data" in the working directory
    and their files in it.
    Attributes:
    - subdir_names: list of strings of subdirectories in data
    - subdir_paths: dictionary consisting of the paths to each
                    subdirectory with the corresponding key from
                    subdir_names.
    - subdir_filenames: dictionary consisting of all the png-filenames in each
                        subdirectory with the corresponding key from
                        subdir_names.
    - subdir_paths_of_filenames: dictionary consisting of the paths to each
                                 filename with the corresponding key from
                                 subdir_names.
    Methods:

'''
class Filenames():
    def __init__(self, cwd: str) -> None:
        data_dir = cwd + '/data'
        data_subdir = os.listdir(data_dir)

        subdir_names = []

        for i in range(len(data_subdir)):
            # Only subdirectories?
            if os.path.isdir(data_dir + '/' + data_subdir[i]):
                # Only non-empty subdirectories
                if os.listdir(data_dir + '/' + data_subdir[i]):
                    subdir_names.append(data_subdir[i])

        self.subdir_names = subdir_names

        subdir_paths = {}
        for i in range(len(subdir_names)):
            subdir_paths[subdir_names[i]] = data_dir + '/' + subdir_names[i]
        
        self.subdir_paths = subdir_paths

        subdir_filenames = {}
        for i in range(len(subdir_names)):
            subdir_filenames[subdir_names[i]] = [os.path.basename(x) for x in glob.glob(self.subdir_paths[subdir_names[i]] + '/*.png')]
        
        self.subdir_filenames = subdir_filenames

        subdir_paths_of_filenames = {}
        for i in range(len(subdir_names)):
            temp_lst = []
            for j in range(len(self.subdir_filenames[subdir_names[i]])):
                temp_lst.append(self.subdir_paths[subdir_names[i]] + '/' + self.subdir_filenames[subdir_names[i]][j])
            subdir_paths_of_filenames[subdir_names[i]] = temp_lst

        self.subdir_paths_of_filenames = subdir_paths_of_filenames   

    ''' ---------------
        Function to return a list of the filenames in a given subdirectory 
    '''
    def get_subdir_filenames(self, subdirname) -> list:
        try:
            filenames = []
            assert subdirname in self.subdir_names, "No subdirectory with this name!"
            filenames = self.subdir_filenames[subdirname]
            return filenames
        except AssertionError as msg:
            print(msg)
      
    ''' ---------------
        Function to get lists of the desired files in given subdirectory
        in form of numpy-arrays from cv.imread
        - img_of_files: list of the names of the images as string
    '''
    def make_img_list(self, subdirname) -> list:
        try:
            img_of_files = []
            assert subdirname in self.subdir_names, "No subdirectory with this name!"
            num_files = len(self.subdir_filenames[subdirname])
            for i in range(num_files):
                img = cv.imread(self.subdir_paths_of_filenames[subdirname][i])
                img_of_files.append(img)

            return img_of_files
        except AssertionError as msg:
            print(msg)
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
