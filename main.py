import os
from pathlib import Path
from PIL import Image
from os import listdir
from os.path import isfile, join
import PySimpleGUI as sg


def main(target_data_type, source_folder, target_folder, verticalsize, horizontalsize, deleteoriginal, rgba):
    # vars
    source_directory = os.path.abspath(source_folder)
    target_directory = os.path.abspath(target_folder)

    # get files according to recognized formats
    p = Path(source_directory)
    for child in p.glob('**/'):
        files = [f for f in listdir(child) if isfile(join(child, f)) and f.endswith(data_type)]

        for file in files:
            try:
                print('Converting ' + file + ' ...')

                image = Image.open(join(child, file))

                if verticalsize != 0 and horizontalsize != 0:
                    size = (int(verticalsize), int(horizontalsize))
                    image = image.resize(size)

                if rgba:
                    image = image.convert('RGBA')
                    background = Image.new('RGBA', image.size, (255, 255, 255))
                    image_rgb = Image.alpha_composite(background, image)
                else:
                    image_rgb = image.convert('RGB')

                newfile = Path(file).stem + target_data_type
                if child == source_directory:
                    image_rgb.save(join(target_directory, newfile))
                target = os.path.join(target_directory, child.relative_to(source_directory))

                # creat sub dir if not existing like in source to maintain original dir structure
                if not os.path.exists(target):
                    os.makedirs(target)

                image_rgb.save(os.path.join(target, newfile))

                print(file + " successfully converted!")
            except Exception as exception:
                print("An error occurred while converting " + file)
                print(exception)
                if deleteoriginal:
                    return False
        if deleteoriginal:
            for file in files:
                try:
                    os.remove(join(child, file))
                except Exception as exception:
                    print("An error occurred while deleting " + file)
                    print(exception)
                    return False
    return True


if __name__ == "__main__":
    data_type = ('.apng', '.blp', '.bmp', '.bufr', '.bw', '.cur', '.dcx', '.dds', '.dib',
                 '.emf', '.eps', '.fit', '.fits', '.flc', '.fli', '.ftc', '.ftu', '.gbr',
                 '.gif', '.grib', '.h5', '.hdf', '.icb', '.icns', '.ico', '.iim', '.im',
                 '.j2c', '.j2k', '.jfif', '.jp2', '.jpc', '.jpe', '.jpeg', '.jpf', '.jpg',
                 '.jpx', '.mpeg', '.mpg', '.msp', '.pbm', '.pcd', '.pcx', '.pgm', '.png',
                 '.pnm', '.ppm', '.ps', '.psd', '.pxr', '.qoi', '.ras', '.rgb', '.rgba',
                 '.sgi', '.tga', '.tif', '.tiff', '.vda', '.vst', '.webp', '.wmf', '.xbm',
                 '.xpm')

    resize_visible = False
    rgba = False

    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [
        [sg.Text('Image Converter')],
        [sg.Text('source folder'), sg.In(size=(25, 1), enable_events=True, key='-InputFOLDER-'), sg.FolderBrowse()],
        [sg.Text('output folder'), sg.In(size=(25, 1), enable_events=True, key='-OutputFOLDER-'), sg.FolderBrowse()],
        [sg.Checkbox('resize Image', enable_events=True, key='-resize-', ),
         sg.Checkbox('RGBA', enable_events=True, key='-rgba-')],
        [sg.Text('resize', key='resize text', visible=resize_visible),
         sg.In(size=(20, 1), key='-verticalsize-', visible=resize_visible),
         sg.Text('x', key='resize x', visible=resize_visible),
         sg.InputText(size=(20, 1), key='-horizontalsize-', visible=resize_visible)],
        [sg.Text('target format'), sg.Combo(data_type, size=(30, 6), key='-targetformat-', )],
        [sg.Text('Delete Original'),
         sg.Combo(['Yes', 'No'], default_value='No', size=(30, 6), key='-deleteoriginal-', )],
        [sg.Button('Ok'), sg.Button('Exit')]
    ]

    # Create the Window
    converter = sg.Window('Plan-Imageconverter', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = converter.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            break
        if event == '-resize-':
            resize_visible = not resize_visible
            converter['resize text'].update(visible=resize_visible)
            converter['-verticalsize-'].update(visible=resize_visible)
            converter['resize x'].update(visible=resize_visible)
            converter['-horizontalsize-'].update(visible=resize_visible)
            converter.refresh()
            print(resize_visible)
        if event == '-rgba-':
            rgba = not rgba

        if event == '-InputFOLDER-':
            source_folder = values['-InputFOLDER-']

        if event == '-OutputFOLDER-':
            target_folder = values['-OutputFOLDER-']

        if event == 'Ok':
            if not (values['-verticalsize-'] and values['-horizontalsize-']):
                values['-verticalsize-'] = values['-horizontalsize-'] = 0

            if values['-deleteoriginal-'] == 'Yes':
                if sg.popup_yes_no('Are you sure to delete the original pictures?') == 'Yes':
                    values['-deleteoriginal-'] = True
                else:
                    values['-deleteoriginal-'] = False

            if values['-deleteoriginal-'] == 'No':
                values['-deleteoriginal-'] = False

            if 'source_folder' in locals() and 'target_folder' in locals() and values['-targetformat-']:

                if main(values['-targetformat-'], source_folder, target_folder, values['-verticalsize-'],
                        values['-horizontalsize-'], values['-deleteoriginal-'], rgba):

                    sg.popup('Process finished successfully')
                else:
                    sg.popup('An error occurred!\nProcess aborted')
