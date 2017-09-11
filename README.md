# SlideSeg

Spawar, Systems Center Pacific <br>
Created August 1, 2017 <br>
Author: Brendan Crabb <brendancrabb8388@pointloma.edu> 
<hr>

Welcome to SlideSeg, a python script that allows you to segment whole slide images into usable image
chips for deep learning. Image masks for each chip are generated from associated markup and annotation files.

## Table of Contents
[User Guide](#user-guide)

1.    [Dependencies](#1.)  
2.    [Anaconda Environment](#2.)  
      2.1 [Creating environment from .yml file](#2.1)  
      2.2 [Change Jupyter Notebook startup folder (Windows)](#2.2)  
      2.3 [Change Jupyter Notebook startup folder (OS X)](#2.3)  
      2.4 [Jupyter Kernel Selection](#2.4)
3.    [Setup](#3.)  
      3.1 [Supported Formats](#3.1)  
      3.2 [Parameters](#3.2)  
      3.3 [Annotation Key](#3.3)  
5.    [Output](#5.)  
      5.1 [Image_Chips](#5.1)  
      5.2 [Image_Masks](#5.2)  
      5.3 [Text Files](#5.3)  
6.    [Run](#6.) 

## User Guide <a class ="anchor" id="user-guide"></a>

### 1. Dependencies <a class ="anchor" id="1."></a>

SlideSeg runs on Python 2.7 and depends on the following libraries: <br>

 * openslide 1.1.1 <br>
 * tqdm 4.15.0 <br>
 * cv2 3.2.0 <br>
 * numpy <br>
 * pexif 0.15 <br>

The libraries can be installed using the following sources: <br>
 * openslide:  pip install openslide-python <br>
 * tqdm:       conda install -c conda-forge tqdm <br>
 * numpy:      conda install -c anaconda numpy <br>
 * cv2:        pip install opencv-python <br>
 * pexif:      pip install pexif<br>
 
If you are using the preconfigured SlideSeg anaconda environment, these dependencies will already be installed.  <br>

### 2. Anaconda Environment <a class ="anchor" id="2."></a>

Make sure anaconda is installed. The SlideSeg environment has an Ipython kernel with all of the necessary packages already installed; however, conda support for jupyter notebooks is needed to switch kernels. This support is available through conda itself and can be enabled by issuing the following command:

<code>conda install nb_conda </code>

##### 2.1 Creating environment from .yml file <a class ="anchor" id="2.1"></a>
Copy the environment_slideseg.yml file to the anaconda directory,  .../anaconda/scripts/. In the same directory, issue the following command to create the anaconda environment from the file:

<code>conda env create -f environment_slideseg.yml </code>

Creating the environment might take a few minutes. Once finished, issue the following command to activate the environment:

* Windows: <code>activate SlideSeg</code>
* macOS and Linux: <code>source activate SlideSeg</code>

If the environment was activated successfully, you should see (SlideSeg) at the beggining of the command prompt. This will set the SlideSeg kernel as your default kernel when running jupyter. 

The Jupyter Notebook App can be launched by clicking on the Jupyter Notebook icon installed by Anaconda in the start menu (Windows) or by typing in the terminal (cmd on Windows): 

<code>jupyter notebook</code>

This will launch a new browser window showing the Notebook Dashboard.  When started, the Jupyter Notebook app can only access files within its start-up folder.  If you stored the SlideSeg notebook documents in a subfolder of your user folder, no configuration is necessary.  Otherwise, you need to change your Jupyter Notebook App start-up folder.  

#####  2.2 Change Jupyter Notebook startup folder (Windows) <a class ="anchor" id="2.2"></a>

* Copy the *Jupyter Notebook* launcher from the menu to the desktop. <br>
* Right click on the new launcher, select properties, and change the *Target field*, change %USERPROFILE% to the full path of the folder which will contain all the notebooks. <br>
* Double-click on the *Jupyter Notebook* desktop launcher (icon shows [IPy]) to start the Jupyter Notebook App, which will open in a new browser window (or tab). Note also that a secondary terminal window (used only for error logging and for shut down) will be also opened. If only the terminal starts, try opening this address with your browser: http://localhost:8888/. <br>

##### 2.3 Change Jupyter Notebook startup folder (OS X) <a class ="anchor" id="2.3"></a>
To launch Jupyter Notebook App:

* Click on spotlight, type terminal to open a terminal window.
* Enter the startup folder by typing cd /some_folder_name.
* Type jupyter notebook to launch the Jupyter Notebook App (it will appear in a new browser window or tab). <br>

##### 2.4 Jupyter Kernel Selection <a class ="anchor" id = "2.4"></a>
After launching the Jupyter Notebook App, navigate to the SlideSeg notebook and click on its name to open in a new browser tab. In the upper right corner, you should see  Python [conda env:SlideSeg].  If not, click on Kernel> Change Kernel> and change your current kernel to Python [conda env:SlideSeg]. 

### 3. Setup <a class ="anchor" id="3."></a>

Create a folder called 'images/' in the main directory and copy all of the slide images into this folder. Copy the markup and annotation files (in .xml format) into the xml folder in the main project directory. It is important that the annotation files have the same file name as the slide they are associated with. <br>
   
##### 3.1 Supported Formats <a class ="anchor" id="3.1"></a>

SlideSeg can read virtual slides in the following formats: <br>
   
  * Aperio (.svs, .tif) <br>
  * Hamamatsu (.ndpi, .vms, .vmu) <br>
  * Leica (.scn) <br>
  * MIRAX (.mrxs) <br>
  * Philips (.tiff) <br>
  * Sakura (.svslide) <br>
  * Trestle (.tif) <br>
  * Ventana (.bif, .tif) <br>
  * Generic tile TIFF (.tif) <br>

SlideSeg can read annotations in the following formats: <br>
  * XML (.xml) <br>

##### 3.2 Parameters <a class ="anchor" id="3.2"></a>
  
 SlideSeg depends on the following parameters:
 
<p style="margin-left: 40px">
<b>single_slide:</b> True if using one image only, False if a folder of images is being used <br>

<b>slide_path:</b> Path to the folder of slide images <br>

<b>xml_path:</b> Path to the folder of xml files <br>

<b>output_dir:</b> Path to the output folder where image_chips, image_masks, and text_files will be saved <br>

<b>format:</b> Output format of the image_chips and image_masks (png or jpg only) <br>

<b>quality:</b> Output quality: JPEG compression if output format is 'jpg' (100 recommended,jpg compression artifacts will distort image segmentation) <br>

<b>size:</b> Size of image_chips and image_masks in pixels <br>

<b>overlap:</b> Pixel overlap between image chips <br>

<b>key:</b> The text file containing annotation keys and color codes <br>

<b>save_all:</b> True saves every image_chip, False only saves chips containing an annotated pixel <br>

<b>save_ratio:</b> Ratio of image_chips containing annotations to image_chips not containing annotations (use 'inf' if only annotated chips are desired; only applicable if save_all == False <br>

<b>printout:</b> Suppress or print outputs.  If printout == 1, the filename will be printed to the terminal if an image chip is saved. If printout == 0, the print function is suppressed <br>

<b>tags:</b> Write annotation key tags to image xmp metadata.  If tags == 1, tags are enabled.  If tags == 0, the tags are disabled. <br>
</p>


   
##### 3.3 Annotation Key <a class ="anchor" id="3.3"></a>

   The main directory should already contain an Annotation_Key.txt file. If no Annotation_Key file is present, one will be generated automatically from the annotation files in the xml folder.<br>

   The Annotation_Key file contains every annotation key with its associated color code. In all image masks, annotations with that key will have the specified pixel value.  If an unknown key is encountered, it will be given a pixel value and added to the Annotation_Key automatically. <br>
   
   the AnnotationKey class generates and loads color codes from an annotation key. It contains the following functions: <br>
   
<code><b>class AnnotationKey</b>(object)</code>
   
<code>\__init\__(self, annotation_key)</code>
> Generates and loads color codes form annotation key <br>

> :param annotation_key:
   
<code>load_keys(self)</code> <br>

> Opens annotation_key file and loads keys and color codes <br>

> :return: color codes <br>

<code>add_keys(self, key)</code> <br>

> Adds new key and color_code to annotaiton key <br>

> :param key: The annotation to be added <br>
> :return: updated annotation key file <br>

<code>write_annotation_keys(self, annotations)</code> <br>

> Writes annotation keys and color codes to text file <br>

> :param annotations: Dictionary of annotation keys and color codes <br>
> :return: .txt file with annotation keys <br>

<code>generate_key(self, path)</code> <br>

> Generates annotation_key from folder of xml files <br>

> :param path: Directory containing xml files <br>
> :return: annotation_key file <br>

### 5. Output <a class ="anchor" id="5."></a>

##### 5.1 Image<span>&#95;</span>chips <a class ="anchor" id="5.1"></a>
Every generated image chip will be saved in the _output/image<span>&#95;</span>chips_ folder. The chips are saved with the naming convention of _slide filename<span>&#95;</span>level number<span>&#95;</span>row<span>&#95;</span>column.format_. If the chip contains an area that was annotated and the tags are enabled, it will have an associated tag (under the Subject category) with the annotation key. If the image chip does not contain annotations, the 'NONE' tag will be added. To view these tags, switch to details view and click display 'Subject' in the explorer. The files can be sorted according to their tags. Unfortunately, these tags will only be available if the output format is .jpg. <br>

The OutputSave class saves both the image chips and image masks, as well as attaching exif metadata to the images. It contains the following functions:

<code><b>class OutputSave</b>(object)</code>

<code>\__init\__(self, keys, print_save, tags)</code> <br>

> Save image chips and image masks

> :param keys: <br>
> :param print_save: <br>
> :param tags: <br>

<code>ensure_dir(self, directory)</code> <br>

> Ensures the existence of a directory <br>

> :param dest: Directory to ensure. <br>
> :return: new directory if it did not previously exist. <br>

<code>attach_tages(self)</code> <br>

> Attaches image tags to metadata of chips and masks <br>

> :param path: file to attach tags to. <br>
> :return: JPG with metadata tags<br>

<code>save_chip(self, chip, path, quality)</code> <br>

> Saves the image chips <br>

> :param chip: the slide image chip to save<br>
> :param path: the full path to the chip<br>
> :param quality: the output quality<br>

<code>save_mask(self, mask, path)</code><br>

> Saves the image mask <br>

> :param mask: the image mask to save<br>
> :param path: the complete path for the mask<br>

The main functionality of SlideSeg is performed by the ChipGenerator class. This class takes all of the inputs specified in parameters and uses it to generate image chips and image masks. It contains the following functions:

<code><b>class ChipGenerator</b>(object)</code>

<code>\__init\__(self, params)</code> <br>

> Generates image chips and masks from whole slides <br>

> :param params: the parameters specified in the parameters file
 
<code>open_slide(self, filename)</code> <br>

> Opens a whole slide image <br>

> :param filename: Slide image name. <br>
> :return: slide image, levels, and dimensions <br>

<code>curate_mask(self, mask, scale_width, scale_height)</code> <br>

> Resize and pad annotation mask if necessary <br>

> :param mask: <br>
> :param scale_width: <br>
> :param scale_height: <br>
> :return: curated annotation mask <br>

<code>get_chips(self, levels, dims, mask, annotations, filename, suffix)</code> <br>

> Finds chip locations that should be loaded and saved. <br>

> :param levels: levels in whole slide image <br>
> :param dims: dimension of whole slide image <br>
> :param mask: annotation mask for slide image <br>
> :param annotations: dictionary of annotations in image <br>
> :param filename: slide image filename <br>
> :param suffix: output format for saving. <br>
> :return: chip_dict. Dictionary of chip names, level, col, row, and scale <br>
> :return: image_dict. Dictionary of annotations and chips with those annotations <br>

##### 5.2 Image<span>&#95;</span>masks <a class ="anchor" id="5.2"></a>
An image mask for each image chip is saved in the _output/image<span>&#95;</span>masks folder_. The mask has the same name as the image chip it is associated with. Furthermore, these masks will have the same tags, allowing you to sort by annotation type. <br>

The class AnnotationMask handles the generation of an annotation mask from xml files. It contains the following functions: <br>

<code><b>class AnnotationMask</b>(object)</code>

<code>\__init\__(self, xml_filename, xml_path, size)</code> <br>

> Returns vertex points for annotations in xml file with their assigned keys <br>

> :param xml_filename: The xml file that contains the annotations <br>
> :param xml_path: Path to the xml file that contains the annotations <br>
> :param size: Size of corresponding slide image <br>  

<code>annotations(self)</code> <br>

> Reads xml file and makes annotation mask for entire slide image <br>

> :return: annotation mask <br>
> :return: dictionary of annotation keys and color codes<br>

##### 5.3 Text Files <a class ="anchor" id="5.3"></a>
A text file with details about annotations and image chips will also be saved to _output/textfiles_. For each slide image, this text file will contain a list of all annotation keys present in the image. For each annotation key, a list of every image chip/mask containing that specific key is also recorded in this file. <br>

The TextOutput class generates these .txt files. it contains the following functions: <br>

<code><b>class TextOutput</b>(object)</code>

<code>\__init\__(self, filename, annotations)</code> <br>

> Generates .txt file with image and annotation information <br>

> :param filename: filename of corresponding slide image <br>
> :param annotations: annotations contained in the slide image <br>

<code>write_keys(self)</code> <br>

> Writes each annotation key to the output text file. <br>

<code>write_key_img_list(self)</code> <br>

> Writes list of images containing each annotation key in the output .txt file<br>

### 6. Run <a class ="anchor" id="6."></a>

To execute SlideSeg, simply run the jupyter notebook cells. Alternatively, you can run the python script 'main.py'. Make sure that you defined the [Parameters](#3.2) above. If the python script is used, the parameters are specified in the Parameters.txt file. <br>
