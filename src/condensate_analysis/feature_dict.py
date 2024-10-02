import numpy as np 
from scipy import ndimage

dictionary_feature_to_properties = {
    "default": ["label", "slice", "area", "centroid", "intensity_mean", "eccentricity"],
    "size": ["area", "num_pixels"],
    "shape": ["centroid", "axis_major_length"],
    "area": ["area", "area_bbox", "area_convex", "area_filled"],
    "axis": ["axis_major_length", "axis_minor_length"],
    "centroid": [
        "centroid",
        "centroid_local",
        "centroid_weighted",
        "centroid_weighted_local",
    ],
    "coords": ["coords", "coords_scaled"],
    "image": ["image", "image_convex", "image_filled", "image_intensity"],
    "inertia": ["inertia_tensor", "inertia_tensor_eigvals"],
    "intensity": [
        "image_intensity",
        "inertia_tensor",
        "inertia_tensor_eigvals",
        "intensity_max",
        "intensity_mean",
        "intensity_min",
        "intensity_std",
    ],
    "moments": [
        "moments",
        "moments_central",
        "moments_hu",
        "moments_normalized",
        "moments_weighted",
        "moments_weighted_central",
        "moments_weighted_hu",
        "moments_weighted_normalized",
    ],
    "misc": [],
    "scikit_all": [
        "area",
        "area_bbox",
        "area_convex",
        "area_filled",
        "axis_major_length",
        "axis_minor_length",
        "bbox",
        "centroid",
        "centroid_local",
        "centroid_weighted",
        "centroid_weighted_local",
        "coords",
        "coords_scaled",
        "eccentricity",
        "equivalent_diameter_area",
        "euler_number",
        "extent",
        "feret_diameter_max",
        "image",
        "image_convex",
        "image_filled",
        "image_intensity",
        "inertia_tensor",
        "inertia_tensor_eigvals",
        "intensity_max",
        "intensity_mean",
        "intensity_min",
        "intensity_std",
        "label",
        "moments",
        "moments_central",
        "moments_hu",
        "moments_normalized",
        "moments_weighted",
        "moments_weighted_central",
        "moments_weighted_hu",
        "moments_weighted_normalized",
        "num_pixels",
        "orientation",
        "perimeter",
        "perimeter_crofton",
        "slice",
        "solidity",
    ],
   "custom_all": ["intensity_total", "area", "centroid_info"],
}

# Write custom features here
def intensity_total(region, intensities):
    return np.sum(intensities[region])
def centroid_info(mask, img):
    point = ndimage.center_of_mass(mask)
    round_point = [ int(round(elem, 0)) for elem in point ]
    if len(round_point) == 2 : 
        intensity = int(img[round_point[0], round_point[1]])
                       #img[round_point[0]+1, round_point[1]] +
                       #img[round_point[0], round_point[1]+1]+
                       #img[round_point[0]-1, round_point[1]]+
                       #img[round_point[0], round_point[1]-1]/ 5)
    elif len(round_point) == 3:
        intensity = int(img[round_point[0], round_point[1], round_point[2]])
                       #img[round_point[0], round_point[1]+1, round_point[2]] +
                       #img[round_point[0], round_point[1]-1, round_point[2]] +
                       #img[round_point[0], round_point[1], round_point[2]+1] +
                       #img[round_point[0], round_point[1], round_point[2]-1]/5)
    return intensity


# vz:can turn this into a class/decorator situation so that the dictionary is automatically generated when developer or user add new custom property
dictionary_custom_property_to_function = {"intensity_total": intensity_total, "centroid_info":centroid_info}

