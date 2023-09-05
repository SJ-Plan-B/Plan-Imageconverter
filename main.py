import os
from pathlib import Path
from PIL import Image
from os import listdir
from os.path import isfile, join
import PySimpleGUI as sg


def main(target_data_type, source_folder, target_folder, verticalsize, horizontalsize, deleteoriginal):
    target_data_type = target_data_type
    source_directory = source_folder
    source_directory = os.path.abspath(source_directory)
    target_directory = target_folder
    target_directory = os.path.abspath(target_directory)

    files = [f for f in listdir(source_directory) if isfile(join(source_directory, f)) and f.endswith(data_type)]

    for file in files:
        try:
            print('Converting '+file+' ...')

            image = Image.open(source_directory + "\\" + file)

            if verticalsize != 0 and horizontalsize != 0:
                size = (int(verticalsize), int(horizontalsize))
                image = image.resize(size)
            image = image.convert('RGB')
            image.save(target_folder + "\\" + Path(file).stem + target_data_type)
            print(file+" successfully converted!")
        except:
            print("An error occurred while converting "+ file)
            if deleteoriginal:
                print("Aborting process...")
                exit(1)
    if deleteoriginal:
            for file in files:
                os.remove(source_folder+"\\"+file)

    exit(0)


if __name__ == "__main__":
    data_type = ('.jpeg', '.jpg', '.webp', '.bmp', '.gif', '.tiff', '.png',
                 '.ftc', '.bw', '.cur', '.icns', '.xpm', '.j2c', '.jpx', '.icb', '.ftu',
                 '.apng', '.vda', '.vst', '.jpe', '.pnm', '.ras', '.psd',
                 '.iim', '.pxr', '.blp', '.j2k', '.jpf', '.im', '.hdf', '.ico',
                 '.h5', '.gbr', '.pcd', '.ppm', '.fli', '.emf', '.eps', '.mpeg', '.dds',
                 '.ps', '.jpc', '.pgm', '.tga', '.jfif', '.wmf', '.grib', '.pbm', '.mpg', '.msp',
                 '.dcx', '.dib', '.tif', '.flc', '.fits', '.rgba', '.pcx', '.rgb', '.xbm', '.fit',
                 '.jp2', '.qoi', '.sgi', '.bufr')

    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [
        [sg.Text('Image Converter')],
        [sg.Text('source folder'), sg.In(size=(25, 1), enable_events=True, key='-InputFOLDER-'), sg.FolderBrowse()],
        [sg.Text('output folder'), sg.In(size=(25, 1), enable_events=True, key='-OutputFOLDER-'), sg.FolderBrowse()],
        [sg.Text('Resize\nLeave empty to not resize\n'), sg.In(size=(20, 1), key='-verticalsize-'), sg.Text('x'), sg.InputText(size=(20, 1),key='-horizontalsize-')],
        [sg.Text('target format'), sg.Combo( data_type, size=(30, 6), key='-targetformat-',)],
        [sg.Text('Delete Original'), sg.Combo(['Yes', 'No'], size=(30, 6), key='-deleteoriginal-', )],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    # Create the Window
    converter = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = converter.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        if event == '-InputFOLDER-':
            source_folder = values['-InputFOLDER-']
        if event == '-OutputFOLDER-':
            target_folder = values['-OutputFOLDER-']
        if event == 'Ok':
            if values['-deleteoriginal-'] == 'Yes':
                if sg.popup_yes_no('Are you sure to delete the original pictures?') == 'Yes':
                    if locals() and 'source_folder' in locals() and 'target_folder' in locals():
                        if values['-targetformat-']:
                            if values['-verticalsize-'] and values['-horizontalsize-']:
                                main(values['-targetformat-'], source_folder, target_folder, values['-verticalsize-'], values['-horizontalsize-'], True)
                            else:
                                main(values['-targetformat-'], source_folder, target_folder, 0, 0, True)

            if values['-deleteoriginal-'] == 'No':
                if locals() and 'source_folder' in locals() and 'target_folder' in locals():
                    if values['-targetformat-']:
                        if values['-verticalsize-'] and values['-horizontalsize-']:
                            main(values['-targetformat-'], source_folder, target_folder, values['-verticalsize-'], values['-horizontalsize-'], False)
                        else:
                            main(values['-targetformat-'], source_folder, target_folder, 0, 0, False)




        print(values)


    converter.close()
