import pandas as pd
import cv2
import functions as asf
import argparse
import sys
import os

parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('--directory', type=str, help="Folder with json yolor esult")
parser.add_argument('--outfile', type=str, help="result.csv")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

def f(img, x, y, rel_w, rel_h):
    im = cv2.imread(img)
    h, w, c = im.shape
    ulx, xres, uly, yres, lrx, lry = asf.get_boundaries(img)
    proj = asf.get_projection(img)
    Pixel_X = x * w
    Pixel_Y = y * h

    X = ulx + Pixel_X * xres
    Y = uly + (Pixel_Y * yres)  #yres ist negativ

    H = rel_h * h * yres
    W = rel_w * w * xres

    y1 = Y + (H/2) #yres ist negativ
    x1 = X - (W/2)
    x2 = X + (W/2) #yres ist negativ
    y2 = Y - (H/2)

    return X,Y,x1, y1, x2, y2, proj


def flatten_nested_json_df(dataframe):
    dataframe = dataframe.reset_index()

    print(f"original shape: {dataframe.shape}")
    print(f"original columns: {dataframe.columns}")
    # search for columns to explode/flatten
    s = (dataframe.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (dataframe.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    print(f"lists: {list_columns}, dicts: {dict_columns}")
    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            print(f"flattening: {col}")
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(dataframe[col]).add_prefix(f'{col}.')
            horiz_exploded.index = dataframe.index
            dataframe = pd.concat([dataframe, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)  # inplace

        for col in list_columns:
            print(f"exploding: {col}")
            # explode lists vertically, adding new columns
            dataframe = dataframe.drop(columns=[col]).join(dataframe[col].explode().to_frame())
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (dataframe[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (dataframe[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()

        print(f"lists: {list_columns}, dicts: {dict_columns}")

    print(f"final shape: {dataframe.shape}")
    print(f"final columns: {dataframe.columns}")
    return dataframe

df = pd.read_json(args.directory)
df = df[df['objects'].map(lambda d: len(d)) > 0]  # Filter empty rows, otherwise its not correctly expanded
df = flatten_nested_json_df(df)
print(df.head())

df['tifname'] = [os.path.splitext(filename)[0] + '.tif' for filename in df['filename']]
df[['X', 'Y','x1','y1', 'x2', 'y2', 'proj']] = [f(img, x, y, rel_x, rel_w) for img, x,y, rel_x, rel_w in zip(df['tifname'], df['objects.relative_coordinates.center_x'], df['objects.relative_coordinates.center_y'], df['objects.relative_coordinates.width'], df['objects.relative_coordinates.height'])]

df['wkt'] =  [str('POLYGON ((' + str(x1) + ' ' + str(y1) + ',' + str(x1) + ' ' +
                  str(y2) + ',' + str(x2) + ' ' + str(y2) + ',' +
                  str(x2) + ' ' + str(y1) + ',' + str(x1) + ' ' +
                  str(y1) + '))') for x1, y1, x2, y2 in zip(df.x1,df.y1, df.x2, df.y2)]

print(df.head())
df.to_csv(args.outfile)