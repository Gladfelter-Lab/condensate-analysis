from skimage.filters import threshold_otsu
from skimage import segmentation
from skimage.measure import label
from skimage.color import label2rgb
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import numpy as np

# Review dependencies, are all necessary?

# Add option to specify whether to use FULLSTACK, MAXPROJ if stack is provided.
# Write method for each.

# Consult Wilton on whether to use single value or also allow other method to be specified.

# Replace "watershed" with "splitting" option, mulitple methods supported. What other methods?


def mask_image(
    image,
    stack=False,
    threshold="otsu",
    watershed=False,
    background_sub=False,
    clear_border=True,
):
    """Create and return a 2D or 3D mask from an input image.
    --- parameters ---
    - image: ndarray of two or three dimensions
    - stack: False, "protein_max_project","rna_max_project","protein_brightest_frame","rna_brightest_frame"
    - threshold: integer value specifying threshold or name of method to determine threshold ("otsu")
    - watershed: False or value specifying watershed footprint size.
    - background_sub: False or "median", which subtracts median pixel value, are currently supported
    - clear_border: boolean for whether condensates touching image edges should be included in mask.
        May need to use False with 3D images right now since blobs often touch top or bottom of Z-stack.

    """
    if stack:
        image = _get_stack(image, stack)
    if background_sub:
        image = _apply_background(image, background_sub)
    thresh = _get_threshold(image, threshold)
    binary = image > thresh
    # Need to replace clear_border option with new clear_border function capable only ONLY clearing XY border, not Z border.
    if watershed:
        mask = _apply_watershed(binary, watershed)
    if clear_border:
        mask = segmentation.clear_border(mask)
    else:
        mask = label(binary)
    rgb_mask  = label2rgb(mask, bg_label=0)
    return mask, rgb_mask


def _get_stack(image_array, stack):
    #gm: Right now there is a lot being computed here that isn't necessarily being 
    #    used. Also we should try to use numpy functions instead of python loops when 
    #    ever possible (for example, I think we can do np.mean across the frame axis 
    #    instead of the for loop). I think we should talk through on a higher level what 
    #    we want _get_stack to do, then we can figure out how to organize this
    protein = image_array[1, :]
    rna = image_array[0, :]
    # get brightest single frames (based on protein or rna ch intensity)
    #do we need other options such as (give rna channel where correponding protein channel is the brightest frame, part of Wil's code)
    if stack == "protein_max_project":
         # protein_max_project
        protein_max = np.max(protein, axis=0)
        image_array = protein_max
    elif stack == "rna_max_project":
        # rna_max_project
        rna_max = np.max(rna, axis=0)
        image_array = rna_max
    elif stack == "protein_brightest_frame":
        frame_mean_protein = np.mean(protein, axis=(1, 2))
        protein_brightest_frame_index = np.argmax(frame_mean_protein)
        protein_brightest_frame = protein[protein_brightest_frame_index, :, :]
        image_array = protein_brightest_frame
    elif stack == "rna_brightest_frame":
        frame_mean_rna = np.mean(rna, axis=(1, 2))
        rna_brightest_frame_index = np.argmax(frame_mean_rna)
        rna_brightest_frame = rna[rna_brightest_frame_index, :, :]
        image_array = rna_brightest_frame
    else:
        print(
            f"Warning: stack specified by user is not one of the supported stack, stack is not appplied."
        )
    return image_array


def _get_threshold(image_array, method):
    if method == "otsu":
        thresh = threshold_otsu(image_array)
    elif type(method) == int or type(method) == float:
        thresh = method
    else:
        print(
            f"Warning: threshold method specified by user is not one of the supported method, using deafult threshold method otsu method instead."
        )
        thresh = threshold_otsu(image_array)
    return thresh


def _apply_watershed(binary, ws_size):
    distance = ndi.distance_transform_edt(binary)
    distance = ndi.gaussian_filter(distance, 5)
    # Consider allowing user defined watershed distance. watershed=value accepted as well as False (none) and True (auto)
    dims = len(binary.shape)
    coords = peak_local_max(
        distance, footprint=np.ones([ws_size] * dims), labels=binary
    )
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels = segmentation.watershed(-distance, markers, mask=binary)
    # mask = label ##gm: not sure what this is doing, commented it out
    return labels


def _apply_background(image, method):
    if method == "median":
        background = np.median(image)
        subtracted_image = image - background
    return subtracted_image
