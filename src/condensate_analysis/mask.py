from skimage.filters import threshold_otsu
from skimage import segmentation
from skimage.measure import label
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import numpy as np
# Aim to reduce variety of dependencies imported

# Add option to specify whether to use FULLSTACK, BRIGHTEST, MAXPROJ if stack is provided. 
# Write method for each.

# Add option for background subtraction.
# Consult Wilton on whether to use single value or also allow other method to be specified. 


def mask_image(img, threshold_method="otzu", watershed=False):
    thresh = apply_threshold(img, threshold_method)
    binary = img > thresh
    no_edge_binary = segmentation.clear_border(binary)
    label_image = label(no_edge_binary)
    if watershed == True:
        mask = apply_watershed(binary)
    elif watershed == False:
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