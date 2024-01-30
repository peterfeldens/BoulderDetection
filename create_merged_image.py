import numpy as np
import argparse

import matplotlib.pyplot as plt
from osgeo import gdal
from tqdm import tqdm
import functions as asf

parser = argparse.ArgumentParser()

parser.add_argument('input_directory', type=str, help=" folder with small tif to be merged")
parser.add_argument('output_directory', type=str, help="Target folder")
parser.add_argument('output_name', type=str, help="Target filename")
parser.add_argument('tile_size', type=int, help="size of tiles")


# Parse Arguments
args = asf.parse_args(parser)
args.output_directory.strip("/")
args.input_directory.strip("/")



# Read files to process
file_list = asf.getfiles(".tif", args.input_directory)

def load_geotiff(file_path):
    dataset = gdal.Open(file_path)
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()
    return array

def merge_images(small_images):
    num_images = len(small_images)
    rows = int(num_images ** 0.5)  # Number of rows in the final image
    cols = (num_images + rows - 1) // rows  # Number of columns in the final image

    # Calculate the dimensions of the final image
    final_height = rows * args.tile_size
    final_width = cols * args.tile_size

    # Create a blank canvas for the final image
    final_image = np.zeros((final_height, final_width), dtype=np.uint8)

    # Merge small images into the final image
    for i, img in enumerate(small_images):
        x = (i % cols) * args.tile_size
        y = (i // cols) * args.tile_size
        final_image[y:y+args.tile_size, x:x+args.tile_size] = img

    return final_image


small_images = []
for file in file_list:
    image = load_geotiff(path)
    small_images.append(image)

# Merge the small images into one large image
final_image = merge_images(small_images)

# Save the final image as a grayscale GeoTIFF file
output_file = args.output_folder + "/" + args.output_name
driver = gdal.GetDriverByName('GTiff')
rows, cols = final_image.shape
dataset = driver.Create(output_file, cols, rows, 1, gdal.GDT_Byte)
band = dataset.GetRasterBand(1)
band.WriteArray(final_image)
dataset.FlushCache()
dataset = None

print(f"The merged image has been saved as '{output_file}'")


