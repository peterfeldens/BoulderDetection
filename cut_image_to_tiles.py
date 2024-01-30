#!/usr/bin/env python
# coding: utf8
"""
This script takes an input mosaic and cuts it into user defined rectangles.

It requires that the gdal command line utilities are installed
"""

import argparse
import multiprocessing
import os

from joblib import Parallel, delayed
from tqdm import tqdm

import functions as asf

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")
if num_cores > 12:
    num_cores = 12
parser = argparse.ArgumentParser()

# Required Arguments

parser.add_argument('source_directory', type=str, help="Folder with input mosaics")
parser.add_argument('target_directory', type=str, help="Target folder for image files")
parser.add_argument('tile_size', type=int, help="size of the squares in pixels")
parser.add_argument('wildcards', type=str, help="identify the files")

parser.add_argument("-o", "--overlap", type=int, help="number of overlap between pixels", default=0)


def execute_command(command):
    os.system(command)
    return


# Parse Arguments
args = asf.parse_args(parser)
args.source_directory.strip("/")
args.target_directory.strip("/")

# Read files to process
files = asf.getfiles(args.wildcards, args.source_directory)

print("Tiling Mosaics:")

for mosaic in files:
    print(mosaic)


skipped_files = []
for mosaic in tqdm(files):
    try:
        if args.overlap == 0:
            print("No overlap")
            cmd = 'gdal_retile.py -ps ' + str(args.tile_size) + ' ' + str(args.tile_size) + ' -targetDir ' + \
                  '"' + args.target_directory + '"' + ' ' + '"' + \
                  args.source_directory + '/' + mosaic + '"'
            # os.system(cmd)
            Parallel(n_jobs=num_cores)(delayed(execute_command)(str(cmd))
                                       for file in tqdm(files))
        if args.overlap > 0:
            print("Cutting with Overlap")
            cmd = 'gdal_retile.py -ps ' + str(args.tile_size) + ' ' + str(args.tile_size) + ' -overlap ' + str(
                args.overlap) + ' -targetDir ' + '"' + args.target_directory + '"' + ' ' + '"' + args.source_directory + '/' + mosaic + '"'
            os.system(cmd)
            #Parallel(n_jobs=num_cores)(delayed(execute_command)(str(cmd))
            #                           for mosaic in tqdm(files))  #TODO bug, wegen der for schleife wird das 2x ausgeführt

    except Exception as ex:
        print(ex)
        skipped_files.append(mosaic)

# print list of files that did not work for further investigation
if skipped_files:
    print('Skipped Files:', skipped_files)
