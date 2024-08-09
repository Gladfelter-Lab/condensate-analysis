import skimage
import nd2
import czifile

def read_image(file):
    """Read image into numpy ndarray.

    Should handle nd2, czi, tif, and other common file type.
    Handling is based on file extention only.
    Dimension order is set with the convention: Channel, Slice, Row, Col.
    """
    if file.endswith(".czi"):
        img = czifile.imread(file).squeeze() # remove dummy dimensions
    elif file.endswith(".nd2"):
        img = nd2.imread(file)
        img = img.swapaxes(0,1) # places channel before slice
    else:
        try:
            img = skimage.io.imread(file)
            img = img.swapaxes(0,1) # I think this is also necessary here, but not sure. 
            # Consider checking for larger value between slice and channel for placement.
        except OSError:
            print("Invalid file extention")
    return img