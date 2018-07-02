# ******************************************************************************
#
# Author: Brendan Crabb <brendancrabb8388@pointloma.edu>
# Created August 1, 2017
#
# ******************************************************************************
"""
MIT License

Copyright (c) 2017 Brendan Crabb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import necessary packages
from PIL import Image
from collections import defaultdict
from openslide import OpenSlide
import xml.etree.ElementTree as ET
import numpy as np
import tqdm
import cv2
import os


def load_parameters(parameters):
    """
    Loads parameters from text file
    :param parameters: the name of the parameters file
    :return: parameters for slideseg
    """
    params = {}
    file = open(parameters, "r")

    for line in file:
        option = line.partition(":")[0]
        value = line.partition(":")[2]
        value = value.partition("#")[0].strip()
        params[option] = value
    return params


def makemask(annotation_key, size, xml_path):
    """
    Reads xml file and makes annotation mask for entire slide image
    :param annotation_key: name of the annotation key file
    :param size: size of the whole slide image
    :param xml_path: path to the xml file
    :return: annotation mask
    :return: dictionary of annotation keys and color codes
    """

    # Import xml file and get root
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Generate annotation array and key dictionary
    mat = np.zeros((size[1], size[0]), dtype='uint8')
    annotations = defaultdict(list)
    contours = []

    # Find data in xml file
    if not os.path.isfile(annotation_key):
        print("Could not find {0}, generating new file...".format(annotation_key))
        generatekey('{0}'.format(annotation_key), os.path.split(xml_path)[0])
        print('{0} generated.'.format(annotation_key))

    color_codes = loadkeys(annotation_key)

    for reg in root.iter('Region'):
        key = reg.get('Text').upper()
        if key in color_codes:
            color_code = color_codes[key][0]
        else:
            addkeys(annotation_key, key)
            color_codes = loadkeys(annotation_key)
            color_codes = color_codes[key][0]

        points = []
        for child in reg.iter('Vertices'):
            for vert in child.iter('Vertex'):
                x = int(round(float(vert.get('X'))))
                y = int(round(float(vert.get('Y'))))
                points.append((x, y))

        cnt = np.array(points).reshape((-1, 1, 2)).astype(np.int32)
        cv2.fillPoly(mat, [cnt], color_code)
        contours.append(cnt)

        # annotations and colors
        if key not in annotations:
            annotations['{0}'.format(key)].append(color_code)
    print('annotations loaded successfully')
    return mat, annotations


def writekeys(filename, annotations):
    """
    Writes each annotation key to the output text file
    :param filename: filename of image chip
    :param annotations: dictionary of annotation keys
    :return: updated text file
    """

    dest = 'output/textfiles/'
    path = os.path.dirname(dest)
    if not os.path.exists(path):
        os.makedirs(path)

    name = '{0}_{1}'.format(os.path.splitext(filename)[0], 'Details')
    file = open("{0}{1}.txt".format(dest, name), "w+")

    for key, value in annotations.iteritems():
        keyline = "Key: {0}".format(key)
        file.write(keyline)
        file.write(("Mask_Color: {0}\n".format(value).rjust(50 - len(keyline))))
    file.close()


def writeimagelist(filename, image_dictionary):
    """
    Writes list of images containing each annotation key
    :param filename: the name of the slide image
    :param image_dictionary: dictionary of images with each key
    :return text
    """
    dest = 'output/textfiles/'
    name = '{0}_{1}'.format(os.path.splitext(filename)[0], 'Details')
    file = open("{0}{1}.txt".format(dest, name), "a")

    for key, value in image_dictionary.iteritems():
        keyline = "\nKey: {0}\n".format(key)
        file.write(keyline)
        for name in value:
            file.write("   {0}\n".format(name))
    file.close()


def loadkeys(annotation_key):
    """
    Opens annotation_key file and loads keys and color codes
    :param: annotation_key: the filename of the annotation key
    :return: color codes
    """

    color_codes = defaultdict(list)
    file = open(annotation_key, "r")

    # Load keys and color codes from Annotation_Key.txt
    for line in file:
        color_value = int(line[-5:-2])
        annotation = line[5:]
        annotation = annotation.partition("Mask_")[0].rstrip()
        color_codes[annotation].append(color_value)
    return color_codes


def addkeys(annotation_key, key):
    """
    Adds new key and color_code to annotation key
    :param annotation_key: the filename of the annotation key
    :param key: The annotation to be added
    :return: updated annotation key file
    """

    color_codes = loadkeys(annotation_key)
    min_color = min(color_codes.items(), key = lambda x: x[1])[1]
    new_color = int(min_color[0]) - 1
    color_codes[key.upper()].append(new_color)
    writeannotations(annotation_key, color_codes)


def writeannotations(annotation_key, annotations):
    """
    Writes annotation keys and color codes to annotation key text file
    :param annotation_key: filename of annotation key
    :param annotations: Dictionary of annotation keys and color codes
    :return: .txt file with annotation keys
    """
    file = open(annotation_key, "w+")

    for key, value in sorted(annotations.iteritems()):
        keyline = "Key: {0}".format(key)
        file.write(keyline)
        file.write(("Mask_Color: {0}\n".format(value).rjust(65 - len(keyline))))
    file.close()


def generatekey(annotation_key, path):
    """
    Generates annotation_key from folder of xml files
    :param annotation_key: the name of the annotation key file
    :param path: Directory containing xml files
    :return: annotation_key file
    """

    color = 256
    annotations = defaultdict(list)
    for filename in os.listdir(path):
        # Import xml file and get root
        tree = ET.parse('{0}/{1}'.format(path, filename))
        root = tree.getroot()

        # Find data in xml file
        for reg in root.iter('Region'):
            key = reg.get('Text').upper()
            if key in annotations:
                continue
            else:
                color -= 1
                color_code = color

            if key not in annotations:
                annotations['{0}'.format(key)].append(color_code)

    # print annotations to text file
    writeannotations(annotation_key, annotations)


def ensuredirectory(dest):
    """
    Ensures the existence of a directory
    :param dest: Directory to ensure.
    :return: new directory if it did not previously exist.
    """
    if not os.path.exists(dest):
        os.makedirs(dest)


def attachtags(path, keys):
    """
    Attaches image tags to metadata of chips and masks
    :param path: file to attach tags to.
    :param keys: keys to attach as tags
    :return: JPG with metadata tags
    """

    if os.path.splitext(path)[1] == ".png":
        pass
    else:
        import pexif

        metadata = pexif.JpegFile.fromFile(path)
        str = ' '.join(keys)
        metadata.exif.primary.ImageDescription = str
        output = open(path, "wb")
        metadata.writeFd(output)
        output.close()


def savechip(chip, path, quality, keys):
    """
    Saves the image chip
    :param chip: the slide image chip to save
    :param path: the full path to the chip
    :param quality: the output quality
    :param keys: keys associated with the chip
    :return:
    """

    # Ensure directories
    directory, filename = os.path.split(path)
    ensuredirectory(directory)
    format, suffix = formatcheck(os.path.splitext(filename)[1].strip('.'))

    if suffix == 'jpg':
        # Save image chip
        chip.save(path, quality = quality)

        # Attach image tags
        attachtags(path, keys)

    else:
        # Save image chip
        chip.save(path)

        # Attach image tags
        attachtags(path, keys)


def savemask(mask, path, keys):
    """
    Saves the image masks
    :param mask: the image mask to save
    :param path: the complete path for the mask
    :param keys: keys associated with the chip
    :return:
    """

    # Ensure directories
    directory, filename = os.path.split(path)
    ensuredirectory(directory)
    format, suffix = formatcheck(os.path.splitext(filename)[1].strip('.'))

    if suffix == 'jpg':
        # Save the image mask
        cv2.imwrite(path, mask, [cv2.IMWRITE_JPEG_QUALITY, 100])

        # Attach image tags
        attachtags(path, keys)

    else:
        # Save the image mask
        cv2.imwrite(path, mask)

        # Attach image tags
        attachtags(path, keys)


def checksave(save_all, pix_list, save_ratio, save_count_annotated, save_count_blank):
    """
    Checks whether or not an image chip should be saved
    :param save_all: (bool) saves all chips if true
    :param pix_list: list of pixel values in image mask
    :param save_ratio: ratio of annotated chips to unannotated chips
    :param save_count_annotated: total annotated chips saved
    :param save_count_blank: total blank chips saved
    :return: bool
    """

    if save_all is True:
        save = True
    elif save_count_annotated / float(save_count_blank) > save_ratio:
        save = True
    elif len(filter(lambda x: x > 0, pix_list)) > 0:
        save = True
    else:
        save = False

    return save


def formatcheck(format):
    """
    Assures correct format parameter was defined correctly
    :param format: the output format parameter
    :return: format
    :return: suffix
    """
    if format.lower() == 'jpg':
        _suffix = format
        format = 'JPEG'

    elif format.lower() == 'jpeg':
        format = format.upper()
        _suffix = 'jpg'

    else:
        format = format.upper()
        _suffix = format.lower()

    return format, _suffix


def openwholeslide(path):
    """
    Opens a whole slide image
    :param path: Slide image path.
    :return: slide image, levels, and dimensions
    """

    _directory, _filename = os.path.split(path)
    print('loading {0}'.format(_filename))

    # Open Slide Image
    osr = OpenSlide(path)

    # Get Image Levels and Level Dimensions
    levels = osr.level_count
    dims = osr.level_dimensions
    print('{0} loaded successfully'.format(_filename))
    return osr, levels, dims


def curatemask(mask, scale_width, scale_height, chip_size):
    """
    Resize and pad annotation mask if necessary
    :param mask: an image mask
    :param scale_width: scaling for higher magnification levels
    :param scale_height: scaling for higher magnification levels
    :return: curated annotation mask
    """
    # Resize and pad annotation mask if necessary
    mask = cv2.resize(mask, None, fx=float(1) / scale_width, fy=float(1) / scale_height,
                      interpolation=cv2.INTER_CUBIC)

    mask_width, mask_height = mask.shape
    if mask_height < chip_size or mask_width < chip_size:
        mask = np.pad(mask, ((0, chip_size - mask_width),
                                       (0, chip_size - mask_height)), 'constant')

    if mask_height > chip_size or mask_width > chip_size:
        mask = mask[:chip_size, :chip_size]

    return mask


def getchips(levels, dims, chip_size, overlap, mask, annotations, filename, suffix, save_all, save_ratio):
    """
    Finds chip locations that should be loaded and saved

    :param levels: levels in whole slide image
    :param dims: dimension of whole slide image
    :param chip_size: the size of the image chips
    :param overlap: overlap between image chips (stride)
    :param mask: annotation mask for slide image
    :param annotations: dictionary of annotations in image
    :param filename: slide image filename
    :param suffix: output format for saving.
    :param save_all: whether or not to save every image chip (bool)
    :param save_ratio: ratio of annotated to unannotated chips (float)
    :return: chip_dict. Dictionary of chip names, level, col, row, and scale
    :return: image_dict. Dictionary of annotations and chips with those annotations
    """

    # Image dictionary of keys and save variables
    image_dict = defaultdict(list)
    chip_dict = defaultdict(list)
    _save_count_blank = 1
    _save_count_annotated = 1

    for i in range(levels):
        width, height = dims[i]
        scale_factor_width = float(dims[0][0]) / width
        scale_factor_height = float(dims[0][1]) / height
        print('Scanning slide level {0} of {1}'.format(i + 1, levels))

        # Generate the image chip coordinates and save information
        for col in tqdm.tqdm(range(0, width, chip_size - overlap)):
            for row in range(0, height, chip_size - overlap):
                img_mask = mask[int(row * scale_factor_height):int((row + chip_size) * scale_factor_height),
                           int(col * scale_factor_width):int((col + chip_size) * scale_factor_width)]
                pix_list = np.unique(img_mask)

                # Check whether or not to save the region
                save = checksave(save_all, pix_list, save_ratio, _save_count_annotated, _save_count_blank)
                # Save image and assign keys.
                if save is True:
                    chip_name = '{0}_{1}_{2}_{3}.{4}'.format(filename.rstrip('.svs'), i, row, col, suffix)
                    keys = []

                    # Make sure annotation key contains value
                    for key, value in annotations.iteritems():
                        for pixel in pix_list:
                            if int(pixel) == int(value[0]):
                                keys.append(key)
                                image_dict[key].append(chip_name)

                    if len(keys) == 0:
                        _save_count_blank += 1
                        keys.append('NONE')
                    else:
                        _save_count_annotated += 1

                    chip_dict[chip_name] = [keys]
                    chip_dict[chip_name].append(i)
                    chip_dict[chip_name].append(col)
                    chip_dict[chip_name].append(row)
                    chip_dict[chip_name].append(scale_factor_width)
                    chip_dict[chip_name].append(scale_factor_height)

    return chip_dict, image_dict


def run(parameters, filename):
    """
    Runs SlideSeg: Generates image chips from a whole slide image.
    :param parameters: specified in Parameters.txt file
    :param filename: filename of whole slide image
    :return: image chips and masks.
    """

    # Define variables
    _slide_path = parameters["slide_path"]
    _xml_path = parameters["xml_path"]
    _output_dir = parameters["output_dir"]
    _format = parameters["format"]
    _quality = int(parameters["quality"])
    _chip_size = int(parameters["size"])
    _overlap = int(parameters["overlap"])
    _key = parameters["key"]
    _save_all = parameters["save_all"]
    _save_ratio = parameters["save_ratio"]

    # Open slide
    _osr, _levels, _dims = openwholeslide('{0}{1}'.format(_slide_path, filename))
    _size = (int(_dims[0][0]), int(_dims[0][1]))

    # Annotation Mask
    xml_file = filename.rstrip(".svs")
    xml_file = xml_file + ".xml"

    print('loading annotation data from {0}/{1}'.format(_xml_path, xml_file))
    _mask, _annotations = makemask(_key, _size, '{0}{1}'.format(_xml_path, xml_file))

    # Define output directory
    output_directory_chip = '{0}image_chips/'.format(_output_dir)
    output_directory_mask = '{0}image_mask/'.format(_output_dir)

    # Output formatting check
    _format, _suffix = formatcheck(_format)

    # Find chip data/locations to be saved
    chip_dictionary, image_dict = getchips(_levels, _dims, _chip_size, _overlap,
                                           _mask, _annotations, filename, _suffix, _save_all, _save_ratio)

    # Save chips and masks
    print('Saving chips... {0} total chips'.format(len(chip_dictionary)))

    for filename, value in tqdm.tqdm(chip_dictionary.iteritems()):
        keys = value[0]
        i = value[1]
        col = value[2]
        row = value[3]
        scale_factor_width = value[4]
        scale_factor_height = value[5]

        # load chip region from slide image
        img = _osr.read_region([int(col * scale_factor_width), int(row * scale_factor_height)], i,
                              [_chip_size, _chip_size]).convert('RGB')

        # load image mask and curate
        img_mask = _mask[int(row * scale_factor_height):int((row + _chip_size) * scale_factor_height),
                         int(col * scale_factor_width):int((col + _chip_size) * scale_factor_width)]

        img_mask = curatemask(img_mask, scale_factor_width, scale_factor_height, _chip_size)

        # save the image chip and image mask
        _path_chip = output_directory_chip + filename
        _path_mask = output_directory_mask + filename

        savechip(img, _path_chip, _quality, keys)
        savemask(img_mask, _path_mask, keys)

    # Make text output of Annotation Data
    print('Updating txt file details...')

    writekeys(xml_file, _annotations)
    writeimagelist(xml_file, image_dict)

    print('txt file details updated')
