# LineLabels

Tkinter app in Python 3 to label lines

## Setup
Clone the repo:
- `git clone https://github.com/ericke8/LineLabels.git`

Dependencies:
- `tkinter`
- `PIL` (Pillow)
- `os`
- `sys`
- `platform`

## Usage
By default, the script will create a folder called `lineCuts` on the same level as the directory of images, if you do not provide an output directory.  The script will go through all of the images in the folder, or until you exit the application.

**Note: As of present, the script only takes `.tif` files!**

- `cd LineLabels`
- `python app.py [directory to images] [optional directory to output]`

To label the image, just click anywhere on the image and it will create a red line indicating a cut.  To remove already existing lines, switch to remove mode via the buttons on the right and click on the line to remove.

After you are finished labelling an image, click on the next page button, and it will save a csv file named `name-of-original-image_lineCuts.csv` to the output directory.
