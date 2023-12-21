'''
The Goal of this Python Script is to take a given input Shapefile and make a Buffer of 100m around it as the
output Shapefile
'''

import geopandas as gpd

def buffer_shapefile(input_shapefile, output_shapefile, buffer_distance=100):
    """
    Buffers a shapefile by a specified distance and saves it as a new shapefile.

    :param input_shapefile: Path to the input shapefile
    :param output_shapefile: Path for the output buffered shapefile
    :param buffer_distance: Buffer distance in meters (default 100)
    """
    # Load the shapefile
    gdf = gpd.read_file(input_shapefile)

    # Apply the buffer
    buffered_gdf = gdf.buffer(buffer_distance)

    # Save the buffered shapefile
    buffered_gdf.to_file(output_shapefile)

    print(f"Buffered shapefile saved as {output_shapefile}")

# Example usage
# buffer_shapefile('path/to/input_shapefile.shp', 'path/to/output_shapefile.shp')

print("TASK COMPLETED SUCCESSFULLY")
