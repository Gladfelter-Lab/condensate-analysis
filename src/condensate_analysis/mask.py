from skimage.filters import threshold_otsu
from skimage import segmentation
from skimage.measure import label
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import numpy as np

# Review dependencies, are all necessary?

# Add option to specify whether to use FULLSTACK, MAXPROJ if stack is provided. 
# Write method for each.

# Consult Wilton on whether to use single value or also allow other method to be specified. 

# Replace "watershed" with "splitting" option, mulitple methods supported. What other methods? 

def mask_image(image, threshold="otsu", watershed=False, background_sub=False, clear_border=True):
    """Create and return a 2D or 3D mask from an input image.
    --- parameters --- 
    - image: ndarray of two or three dimensions
    - threshold: integer value specifying threshold or name of method to determine threshold ("otsu")
    - watershed: False or value specifying watershed footprint size.
    - background_sub: False or "median", which subtracts median pixel value, are currently supported
    - clear_border: boolean for whether condensates touching image edges should be included in mask. 
        May need to use False with 3D images right now since blobs often touch top or bottom of Z-stack.
    
    """
    if background_sub:
        image = _apply_background(image, background_sub)
    thresh = _get_threshold(image, threshold)
    binary = image > thresh
    # Need to replace clear_border option with new clear_border function capable only ONLY clearing XY border, not Z border. 
    if clear_border:
        binary = segmentation.clear_border(binary)
    if watershed:
        mask = _apply_watershed(binary, watershed)
    else:
        mask = label(binary)
    return mask

def _get_threshold(image_array, method):
    if method == "otsu":
        thresh = threshold_otsu(image_array)
    elif type(method)==int or type(method)==float:
        thresh = method
    else:
        print(f"Warning: threshold method specified by user is not one of the supported method, using deafult threshold method otsu method instead.")
        thresh = threshold_otsu(image_array)
    return thresh

def _apply_watershed(binary, ws_size):
    distance = ndi.distance_transform_edt(binary)
    distance = ndi.gaussian_filter(distance,5)
    # Consider allowing user defined watershed distance. watershed=value accepted as well as False (none) and True (auto)
    dims = len(binary.shape)
    coords = peak_local_max(distance, footprint=np.ones([ws_size]*dims), labels=binary)
    mask = np.zeros(distance.shape, dtype=bool)
    print(mask.shape)
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