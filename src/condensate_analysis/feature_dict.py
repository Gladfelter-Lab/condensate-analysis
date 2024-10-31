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
    # Get the centroid coordinates
    point = ndimage.center_of_mass(mask)
    round_point = [int(round(elem, 0)) for elem in point]
    
    # Define the dimensions of the image
    img_shape = img.shape
    
    def is_within_bounds(coords):
        """Check if the given coordinates are within the image bounds."""
        return all(0 <= coords[i] < img_shape[i] for i in range(len(coords)))
    
    # Handle 2D images
    if len(round_point) == 2:
        neighbors = [
            (0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)
        ]
        intensity_values = []
        for dx, dy in neighbors:
            new_point = (round_point[0] + dx, round_point[1] + dy)
            if is_within_bounds(new_point):
                intensity_values.append(img[new_point[0], new_point[1]])
        
        intensity = int(sum(intensity_values) / len(intensity_values)) if intensity_values else 0
    
    # Handle 3D images
    elif len(round_point) == 3:
        neighbors = [
            (0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
        intensity_values = []
        for dx, dy, dz in neighbors:
            new_point = (round_point[0] + dx, round_point[1] + dy, round_point[2] + dz)
            if is_within_bounds(new_point):
                intensity_values.append(img[new_point[0], new_point[1], new_point[2]])
        
        intensity = int(sum(intensity_values) / len(intensity_values)) if intensity_values else 0
    
    return intensity

# vz:can turn this into a class/decorator situation so that the dictionary is automatically generated when developer or user add new custom property
dictionary_custom_property_to_function = {"intensity_total": intensity_total, "centroid_info":centroid_info}

