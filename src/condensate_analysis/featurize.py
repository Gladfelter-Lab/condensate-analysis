

def featurize(img, mask):
    # 
    regionprops = ski.measure.regionprops(mask, intensity_image=img)
    # apply mask
    # extract features
    # return table
    return features