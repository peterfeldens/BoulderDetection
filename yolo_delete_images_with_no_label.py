# Make all images without .jpg as empty examples
# If no empty examples are needed, do not execute this cell

import functions as asf
import argparse
from tqdm import tqdm
import os


parser = argparse.ArgumentParser()

parser.add_argument('directory', type=str, help="Folder with input mosaics")
parser.add_argument('wildcards', type=str, help="file type with leading dot")

args = asf.parse_args(parser)
args.directory.strip("/")



def delete_empty(files, PFAD):
    counter = 0
    for f in tqdm(files):
        filename = os.path.basename(f)
        basename = os.path.splitext(filename)[0]
        try:
            f = open(PFAD + '/' + basename + ".txt")
            f.close()
        except IOError:
            os.remove(PFAD + '/' + basename + args.wildcards)
            counter = counter + 1
    return counter

files = asf.getfiles(args.wildcards, args.directory)
counter = delete_empty(files, args.directory)
print('Deleted ', counter , ' files.')

