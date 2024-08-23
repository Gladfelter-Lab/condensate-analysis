import pandas as pd
from skimage.measure import regionprops_table

def featurize(img, mask, features="default"):
    if features == "default":
        features = ['label', 'slice', 'area', 'centroid', 'mean_intensity', 'eccentricity']
    # Need way to split builtin and custom features. Loop over and decide whether to use custom.
    
    feat_table = pd.DataFrame(ski.measure.regionprops_table(mask, intensity_image=img
                properties=builtin_features, extra_properties=custom_features)
            ).set_index('label')

    return feat_table

# Write custom features here