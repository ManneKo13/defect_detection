from ast import Assert
import os
import glob
import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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
        Are described above.
'''
class DataFiles():
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
        Function returns the bgr-format from opencv.imread from a specific filename.
        - subdirname: name of the subdirectory which contains the desired image
        - filename: the image from whom we want the bgr-format
    '''
    def get_img_from_filename(self, subdirname, filename):
        try:
            assert subdirname in self.subdir_names, "No subdirectory with this name!"
            assert filename in self.subdir_filenames[subdirname], "No file in directory {} with this name!".format(subdirname)
            img_index = self.subdir_filenames[subdirname].index(filename)
            img_bgr = cv.imread(self.subdir_paths_of_filenames[subdirname][img_index])
            return img_bgr
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

    ''' ---------------
        Provides a simple plot of a specific image, given by an filename,
        in a given subdirectory.
    '''
    def plot_specific_image_by_name(self, subdirname, imagename):
        try:
            assert subdirname in self.subdir_names, "No subdirectory with this name!"
            assert imagename in self.subdir_filenames[subdirname], "No file with this name in subdirectory {}".format(subdirname)
            img = cv.imread(self.subdir_paths[subdirname] + '/' + imagename)
            rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            fig, ax = plt.subplots(figsize = (12, 8), layout = 'constrained')
            ax.set_title('Image: {} in folder: {}'.format(imagename, subdirname))
            ax.imshow(rgb_img)
            move_figure(fig, 0, 0)
            plt.show()
        except AssertionError as msg:
            print(msg)

    ''' ---------------
        Provides a simple plot of a specific image, given in bgr-format.
    '''
    def plot_specific_image(self, img):
            rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            fig, ax = plt.subplots(figsize = (12, 8), layout = 'constrained')
            ax.set_title('Image')
            ax.imshow(rgb_img)
            move_figure(fig, 0, 0)
            plt.show()
    ''' ---------------
    Function to plot two images in numpyarray-format, this function should be
    used to compare those two images.
    - img1: image on the left side of the subplot in bgr-format from opencv.imread
    - img2: image on the right side of the subplot in bgr-format from opencv.imread
    - imagename: str of the left-side imagename
    - description: str of possible modification of the right-side image
    '''
    def plot2img(self, 
                 img1_bgr, 
                 img2_bgr, 
                 imagename, 
                 description):

        rgb_img1 = cv.cvtColor(img1_bgr, cv.COLOR_BGR2RGB)
        rgb_img2 = cv.cvtColor(img2_bgr, cv.COLOR_BGR2RGB)
        fig = plt.figure(figsize = (12, 8))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ax1.imshow(rgb_img1), ax1.set_title('Original ({}) '.format(imagename))
        ax2.imshow(rgb_img2), ax2.set_title('Output (%s)' % description)
        move_figure(fig, 0, 0)
        plt.show()
    
    ''' ---------------
        Same method as "plot2img" but one can plot four images in one figure.
        This method was meant to plot one original image and three different 
        modifications of that image.
        - img1: originial image in the upper left corner in bgr-format from opencv.imread
        - img2-img4: modified images in bgr-format from opencv.imread
        - imagename: str of the original image
        - descriptions: list how img2-img4 are modified in the corresponding order
    '''
    def plotThreeOutputs(self,
                         img1_bgr, 
                         img2_bgr, 
                         img3_bgr, 
                         img4_bgr,
                         imagename: str,
                         descriptions: list):

        img1_rgb = cv.cvtColor(img1_bgr, cv.COLOR_BGR2RGB)
        img2_rgb = cv.cvtColor(img2_bgr, cv.COLOR_BGR2RGB)
        img3_rgb = cv.cvtColor(img3_bgr, cv.COLOR_BGR2RGB)
        img4_rgb = cv.cvtColor(img4_bgr, cv.COLOR_BGR2RGB)
        
        figure = plt.figure(figsize = (12, 8))
        ax = figure.subplots(2, 2)
        ax[0, 0].imshow(img1_rgb), ax[0, 0].set_title('Original ({})'.format(imagename))
        ax[0 ,1].imshow(img2_rgb), ax[0 ,1].set_title('Output ({})'.format(descriptions[0]))
        ax[1, 0].imshow(img3_rgb), ax[1, 0].set_title('Output ({})'.format(descriptions[1]))
        ax[1, 1].imshow(img4_rgb), ax[1, 1].set_title('Output ({})'.format(descriptions[2]))
        move_figure(figure, 0, 0)
        plt.show()

    ''' ---------------
        This method returns an grayscale image after using a CLAHE transform 
        in the bgr-format.
        - img: the bgr-image which should be transformed
        - clipLimit/tileGridSize: are used for the CLAHE object, since we are 
                                  using an adaptive histogram equalization 
    '''
    def get_Clahe_img_gray(self, img,  
                           clipLimit = 2.0, 
                           tileGridSize = (8, 8)):
        clahe = cv.createCLAHE(clipLimit = clipLimit,
                               tileGridSize = tileGridSize)
        # Convert the BGR images into the gray spaces 
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_gray_histeq = clahe.apply(gray_image)
        return cv.cvtColor(img_gray_histeq, cv.COLOR_GRAY2BGR)

    ''' ---------------
        This method returns an bgr-image after using a CLAHE transform in the value plane,
        of the correspondig HSV-image.
        - img: the bgr-image which should be transformed
        - clipLimit/tileGridSize: are used for the CLAHE object, since we are 
                                  using an adaptive histogram equalization 
    '''
    def get_Clahe_img_hsv(self, img,  
                          clipLimit = 2.0, 
                          tileGridSize = (8, 8)):
        clahe = cv.createCLAHE(clipLimit = clipLimit,
                               tileGridSize = tileGridSize)
        # Convert the BGR images into the hsv color spaces 
        hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        ''' ---------------
            Applying limited adaptive Histogram Equalization onto the
            layer which are describing the intensity of the image, in the
            corresponding color space.
        ''' 
        hsv_image[:,:,2] = clahe.apply(hsv_image[:,:,2])
        return cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)

    ''' ---------------
        This method returns an bgr-image after using a CLAHE transform in the value plane,
        of the correspondig HSV-image.
        - img: the bgr-image which should be transformed
        - clipLimit/tileGridSize: are used for the CLAHE object, since we are 
                                  using an adaptive histogram equalization 
    '''
    def get_Clahe_img_lab(self, img,  
                          clipLimit = 2.0, 
                          tileGridSize = (8, 8)):
        clahe = cv.createCLAHE(clipLimit = clipLimit,
                               tileGridSize = tileGridSize)
        # Convert the BGR images into the lab color spaces 
        lab_image = cv.cvtColor(img, cv.COLOR_BGR2Lab)
        lab_image[:,:,0] = clahe.apply(lab_image[:,:,0])
        return cv.cvtColor(lab_image, cv.COLOR_Lab2BGR)    
    
    def get_Clahe_img_yuv(self, img,  
                          clipLimit = 2.0, 
                          tileGridSize = (8, 8)):
        clahe = cv.createCLAHE(clipLimit = clipLimit,
                               tileGridSize = tileGridSize)
        # Convert the BGR images into the lab color spaces 
        lab_image = cv.cvtColor(img, cv.COLOR_BGR2YUV)
        lab_image[:,:,0] = clahe.apply(lab_image[:,:,0])
        return cv.cvtColor(lab_image, cv.COLOR_YUV2BGR)    
    
    ''' ---------------
        This method returns an bgr-image after using a standard 
        histogram equalization with equalizeHist in the value plane,
        of the correspondig HSV-image.
        - img: the bgr-image which should be transformed
    '''        
    def get_EqualHist_img(self, img):
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        img_hsv[:,:,2] = cv.equalizeHist(img_hsv[:,:,2])
        return cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR)