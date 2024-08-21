import pandas as pd
def featurize(img, mask):
    regionprops = ski.measure.regionprops(mask, intensity_image=img)
    supported_features_list = []
    unsupported_features_list = []
    #set parameters
    # remove objects with area < area_threshold pixels
    area_threshold=20

    # list regionprops options for storing in info_table
    for prop in regionprops[0]:
        try:
            regionprops[0][prop]
            supported_features_list.append(prop)
        except NotImplementedError:
            unsupported_features_list.append(prop)

        # print("Supported properties:")
        # print("  " + "\n  ".join(supported_features_list))
        # print()
        # print("Unsupported properties:")
        # print("  " + "\n  ".join(unsupported_features_list))

        # create info table
        df_info_table = pd.DataFrame(ski.measure.regionprops_table(labels, prt_MAX_bs1,
                properties=['label', 'slice', 'area', 'centroid', 'mean_intensity', 'eccentricity'])
            ).set_index('label')

        df_info_table = df_info_table.drop(df_info_table[df_info_table.area < area_threshold].index) 
        df_info_table['area'] = df_info_table['area'].apply(lambda x: x*pxlsz_x**2) # rescale areas to µm^2

        # create lists of integer-rounded x and y centroid positions
        ypos = [int(round(elem, 0)) for elem in df_info_table["centroid-0"].tolist()]
        xpos = [int(round(elem, 0)) for elem in df_info_table["centroid-1"].tolist()]

        # plot rounded centroid positions over image
        # plt.figure(figsize=(24, 8), tight_layout=True)
        
        # apply mask
        # extract features
        # return table
    return features
