import pandas as pd
import numpy as np
from skimage.measure import regionprops, regionprops_table

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
    "custom_all": ["intensity_total"],
}

def featurize_image(img, mask, features=["default"], feature_table_output_path=False):
    """
    docstring here.
    """
    properties = ["label"]  # always want to include label
    for feature in features:
        properties += dictionary_feature_to_properties[feature]
    # partition properties into built-into-scikit vs custom
    scikit_properties = []
    custom_properties = []
    for property in properties:
        if property in dictionary_feature_to_properties["scikit_all"]:
            scikit_properties.append(property)
        elif property in dictionary_feature_to_properties["custom_all"]:
            function = dictionary_custom_property_to_function[property]
            custom_properties.append(function)
        else:
            print(
                f"Warning:{property} is not supported by scikit-image or custom, removing from table."
            )

    try:
        feature_table = pd.DataFrame(
            regionprops_table(
                mask,
                img,
                properties=scikit_properties,
                extra_properties=custom_properties,
            )
        )
    except AttributeError as e:
        raise NotImplementedError(f"{e.name} is not supported for this image type")

    if feature_table_output_path:
        feature_table.to_csv(
            feature_table_output_path, header=True, index=False, mode="w"
        )
    return feature_table


# Write custom features here
def intensity_total(region, intensities):
    return np.sum(intensities[region])


# vz:can turn this into a class/decorator situation so that the dictionary is automatically generated when developer or user add new custom property
dictionary_custom_property_to_function = {"intensity_total": intensity_total}
