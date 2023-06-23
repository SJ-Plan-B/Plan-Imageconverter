import os
from pathlib import Path
from PIL import Image


data_type = ('.ftc', '.bw', '.cur', '.icns', '.xpm', '.j2c', '.jpx', '.icb', '.ftu',
            '.apng', '.vda', '.tiff', '.vst', '.jpe', '.pnm', '.ras', '.psd', '.bmp',
            '.gif', '.iim', '.pxr', '.blp', '.j2k', '.jpf', '.im', '.hdf', '.png', '.ico',
            '.h5', '.gbr', '.jpg', '.pcd', '.ppm', '.fli', '.emf', '.eps', '.mpeg', '.dds',
            '.ps', '.jpc', '.pgm', '.tga', '.jfif', '.wmf', '.grib', '.pbm', '.mpg', '.msp',
            '.dcx', '.dib', '.tif', '.flc', '.fits', '.rgba', '.pcx', '.rgb', '.xbm', '.fit',
            '.jp2', '.jpeg', '.webp', '.qoi', '.sgi', '.bufr')
target_data_type = str(input("Enter target data type: ") or ".jpg")
source_directory = str(input("Enter path of the source folder: ") or "input/")
target_source_directory = str(input("Enter path of the target folder: ") or "output/")


try:
    for file in os.listdir(source_directory):
        try:
            if file.endswith(data_type):
                image = Image.open(source_directory+file)
                print(image)
                image = image.convert('RGB')
                image.save("output/"+Path(file).stem+target_data_type)
                print("Image successfully converted!")
        except IOError:
            print("Can not convert "+file+" to "+file+target_data_type)
except OSError:
    print("Can not acces OS folder")

exit(0)