#!/usr/bin/env python
# coding: utf8

import argparse
import multiprocessing
import os
from PIL import Image
from joblib import Parallel, delayed
from tqdm import tqdm

import functions as asf


def make_png(directory, image):
    im = Image.open(os.path.join(directory, image))
    outfile, ext = os.path.splitext(os.path.basename(image))#
    im.save(directory + '/' + outfile + '.png', "PNG", quality=100)
    return


def main():
    num_cores = multiprocessing.cpu_count() - 1
    print("Using ", num_cores, " cores. ")

    parser = argparse.ArgumentParser()
    # Required Arguments
    parser.add_argument('directory', type=str, help="Folder with data")

    args = asf.parse_args(parser)

    args.directory.strip("/")
    print("TIF warnings are supressed")

    filelist = asf.getfiles('.tif', args.directory)

    Parallel(n_jobs=num_cores)(delayed(make_png)(args.directory, image) for image in tqdm(filelist))


main()
