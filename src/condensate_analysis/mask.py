from skimage.filters import threshold_otsu
from skimage import segmentation
from skimage.measure import label
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import numpy as np
import os
import czifile

#example of configuration file (json)
#  "config_parameters": [
#     {
#       "threshold_method": "otzu",
#       "watershed_binary": False,
#       "stacks_option": "maxproject",
#       "background_subtraction_binary"=True
#     }]


# Aim to reduce variety of dependencies imported

# Add option to specify whether to use FULLSTACK, BRIGHTEST, MAXPROJ if stack is provided. 
# Write method for each.

# Add option for background subtraction.
# Consult Wilton on whether to use single value or also allow other method to be specified. 

#user_input_path can be a directory with image files or an image file
def input_image(configuration_file,user_input_path):
    configure(configuration_file)
    #bulk processing images in a folder
    if os.path.isdir(user_input_path):
       for filename in os.listdir(user_input_path):
           image_file_path = os.path.join(user_input_path, filename)
           if check_file_type(image_file_path)==True:
               image_raw_array = czifile.imread(image_file_path)
               
    #processing a single image file
    elif os.path.isfile(user_input_path):
        if check_file_type(user_input_path)==True:
            image_raw_array = czifile.imread(user_input_path)
    else:
        print("Error: user input path is not a directory nor a file.")
    return image_raw_array

def check_file_type (file_path):
    supporting_image_file_type=[".czi",".nd2",".tiff"]
    file_type = os.path.splitext(file_path)[1]
    if file_type not in supporting_image_file_type:
        return True
    else:
        print(f"Warning: {file_path} doesn't have a supported image file type, skipping...")
        return False

def print_image_info(image_raw_array):
    print("shape: {}".format(image_raw_array.shape))
    print("dtype: {}".format(image_raw_array.dtype))
    print("range: ({}, {})".format(np.min(image_raw_array), np.max(image_raw_array)))

def configure (configuration_file):
    #parameters to specify, can all become read in from the configuration file eventually
    threshold_method_list=["otzu"]
    threshold_method="otzu"
    #watershed True/False
    watershed_binary=False
    stacks_option_list=["fullstack","brightest","maxproject"]
    stacks_opiton=""
    #background_subtraction True/False
    background_subtraction_binary=True


def mask_image(image_raw_array, threshold_method=threshold_method, watershed=watershed_parameter):
    thresh = apply_threshold(image_raw_array, threshold_method)
    binary = image_raw_array > thresh
    no_edge_binary = segmentation.clear_border(binary)
    label_image = label(no_edge_binary)
    if watershed:
        mask = apply_watershed(binary)
    elif not watershed :
        mask = label_image
    return mask

def apply_threshold(img, method):
    if method == "otzu":
        thresh = threshold_otsu(img)
    return thresh

def apply_watershed(binary):
    distance = ndi.distance_transform_edt(binary)
    distance = ndi.gaussian_filter(distance,5)
    # Consider allowing user defined watershed distance. watershed=value accepted as well as False (none) and True (auto)
    coords = peak_local_max(distance, footprint=np.ones((25, 25)), labels=binary)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels = segmentation.watershed(-distance, markers, mask=binary)
    mask = label
    return labels

def apply_stack():

def apply_background_subtraction():
