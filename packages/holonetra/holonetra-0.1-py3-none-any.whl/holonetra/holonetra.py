'''
The Goal of this Python Script is to take a given input Shapefile and make a Buffer of 100m around it as the
output Shapefile
'''

import geopandas as gpd

def buffer_shapefile(input_shapefile, buffer_distance=100):
    """
    Buffers a shapefile by a specified distance.

    :param input_shapefile: Path to the input shapefile
    :param buffer_distance: Buffer distance in meters (default 100)
    :return: Buffered GeoDataFrame
    """
    # Load the shapefile
    gdf = gpd.read_file(input_shapefile)

    # Apply the buffer
    buffered_gdf = gdf.buffer(buffer_distance)

    return buffered_gdf

# End of the Python Script
print("TASK COMPLETED SUCCESSFULLY")
