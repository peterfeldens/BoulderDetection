# !/usr/bin/env python
# coding: utf8

import argparse
import multiprocessing
import os

import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm
import functions as asf
from PIL import Image

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")

parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('source_directory', type=str, help="Folder with input mosaics")
parser.add_argument('wildcards', type=str, help="identify the files")
parser.add_argument('threshold', type=float, help="minimum acceptable StdDev.", default=2.)

args = asf.parse_args(parser)
args.source_directory.strip("/")

files = asf.getfiles(args.wildcards, args.source_directory)
print('Working on ', len(files), ' files.')


def delete_white(file, folder):
    img = np.asarray(Image.open(folder + "/" + file))
    if np.std(img) < args.threshold:
        cmd = 'rm' + '  ' + args.source_directory + '/' + file
        os.system(cmd)


Parallel(n_jobs=num_cores)(delayed(delete_white)(file, args.source_directory) for file in tqdm(files))
