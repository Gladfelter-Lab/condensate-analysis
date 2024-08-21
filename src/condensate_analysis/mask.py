from skimage.filters import threshold_otsu
from skimage import segmentation
from skimage.measure import label
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import numpy as np

# Aim to reduce variety of dependencies imported

# Add option to specify whether to use FULLSTACK, MAXPROJ if stack is provided. 
# Write method for each.

# Consult Wilton on whether to use single value or also allow other method to be specified. 

def mask_image(image, threshold_method="otsu", watershed=False, background_sub=False, clear_border=True):
    if background_sub:
        image = _apply_background(image, background_sub)
    thresh = _apply_threshold(image, threshold_method)
    binary = image > thresh
    # Need to replace clear_border option with new clear_border function capable only ONLY clearing XY border, not Z border. 
    if clear_border:
        binary = segmentation.clear_border(binary)
    mask = label(binary)
    if watershed:
        mask = _apply_watershed(binary)
    return mask

def _apply_threshold(image_array, method):
    if method == "otsu":
        thresh = threshold_otsu(image_array)
    else:
        print(f"Warning: threshold method specified by user is not one of the supported method, using deafult threshold method otzu method instead.")
        thresh = threshold_otsu(image_array)
    return thresh

def _apply_watershed(binary):
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

def _apply_background(image, method):
    if method=="median":
        background = np.median(image)
        subtracted_image = image - background
    return subtracted_image