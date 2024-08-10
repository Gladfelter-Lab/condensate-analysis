from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label

def mask_image(img, threshold_method="otzu", watershed=True):
    if threshold_method == "otzu":
        thresh = threshold_otsu(img)
    binary = img > thresh
    no_edge_binary = clear_border(binary)
    label_image = label(no_edge_binary)
    mask = label_image
    return mask