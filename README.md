# SlideSeg

Spawar, Systems Center Pacific <br>
Created August 1, 2017 <br>
Author: Brendan Crabb <brendancrabb8388@pointloma.edu> 
<hr>

Welcome to SlideSeg, a python module that allows you to segment whole slide images into usable image
chips for deep learning. Image masks for each chip are generated from associated markup and annotation files.

## Table of Contents
[User Guide](#user-guide)

1.    [Dependencies](#1.)  
2.    [Anaconda Environment](#2.)  
      2.1 [Creating environment from .yml file](#2.1)
      2.2 [Installing C Libraries - Openslide (Windows)](#2.2)
      2.3 [Installing C Libraries - Openslide (Mac OS X)](#2.3)
      2.4 [Launching Jupyter Notebook](#2.4)
      2.5 [Change Jupyter Notebook startup folder (Windows)](#2.5)
      2.6 [Change Jupyter Notebook startup folder (OS X)](#2.6)
      2.7 [Jupyter Kernel Selection](#2.7)
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

##### 2.2 Installing C Libraries - Openslide (Windows)  <a class ="anchor" id="2.2"></a>

OpenSlide is a C library; as a result, it has to be installed separately from
the conda environment, which contains all of the python dependencies.

The Windows Binaries for OpenSlide can be found at 'openslide.org/download/'.
Download the appropriate binaries for your system (either 32-bit or 64-bit) and
unzip the file.  Copy the .dll files in ../bin/ to .../Anaconda/envs/SlideSeg/Library/bin/.
Copy the .h files to .../Anaconda/envs/SlideSeg/include/. Finally, copy the
.lib file to .../Anaconda/envs/SlideSeg/libs/.  OpenSlide has now been installed.

##### 2.3 Installing C Libraries - Openslide (Mac OS X)  <a class ="anchor" id="2.3"></a>

OpenSlide is a C library; as a result, it has to be installed separately from
the conda environment, which contains all of the python dependencies.

If you are using MacPorts, simply enter the following in the terminal:

<code>port install openslide</code>

If you are using Homebrew, enter the following in the terminal:

<code>brew install openslide</code>

OpenSlide should now be installed in your anaconda environment.

##### 2.4 Launching Jupyter Notebook  <a class ="anchor" id="2.4"></a>

The Jupyter Notebook App can be launched by clicking on the Jupyter Notebook icon installed by Anaconda in the start menu (Windows) or by typing in the terminal (cmd on Windows): 

<code>jupyter notebook</code>

This will launch a new browser window showing the Notebook Dashboard.  When started, the Jupyter Notebook app can only access files within its start-up folder.  If you stored the SlideSeg notebook documents in a subfolder of your user folder, no configuration is necessary.  Otherwise, you need to change your Jupyter Notebook App start-up folder.  

#####  2.5 Change Jupyter Notebook startup folder (Windows) <a class ="anchor" id="2.5"></a>

* Copy the *Jupyter Notebook* launcher from the menu to the desktop. <br>
* Right click on the new launcher, select properties, and change the *Target field*, change %USERPROFILE% to the full path of the folder which will contain all the notebooks. <br>
* Double-click on the *Jupyter Notebook* desktop launcher (icon shows [IPy]) to start the Jupyter Notebook App, which will open in a new browser window (or tab). Note also that a secondary terminal window (used only for error logging and for shut down) will be also opened. If only the terminal starts, try opening this address with your browser: http://localhost:8888/. <br>

##### 2.6 Change Jupyter Notebook startup folder (OS X) <a class ="anchor" id="2.6"></a>
To launch Jupyter Notebook App:

* Click on spotlight, type terminal to open a terminal window.
* Enter the startup folder by typing cd /some_folder_name.
* Type jupyter notebook to launch the Jupyter Notebook App (it will appear in a new browser window or tab). <br>

##### 2.7 Jupyter Kernel Selection <a class ="anchor" id = "2.7"></a>
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
</p>
   
##### 3.3 Annotation Key <a class ="anchor" id="3.3"></a>

   The main directory should already contain an Annotation_Key.txt file. If no Annotation_Key file is present, one will be generated automatically from the annotation files in the xml folder.<br>

   The Annotation_Key file contains every annotation key with its associated color code. In all image masks, annotations with that key will have the specified pixel value.  If an unknown key is encountered, it will be given a pixel value and added to the Annotation_Key automatically. <br>
   
The following functions are defined within the slideseg module and used to generate, edit, and read the annotation key: <br>

```
<code>def loadkeys(annotation_key):
    """
    Opens annotation_key file and loads keys and color codes
    :param: annotation_key: the filename of the annotation key
    :return: color codes
    """
    
def addkeys(annotation_key, key):
    """
    Adds new key and color_code to annotation key
    :param annotation_key: the filename of the annotation key
    :param key: The annotation to be added
    :return: updated annotation key file
    """
    
 def writeannotations(annotation_key, annotations):
    """
    Writes annotation keys and color codes to annotation key text file
    :param annotation_key: filename of annotation key
    :param annotations: Dictionary of annotation keys and color codes
    :return: .txt file with annotation keys
    """
    
def generatekey(annotation_key, path):
    """
    Generates annotation_key from folder of xml files
    :param annotation_key: the name of the annotation key file
    :param path: Directory containing xml files
    :return: annotation_key file
    """
```

### 5. Output <a class ="anchor" id="5."></a>

##### 5.1 Image<span>&#95;</span>chips <a class ="anchor" id="5.1"></a>
Every generated image chip will be saved in the _output/image<span>&#95;</span>chips_ folder. The chips are saved with the naming convention of _slide filename<span>&#95;</span>level number<span>&#95;</span>row<span>&#95;</span>column.format_. If the chip contains an area that was annotated and the tags are enabled, it will have an associated tag (under the Subject category) with the annotation key. If the image chip does not contain annotations, the 'NONE' tag will be added. To view these tags, switch to details view and click display 'Subject' in the explorer. The files can be sorted according to their tags. Unfortunately, these tags will only be available if the output format is .jpg. <br>

The following functions are defined in the slideseg module and are used to save both the image chips and image masks, as well as attaching exif metadata to the images:

```
def ensuredirectory(dest): 
    """ 
    Ensures the existence of a directory 
    :param dest: Directory to ensure.
    :return: new directory if it did not previously exist. 
    """ 

def attachtags(path, keys):
    """
    Attaches image tags to metadata of chips and masks
    :param path: file to attach tags to.
    :param keys: keys to attach as tags
    :return: JPG with metadata tags 
    """

def savechip(chip, path, quality, keys):
    """
    Saves the image chip
    :param chip: the slide image chip to save
    :param path: the full path to the chip
    :param quality: the output quality
    :param keys: keys associated with the chip
    :return:
    """

def savemask(mask, path, keys):
    """
    Saves the image masks
    :param mask: the image mask to save
    :param path: the complete path for the mask
    :param keys: keys associated with the chip
    :return:
    """

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

def formatcheck(format):
    """
    Assures correct format parameter was defined correctly
    :param format: the output format parameter
    :return: format
    :return: suffix
    """
```

The following functions are defined in the slideseg module and are used to save both the image chips and image masks, as well as attaching exif metadata to the images:

```
def ensuredirectory(dest):
    """
    Ensures the existence of a directory
    :param dest: Directory to ensure.
    :return: new directory if it did not previously exist.
    """

def attachtags(path, keys):
    """
    Attaches image tags to metadata of chips and masks
    :param path: file to attach tags to.
    :param keys: keys to attach as tags
    :return: JPG with metadata tags
    """

def savechip(chip, path, quality, keys):
    """
    Saves the image chip
    :param chip: the slide image chip to save
    :param path: the full path to the chip
    :param quality: the output quality
    :param keys: keys associated with the chip
    :return:
    """

def savemask(mask, path, keys):
    """
    Saves the image masks
    :param mask: the image mask to save
    :param path: the complete path for the mask
    :param keys: keys associated with the chip
    :return:
    """

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

def formatcheck(format):
    """
    Assures correct format parameter was defined correctly
    :param format: the output format parameter
    :return: format
    :return: suffix
    """
```

##### 5.2 Image<span>&#95;</span>masks <a class ="anchor" id="5.2"></a>
An image mask for each image chip is saved in the _output/image<span>&#95;</span>masks folder_. The mask has the same name as the image chip it is associated with. Furthermore, these masks will have the same tags, allowing you to sort by annotation type. <br>

The following function handles the generation of an annotation mask from xml files: <br>

```
def makemask(annotation_key, size, xml_path):
    """
    Reads xml file and makes annotation mask for entire slide image
    :param annotation_key: name of the annotation key file
    :param size: size of the whole slide image
    :param xml_path: path to the xml file
    :return: annotation mask
    :return: dictionary of annotation keys and color codes
    """
```

##### 5.3 Text Files <a class ="anchor" id="5.3"></a>
A text file with details about annotations and image chips will also be saved to _output/textfiles_. For each slide image, this text file will contain a list of all annotation keys present in the image. For each annotation key, a list of every image chip/mask containing that specific key is also recorded in this file. <br>

The following functions generates these .txt files: <br>

```
def writekeys(filename, annotations):
    """
    Writes each annotation key to the output text file
    :param filename: filename of image chip
    :param annotations: dictionary of annotation keys
    :return: updated text file
    """

def writeimagelist(filename, image_dictionary):
    """
    Writes list of images containing each annotation key
    :param filename: the name of the slide image
    :param image_dictionary: dictionary of images with each key
    :return text
    """
```

### 6. Run <a class ="anchor" id="6."></a>

To execute SlideSeg, simply open the jupyter notebook and run the cells. Alternatively, you can run the python script 'main.py'. Make sure that you defined the [Parameters](#3.2). If the python script is used, the parameters are specified in the Parameters.txt file. <br>
