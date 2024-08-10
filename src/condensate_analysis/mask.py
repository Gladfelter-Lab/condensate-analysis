from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label

def mask_image(img, threshold_method="otzu", watershed=True):
    thresh = apply_threshold(img, threshold_method)
    binary = img > thresh
    no_edge_binary = clear_border(binary)
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
    coords = peak_local_max(distance, footprint=np.ones((25, 25)), labels=binary)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels = watershed(-distance, markers, mask=binary)
    mask = label
    return label_watershed