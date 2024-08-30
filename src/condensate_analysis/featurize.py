import pandas as pd
import numpy as np
from skimage.measure import regionprops, regionprops_table


def featurize(img, mask, feature_options, export_path=""):
    ### list of built-in properties: https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.regionprops
    
    ### features that are always included:
    properties = ['label']
    extra_properties = []
    
    ### features related to size:
    if feature_options['size']:
        properties = properties + ['area', 'num_pixels']
    
    ### features related to intensity:
    if feature_options['intensity']:
        properties = properties + ['max_intensity', 'mean_intensity', 'min_intensity']

        def total_intensity(region, intensities): #we could leave smaller functions inside and define larger ones
            return np.sum(intensities[region])    #down below, or we could move all of them below
        
        def std_intensity(region, intensities): 
            return np.std(intensities[region])
        
        extra_properties.append(total_intensity)
        extra_properties.append(std_intensity)
    
    ### features related to shape:
    if feature_options['shape']:
        properties = properties + ['centroid', 'axis_major_length']

    ### creating table of features:
    feature_table = pd.DataFrame(regionprops_table(mask, img, properties=properties, 
                                                   extra_properties=extra_properties))

    ### exporting csv features to specified loccation:
    if export_path:
        feature_table.to_csv(export_path, header=True, index=False, mode="w")

    return feature_table
    
### gm: commenting out previous:   
    # """generate feature table.
    # --- parameters ---
    # - img: img array, must be the same dimension as mask
    # - mask: value returned from mask_image
    # - features:"default" or list of features
    # - feature_table_output_path: False or output_path
    # """
    # # might need to add in stack option for which img stack to featurize

    # builtin_features = []
    # custom_features = []
    # if features == "default":
    #     builtin_features = [
    #         "label",
    #         "slice",
    #         "area",
    #         "centroid",
    #         "mean_intensity",
    #         "eccentricity",
    #     ]
    # # Need way to split builtin and custom features. Loop over and decide whether to use custom.
    # else:
    #     # vita: i think we have to run regionprops first in order to find out supported properties in order to split between built in and custom, but we can run it only if it's not default features.
    #     supported_builtin_properties = []
    #     # needs to define supported_custom_features
    #     supported_custom_features = []

    #     regionprops = regionprops(mask, intensity_image=img)
    #     for prop in regionprops[0]:
    #         try:
    #             regionprops[0][prop]
    #             supported_builtin_properties.append(prop)
    #         except NotImplementedError:
    #             pass
    #     for feature in features:
    #         if feature in supported_builtin_properties:
    #             builtin_features.append(feature)
    #         elif feature in supported_custom_features:
    #             custom_features.append(feature)
    #         else:
    #             print(
    #                 f"Warning: {feature} is not supported, and will not be generated."
    #             )

    # feature_table = pd.DataFrame(
    #     regionprops_table(
    #         label_image=mask,
    #         intensity_image=img,
    #         properties=builtin_features,
    #         extra_properties=custom_features,
    #     )
    # ).set_index("label")

    # if feature_table_output_path:
    #     feature_table.to_csv(
    #         feature_table_output_path, header=True, index=False, mode="w"
    #     )

    # return feature_table


# Write custom features here
