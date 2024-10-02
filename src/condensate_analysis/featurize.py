import pandas as pd
import numpy as np
from skimage.measure import regionprops, regionprops_table
from feature_dict import *

def featurize_image(img, mask, features=["default"], custom_features=None, feature_table_output_path=False):
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
    if custom_features:
        custom_properties.append(custom_features)
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
