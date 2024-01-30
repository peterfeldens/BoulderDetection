def getfiles(ID='', PFAD='.', rekursive='no'):
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    import os
    import glob2
    files = []
    if rekursive == 'no':
        for file in os.listdir(PFAD):
            if file.endswith(ID):
                files.append(str(file))
    if rekursive == 'yes':
        files = glob2.glob(PFAD + '/**/*' + ID)
    return files


def parse_args(parser):
    try:
        args = parser.parse_args()
    except Exception as ex:
        parser.print_help()
        print(ex)
    return args


def get_boundaries(image):
    '''
    Bestimmen der Bildgrenzen
    '''
    import gdal
    src = gdal.Open(image)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    return ulx, xres, uly, yres, lrx, lry

def get_projection(image):
    '''
    Bestimmen der Projektion
    '''
    import gdal
    src = gdal.Open(image)
    prj=src.GetProjection()
    return prj