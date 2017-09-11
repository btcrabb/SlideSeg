# ******************************************************************************
# SPAWAR, Systems Center Pacific
# Created August 1, 2017
# Author: Brendan Crabb <brendancrabb8388@pointloma.edu>
#
# ******************************************************************************

# Import necessary packages
from collections import defaultdict
from openslide import OpenSlide
import xml.etree.ElementTree as ET
import numpy as np
import tqdm
import cv2
import os

class AnnotationMask(object):

    def __init__(self, xml_filename, xml_path, size):
        """
        Returns vertex points for annotations in xml file with their assigned keys
        :param xml_filename: The xml file that contains the annotations
        :param xml_path: Path to the xml file that contains the annotations
        :param size: Size of corresponding slide image
        """

        self._xml_filename = xml_filename
        self._xml_path = xml_path
        self._size = size

    def annotations(self):
        """
        Reads xml file and makes annotation mask for entire slide image
        :return: annotation mask
        :return: dictionary of annotation keys and color codes
        """

        # Input parameters
        path = self._xml_path
        input = self._xml_filename

        # Import xml file and get root
        tree = ET.parse('{0}/{1}'.format(path, input))
        root = tree.getroot()

        # Generate annotation array and key dictionary
        mat = np.zeros((self._size[1], self._size[0]), dtype='uint8')
        annotations = defaultdict(list)
        contours = []

        # Find data in xml file
        if not os.path.isfile('Annotation_Key.txt'):
            print("Could not find Annotation_Key.txt, generating new file...")
            AnnotationKey('Annotation_Key.txt').generate_key('xml/')
            print('Annotation_Key generated.')

        color_codes = AnnotationKey('Annotation_Key.txt').load_keys()

        for reg in root.iter('Region'):
            key = reg.get('Text').upper()
            if key in color_codes:
                color_code = color_codes[key][0]
            else:
                AnnotationKey('Annotation_Key.txt').add_keys(key)
                color_codes = AnnotationKey('Annotation_Key.txt').load_keys()
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


class TextOutput(object):

    def __init__(self, filename, annotations):
        """
        Generates .txt file with image and annotation information
        :param filename: filename of corresponding slide image
        :param annotations: annotations contained in the slide image
        """

        self._filename = os.path.splitext(filename)[0]
        self._annotations = annotations

    def write_keys(self):
        """
        Writes each annotation key to the output text file
        :return:
        """
        dest = 'output/textfiles/'
        path = os.path.dirname(dest)
        if not os.path.exists(path):
            os.makedirs(path)

        name = '{0}_{1}'.format(self._filename, 'Details')
        file = open("{0}{1}.txt".format(dest, name), "w+")

        for key, value in self._annotations.iteritems():
            keyline = "Key: {0}".format(key)
            file.write(keyline)
            file.write(("Mask_Color: {0}\n".format(value).rjust(50 - len(keyline))))
        file.close()

    def write_key_img_list(self):
        """
        Writes list of images containing each annotation key
        :return:
        """
        dest = 'output/textfiles/'
        name = '{0}_{1}'.format(self._filename, 'Details')
        file = open("{0}{1}.txt".format(dest, name), "a")

        for key, value in self._annotations.iteritems():
            keyline = "\nKey: {0}\n".format(key)
            file.write(keyline)
            for name in value:
                file.write("   {0}\n".format(name))
        file.close()


class AnnotationKey(object):

    def __init__(self, annotation_key):
        """
        Generates and loads color codes form annotation key
        :param annotation_key:
        """
        self._annotation_key = annotation_key

    def load_keys(self):
        """
        Opens annotation_key file and loads keys and color codes
        :return: color codes
        """

        color_codes = defaultdict(list)
        file = open(self._annotation_key, "r")

        # Load keys and color codes from Annotation_Key.txt
        for line in file:
            color_value = int(line[-5:-2])
            annotation = line[5:]
            annotation = annotation.partition("Mask_")[0].rstrip()
            color_codes[annotation].append(color_value)
        return color_codes

    def add_keys(self, key):
        """
        Adds new key and color_code to annotaiton key
        :param key: The annotation to be added
        :return: updated annotation key file
        """

        color_codes = self.load_keys()
        min_color = min(color_codes.items(), key = lambda x: x[1])[1]
        new_color = int(min_color[0]) - 1
        color_codes[key.upper()].append(new_color)
        self.write_annotation_keys(color_codes)

    def write_annotation_keys(self, annotations):
        """
        Writes annotation keys and color codes to text file
        :param annotations: Dictionary of annotation keys and color codes
        :return: .txt file with annotation keys
        """
        file = open(self._annotation_key, "w+")

        for key, value in sorted(annotations.iteritems()):
            keyline = "Key: {0}".format(key)
            file.write(keyline)
            file.write(("Mask_Color: {0}\n".format(value).rjust(65 - len(keyline))))
        file.close()

    def generate_key(self, path):
        """
        Generates annotation_key from folder of xml files
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
        self.write_annotation_keys(annotations)


class OutputSave(object):

    def __init__(self, image, out_format, quality, dir_mask, dir_image, name, mask, keys, print_save, tags):
        """
        Save image chips and image masks
        :param keys:
        :param print_save:
        :param tags:
        """

        self._keys = keys
        self._print_save = print_save
        self._tags = tags

    def ensure_dir(self, dest):
        """
        Ensures the existence of a directory
        :param dest: Directory to ensure.
        :return: new directory if it did not previously exist.
        """
        directory = os.path.dirname(dest)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def attach_tags(self, path):
        """
        Attaches image tags to metadata of chips and masks
        :param path: file to attach tags to.
        :return: JPG with metadata tags
        """

        if not self._keys:
            pass
        elif os.path.splitext(path)[1] == ".png":
            pass
        else:
            import pexif

            metadata = pexif.JpegFile.fromFile(path)
            str = ' '.join(self._keys)
            metadata.exif.primary.ImageDescription = str
            output = open(path, "wb")
            metadata.writeFd(output)
            output.close()

    def save_chip(self, chip, path, quality):
        """
        Saves the image chip
        :param chip: the slide image chip to save
        :param path: the full path to the chip
        :param quality: the output quality
        :return:
        """

        # Ensure directories
        suffix = os.path.splitext(path)[1]
        directory, filename = os.path.split(path)

        self.ensure_dir(directory)

        if suffix == '.jpg':
            if self._print_save == 1:
                print('\nsaving .../{0}'.format(filename))

            # Save image chip
            chip.save(path, quality)

            # Attach image tags
            if self._tags == 1:
                self.attach_tags(path)

        else:
            if self._print_save == 1:
                print('\nsaving .../{0}'.format(filename))

            # Save image chip
            chip.save(path)

            # Attach image tags
            if self._tags == 1:
                self.attach_tags(path)

    def save_mask(self, mask, path):
        """
        Saves the image masks
        :param mask: the image mask to save
        :param path: the complete path for the mask
        :return:
        """

        # Ensure directories
        suffix = os.path.splitext(path)[1]
        directory, filename = os.path.split(path)

        self.ensure_dir(directory)

        if suffix == '.jpg':

            # Save the image mask
            cv2.imwrite(path, mask, [cv2.IMWRITE_JPEG_QUALITY, 100])

            # Attach image tags
            if self._tags == 1:
                self.attach_tags(path)

        else:
            # Save the image mask
            cv2.imwrite(path, mask)

            # Attach image tags
            if self._tags == 1:
                self.attach_tags(path)


class ChipGenerator(object):

    def __init__(self, params):
        """
        Generates image chips and masks from whole slides
        :param params: the parameters specified
        """
        self._svs_dir = params["slide_path"]
        self._output_path = params["output_dir"]
        self._output_format = params["format"]
        self._output_quality = int(params["quality"])
        self._chip_size = int(params["size"])
        self._overlap = int(params["overlap"])
        self._xml_path = params["xml_path"]
        self._save_all = params["save_all"]
        self._save_ratio = float(params["save_ratio"])
        self._print_save = int(params["print"])
        self._tags = int(params["tags"])

    def open_slide(self, filename):
        """
        Opens a whole slide image
        :param filename: Slide image name.
        :return: slide image, levels, and dimensions
        """

        _path = '{0}{1}'.format(self._svs_dir, filename)
        print('loading {0}'.format(filename))

        # Open Slide Image
        osr = OpenSlide(_path)

        # Get Image Levels and Level Dimensions
        levels = osr.level_count
        dims = osr.level_dimensions
        print('{0} loaded successfully'.format(filename))
        return osr, levels, dims

    def curate_mask(self, mask, scale_width, scale_height):
        """
        Resize and pad annotation mask if necessary
        :param mask:
        :param scale_width:
        :param scale_height:
        :return: curated annotation mask
        """
        # Resize and pad annotation mask if necessary
        mask = cv2.resize(mask, None, fx=float(1) / scale_width, fy=float(1) / scale_height,
                          interpolation=cv2.INTER_CUBIC)

        mask_width, mask_height = mask.shape
        if mask_height < self._chip_size or mask_width < self._chip_size:
            mask = np.pad(mask, ((0, self._chip_size - mask_width),
                                           (0, self._chip_size - mask_height)), 'constant')

        if mask_height > self._chip_size or mask_width > self._chip_size:
            mask = mask[:self._chip_size, :self._chip_size]

        return mask

    def get_chips(self, levels, dims, mask, annotations, filename, suffix):
        """
        Finds chip locations that should be loaded and saved

        :param levels: levels in whole slide image
        :param dims: dimension of whole slide image
        :param mask: annotation mask for slide image
        :param annotations: dictionary of annotations in image
        :param filename: slide image filename
        :param suffix: output format for saving.
        :return: chip_dict. Dictionary of chip names, level, col, row, and scale
        :return: image_dict. Dictionary of annotations and chips with those annotations
        """

        # Image dictionary of keys and save variables
        image_dict = defaultdict(list)
        chip_dict = defaultdict(list)
        save_count_blank = 1
        save_count_annotated = 1

        for i in range(levels):
            width, height = dims[i]
            scale_factor_width = float(dims[0][0]) / width
            scale_factor_height = float(dims[0][1]) / height
            print('Scanning slide level {0}...)'.format(i))

            # Generate the image chip coordinates and save information
            for col in tqdm.tqdm(range(0, width, self._chip_size - self._overlap)):
                for row in range(0, height, self._chip_size - self._overlap):
                    img_mask = mask[int(row * scale_factor_height):int((row + self._chip_size) * scale_factor_height),
                               int(col * scale_factor_width):int((col + self._chip_size) * scale_factor_width)]
                    pix_list = np.unique(img_mask)

                    # Check whether or not to load and save region
                    if self._save_all is True:
                        save = True
                    elif save_count_annotated / float(save_count_blank) > self._save_ratio:
                        save = True
                    elif len(filter(lambda x: x > 0, pix_list)) > 0:
                        save = True
                    else:
                        save = False

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
                            save_count_blank += 1
                            keys.append('NONE')
                        else:
                            save_count_annotated += 1

                        chip_dict[chip_name] = [keys]
                        chip_dict[chip_name].append(i)
                        chip_dict[chip_name].append(col)
                        chip_dict[chip_name].append(row)
                        chip_dict[chip_name].append(scale_factor_width)
                        chip_dict[chip_name].append(scale_factor_height)

        return chip_dict, image_dict


def run(parameters, filename):
    """
    Generates image chips from a whole slide image.
    :param filename:
    :param parameters:
    :return: image chips and masks.
    """

    # Open slide
    osr, levels, dims = ChipGenerator(parameters).open_slide(filename)
    size = (int(dims[0][0]), int(dims[0][1]))

    # Annotation Mask
    xml_file = filename.rstrip(".svs")
    xml_file = xml_file + ".xml"

    print('loading annotation data from {0}/{1}'.format(parameters["xml_path"], xml_file))
    mask, annotations = AnnotationMask(xml_file, parameters["xml_path"], size).annotations()

    # Define output directory
    output_directory_chip = '{0}image_chips/'.format(parameters["output_dir"])
    output_directory_mask = '{0}image_mask/'.format(parameters["output_dir"])

    # Output formatting check
    if parameters["format"].lower() == 'jpg':
        suffix = parameters["format"]
        parameters["format"] = 'JPEG'

    elif parameters["format"].lower() == 'jpeg':
        parameters["format"] = parameters["format"].upper()
        suffix = 'jpg'

    else:
        parameters["format"] = parameters["format"].upper()
        suffix = parameters["format"].lower()

    # Find chip data/locations to be saved
    chip_dictionary, image_dict = ChipGenerator(parameters).get_chips(levels, dims, mask, annotations, filename, suffix)

    # Save chips and masks
    if int(parameters["print"]) == 1:
        print('Saving chips...')

    for filename, value in tqdm.tqdm(chip_dictionary.iteritems()):
        keys = value[0]
        i = value[1]
        col = value[2]
        row = value[3]
        scale_factor_width = value[4]
        scale_factor_height = value[5]

        # load chip region from slide image
        img = osr.read_region([int(col * scale_factor_width), int(row * scale_factor_height)], i,
                              [int(parameters["size"]), int(parameters["size"])]).convert('RGB')

        # load image mask and curate
        img_mask = mask[int(row * scale_factor_height):int((row + int(parameters["size"])) * scale_factor_height),
                   int(col * scale_factor_width):int((col + int(parameters["size"])) * scale_factor_width)]

        img_mask = ChipGenerator(parameters).curate_mask(img_mask, scale_factor_width, scale_factor_height)

        # save the image chip and image mask
        print('Saving chips... {0} chips'.format(len(chip_dictionary)))

        path_chip = output_directory_chip + filename
        path_mask = output_directory_mask + filename

        OutputSave(keys, int(parameters["print"]), int(parameters["tags"])).save_chip(img, path_chip,
                                                                                      int(parameters["quality"]))
        OutputSave(keys, int(parameters["print"]), int(parameters["tags"])).save_mask(img_mask, path_mask)

    # Make text output of Annotation Data
    if int(parameters["print"]) == 1:
        print('Updating txt file details...')

    TextOutput(xml_file, annotations).write_keys()
    TextOutput(xml_file, image_dict).write_key_img_list()

    if int(parameters["print"]) == 1:
        print('txt file details updated')