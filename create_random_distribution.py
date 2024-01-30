#!/usr/bin/env python
# coding: utf8
"""
Split files in a folder randomly on training and validation datasets
"""

import argparse
from tqdm import tqdm

import functions as asf


def random_distribution(source_folder, target_folder, wildcard, valid_percentage=0.2, txtcopy=0):
    import os
    import random
    import shutil
    import functions as asf

    filelist = asf.getfiles(ID=wildcard, PFAD=source_folder, rekursive='no')
    number_of_files = len(filelist)
    index_of_files = range(0, number_of_files - 1)
    number_of_valid_files = int(number_of_files * valid_percentage)
    random_files_index = random.sample(index_of_files, number_of_valid_files)
    for i in tqdm(random_files_index):
        shutil.move(source_folder + '/' + filelist[i], target_folder + '/' + filelist[i])
        if txtcopy > 0:
            base = os.path.basename(filelist[i])
            txtname = os.path.splitext(base)[0] + ".txt"
            shutil.move(source_folder + '/' + txtname, target_folder + '/' + txtname)
    return


parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('source_directory', type=str, help="Folder with all training data")
parser.add_argument('target_directory', type=str, help="A percentage of files is moved in this folder")
parser.add_argument('valid_percentage', type=float, help="Percentage of validation dataset")
parser.add_argument('wildcards', type=str, help="identfiy the files")
parser.add_argument('--txtfiles', type=int, help="copy orresponding txtfiles for yolo", default=0)

args = asf.parse_args(parser)

args.source_directory.strip("/")
args.target_directory.strip("/")

print("Splitting all files in folder:", args.source_directory)

random_distribution(args.source_directory, args.target_directory, args.wildcards, args.valid_percentage, args.txtfiles)
