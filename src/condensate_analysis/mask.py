from skimage.filters import threshold_otsu
from skimage import segmentation
from skimage.measure import label
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import numpy as np
import os
import czifile
import json

#example of configuration file (json)
#  "config_parameters":[] 
#     {
#       "threshold_method": "otzu",
#       "is_watershed": False,
#       "stacks_option": "maxproject",
#       "is_background_subtraction"=True
#     }
#]

supported_configuration_parameters={
    "threshold_method": ["otzu"],
    "is_watershed": [True,False],
    "stacks_option": ["fullstack","brightest","maxproject"],
    "is_background_subtraction":[True,False]}
#default parameters if none is specified 
default_threshold_method="otzu"
default_is_watershed=False
default_stacks_opiton="maxprojection"
default_is_background_subtraction=True

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

def configure (configuration_file)
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    config_params = config_data['config_parameters'][0]
    threshold_method = config_params.get('threshold_method', default_threshold_method)
    is_watershed = config_params.get('is_watershed', default_is_watershed)
    stacks_option = config_params.get('stacks_option', default_stacks_opiton)
    is_ackground_subtraction = config_params.get('is_background_subtraction', default_is_background_subtraction)

def mask_image(image_raw_array, threshold_method=threshold_method, watershed=is_watershed):
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
