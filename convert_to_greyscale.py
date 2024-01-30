#!/usr/bin/env python
# coding: utf8
"""
Convert RGB to grayscale images by copying the first band to a new file
"""
import argparse
import multiprocessing
import os

import gdal
from joblib import Parallel, delayed
from tqdm import tqdm

import functions as asf

num_cores = multiprocessing.cpu_count() - 1

print("Using ", num_cores, " cores. ")
parser = argparse.ArgumentParser()

parser.add_argument('source_directory', type=str, help="Folder with input mosaics")
parser.add_argument('target_directory', type=str, help="Target folder for image files")
parser.add_argument('wildcards', type=str, help="identify the files. Give complete filename to work on one file only")
parser.add_argument("-t", "--tag", type=str,
                    help="Add Tag to beginning of converted file. Pass emtpy to overwrite files", default='Band_1')
parser.add_argument("-o", "--overwrite", action='store_true',
                    help="Replace Original files")


def make_grey(args, image):
    errors = []
    try:
        src_ds = gdal.Open(args.source_directory + '/' + image)
        img_in = args.source_directory + '/' + image
        img_out = args.target_directory + '/' + args.tag + image

        if src_ds.RasterCount == 1:
            pass

        if src_ds.RasterCount > 1:
            cmd = 'gdal_translate -q -of GTiff -b 1 ' + img_in + ' ' + img_out
            # Could also be done with gdal_calc for mor flexibility cmd = 'gdal_calc.py -R ' + img_in
            # + ' --R_band=1 -G ' + img_in + ' --G_band=2 -B ' + img_in + ' --B_band=3 --outfile=' + img_out + '
            # --calc=\"(R+G+B)/3\"'
            os.system(cmd)
            if args.overwrite:
                cmd = 'mv ' + img_out + ' ' + img_in
                os.system(cmd)
    except Exception as ex:
        print(ex)
        errors.append(image)
    return errors


def main():
    args = asf.parse_args(parser)
    args.source_directory.strip("/")
    args.target_directory.strip("/")
    filelist = asf.getfiles(args.wildcards, args.source_directory)
    errors = Parallel(n_jobs=num_cores)(delayed(make_grey)(args, image) for image in tqdm(filelist))
    errors[:] = [x for x in errors if x]
    print("Following files had error")
    print(errors)


main()
