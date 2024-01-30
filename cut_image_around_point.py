import argparse

import pandas as pd
from osgeo import gdal
from tqdm import tqdm
import functions as asf
#TODO make this accept sqlite Input, so there does not need to be an extra export of the database during training
parser = argparse.ArgumentParser()

parser.add_argument('path_csv', type=str, help="Path to csv with points in columns named X and Y ")
parser.add_argument('target_directory', type=str, help=" folder for tifs to be cutted")
parser.add_argument('output_directory', type=str, help="Target folder cuts")
parser.add_argument('tile_size', type=int, help="buffer around points for cutting in projection of tif and csv file")
parser.add_argument('wildcards', type=str, help="identify the files")

# Parse Arguments
args = asf.parse_args(parser)
args.target_directory.strip("/")

# Read files to process
file_list = asf.getfiles(args.wildcards, args.target_directory)

# Read csv
df_bbox = pd.read_csv(args.path_csv)

for tif in file_list:
    for row in tqdm(df_bbox.itertuples()):
        x = row.X
        y = row.Y
        ulx = x - args.tile_size
        uly = y + args.tile_size
        lrx = x + args.tile_size
        lry = y - args.tile_size
        # [-projwin ulx uly lrx lry]
        bbox = (ulx, uly, lrx, lry)
        # print(bbox)
        input_tif = args.target_directory + "/" + tif
        output_tif = args.output_directory + "/" + tif.strip(args.wildcards) + "_" + str(int(x)) + "_" + str(
            int(y)) + ".tif"
        gdal.Translate(output_tif, input_tif, projWin=bbox)
