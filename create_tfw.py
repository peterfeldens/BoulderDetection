# Create tfw files if needed
# funktioniert nicht für gedrehte bilder

import argparse
import multiprocessing
import os

import gdal
import osgeo.osr as osr
from joblib import Parallel, delayed
from tqdm import tqdm

import functions as asf


def generate_tfw(infile, scale_factor=1, suffix='.tfw', gen_prj='prj'):
    src = gdal.Open(infile)
    xform = src.GetGeoTransform()

    if gen_prj == 'prj':
        src_srs = osr.SpatialReference()
        src_srs.ImportFromWkt(src.GetProjection())
        src_srs.MorphToESRI()
        src_wkt = src_srs.ExportToWkt()

        prj = open(os.path.splitext(infile)[0] + '.prj', 'wt')
        prj.write(src_wkt)
        prj.close()

    corr_1 = xform[1] / scale_factor
    corr_5 = xform[5] / scale_factor
    edit1 = xform[0] + corr_1 / 2
    edit2 = xform[3] + corr_5 / 2

    tfw = open(os.path.splitext(infile)[0] + suffix, 'wt')
    tfw.write("%0.8f\n" % corr_1)
    tfw.write("%0.8f\n" % xform[2])
    tfw.write("%0.8f\n" % xform[4])
    tfw.write("%0.8f\n" % corr_5)
    tfw.write("%0.8f\n" % edit1)
    tfw.write("%0.8f\n" % edit2)
    tfw.close()


parser = argparse.ArgumentParser()
# Required Arguments
parser.add_argument('directory', type=str, help="Folder with data")
parser.add_argument('wildcards', type=str, help="identifier for Files")
parser.add_argument('scale', type=float, help="multiply tfw file by factor for magnfied or shrink images. standard = 1",
                    default=1)
parser.add_argument('suffix', type=str, help="suffix for world file. Default is tfw", default='tfw')

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")
args = asf.parse_args(parser)
args.directory.strip("/")

filelist = asf.getfiles(args.wildcards, args.directory)

Parallel(n_jobs=num_cores)(
    delayed(generate_tfw)(args.directory + '/' + file, args.scale, args.suffix) for file in tqdm(filelist))
