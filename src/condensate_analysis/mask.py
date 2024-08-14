from skimage.filters import threshold_otsu
from skimage import segmentation
from skimage.measure import label
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import numpy as np
import os
import czifile
import json

# Aim to reduce variety of dependencies imported

# Add option to specify whether to use FULLSTACK, MAXPROJ if stack is provided. 
# Write method for each.

# Add option for background subtraction.
# Consult Wilton on whether to use single value or also allow other method to be specified. 

#user_input_path can be a directory with image files or an image file
def input_image(configuration_file,user_input_path):
    configure(configuration_file)
    #bulk processing images in a folder
    if os.path.isdir(user_input_path):
       for filename in os.listdir(user_input_path):
           image_file_path = os.path.join(user_input_path, filename)
           if check_image_file_type(image_file_path)==True:
               image_raw_array = czifile.imread(image_file_path)
               with czifile.CziFile(image_file_path) as czi:
                xml_metadata = czi.metadata()
               
    #processing a single image file
    elif os.path.isfile(user_input_path):
        if check_image_file_type(user_input_path)==True:
            image_raw_array = czifile.imread(user_input_path)
            with czifile.CziFile(user_input_path) as czi:
                xml_metadata = czi.metadata()
    else:
        print("Error: user input path is not a directory nor a file.")
    return image_raw_array,xml_metadata

supported_configuration_parameters={
    "threshold_method": ["otsu"],
    "is_watershed": [True,False],
    "stacks_option": ["full_stack","max_projection_protein","max_projection_rna"],
    "is_background_subtraction":[True,False],
    "background_subtraction_model":["wilton1","wilton2"]}

#example of configuration file (json)
## to be consistent, might need to change to xml bc metadata is written in xml
#  "config_parameters":[] 
#     {
#       "threshold_method": "otsu",
#       "is_watershed": False,
#       "stacks_option": "maxprojection",
#       "is_background_subtraction"=True,
#       "background_subtraction_model"="wilton1"
#       "area_threshold"=20
#     }
#]

#default parameters if none is specified 
default_threshold_method="otsu"
default_is_watershed=False
default_stacks_option="max_projection_protein"
default_is_background_subtraction=True
default_background_subtraction_model="wilton1"

def configure (configuration_file):
    try:
        with open(configuration_file, 'r') as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {configuration_file} was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error:The file {configuration_file} is not a valid JSON file.")
    
    config_params = config_data['config_parameters'][0]
    threshold_method = config_params.get('threshold_method', default_threshold_method)
    is_watershed = config_params.get('is_watershed', default_is_watershed)
    stacks_option = config_params.get('stacks_option', default_stacks_option)
    is_background_subtraction = config_params.get('is_background_subtraction', default_is_background_subtraction)
    background_subtraction_model=config_params.get('background_subtraction_model', default_background_subtraction_model)

def check_image_file_type (file_path):
    supporting_image_file_type=[".czi",".nd2",".tiff"]
    file_type = os.path.splitext(file_path)[1]
    if file_type not in supporting_image_file_type:
        return True
    else:
        print(f"Warning: {file_path} doesn't have a supported image file type, skipping...")
        return False
    
def print_image_info(image_raw_array):
    print("shape: {}".format(image_raw_array.shape))
    print("dtype: {}".format(image_raw_array.dtype))
    print("range: ({}, {})".format(np.min(image_raw_array), np.max(image_raw_array)))

def parse_metadata(xml_metadata):
    root_metadata = ET.fromstring(xml_metadata)
    # print(ET.tostring(root, encoding='utf8').decode('utf8'))
    #rescale to µM
    pixel_size_x = float(root_metadata.find('.//Scaling/Items/Distance[@Id="X"]/Value').text)*1E6
    pixel_size_y = float(root_metadata.find('.//Scaling/Items/Distance[@Id="Y"]/Value').text)*1E6
    pixel_size_z = float(root_metadata.find('.//Scaling/Items/Distance[@Id="Z"]/Value').text)*1E6

    print("pixel_size_x: {}".format(pixel_size_x) + " µm")
    print("pixel_size_y: {}".format(pixel_size_y) + " µm")
    print("pixel_size_z: {}".format(pixel_size_z) + " µm")

def apply_stack(image_raw_array,stack_option):
    if stack_option=="full_stack":
        return image_raw_array
    if stack_option=="max_projection_protein":
        protein_brightest_frame, rna_brightest_frame=max_projection(image_raw_array)
        return protein_brightest_frame
    if stack_option=="max_projection_rna":
        protein_brightest_frame, rna_brightest_frame=max_projection(image_raw_array)
        return rna_brightest_frame
    else:
        print(f"Warning: stack option specified by user is not one of the supported option:{supported_configuration_parameters["stack_option"]}, using deafult stack option {default_stacks_option} instead.")

def max_projection(image_raw_array):
    protein = image_raw_array[0,0,0,:,:,:,0]
    rna = image_raw_array[0,0,1,:,:,:,0]
    protein_max = np.max(protein, axis=0)
    rna_max = np.max(rna, axis=0)
    # get brightest single frames (based on prt ch intensity)
    nframes = len(protein)
    frame_average_protein = []
    frame_average_rna = []
    for frame in range(nframes):
    # plt.imshow(prt[frame,:,:], cmap='rainbow')
    # plt.title('protein frame {}'.format(frame))
    # plt.axis('off')
    # plt.show()
        frame_average_protein.append(np.mean(protein[frame,:,:]))
        frame_average_rna.append(np.mean(rna[frame,:,:]))
    # sns.scatterplot(x=frame_average_protein,y=frame_average_rna)
    # plt.xlabel('protein intensity')
    # plt.ylabel('RNA intensity')
    # plt.show()
    brightest_frame_index = frame_average_protein.index(max(frame_average_protein))
    protein_brightest_frame = protein[brightest_frame_index,:,:]
    rna_brightest_frame = rna[brightest_frame_index,:,:]
    return protein_brightest_frame,rna_brightest_frame

def apply_background_subtraction(image, background_subtraction_model):
    if background_subtraction_model=="":
    
    else:
        print(f"Warning: background subtraction model specified by user is not one of the supported model:{supported_configuration_parameters["background_subtraction_model"]}, using deafult background subtraction model {default_background_subtraction_model} instead.")
    return image_subtracted_array

def mask_image(image_raw_array, threshold_method, is_watershed,stacks_option,is_background_subtraction,background_subtraction_model):
    image_stack_array=apply_stack(image_raw_array)
    if is_background_subtraction:
        image_stack_subtracted_array=apply_background_subtraction(image_stack_array,background_subtraction_model)
    thresh = apply_threshold(image_stack_subtracted_array, threshold_method)
    binary = image_stack_array > thresh
    no_edge_binary = segmentation.clear_border(binary)
    mask = label(no_edge_binary)
    if is_watershed:
        mask = apply_watershed(binary)
    return mask

def apply_threshold(image_array, threshold_method):
    if threshold_method == "otsu":
        threshold_image_array = threshold_otsu(image_array)
    else:
        print(f"Warning: threshold method specified by user is not one of the supported method:{supported_configuration_parameters["threshold_method"]}, using deafult threshold method {default_threshold_method} instead.")
        threshold_image_array = threshold_otsu(image_array)
    return threshold_image_array

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



