__author__ = 'Isai Olvera'
 
from PIL import Image
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from skimage.filter.rank import entropy
from skimage.morphology import disk
from skimage.util import img_as_ubyte
from skimage import color
from skimage import io
import skimage

##Luminance conversion formula from http://en.wikipedia.org/wiki/Luminance_(relative)
def luminosity(rgb, rcoeff=0.2126, gcoeff=0.7152, bcoeff=0.0722):
    return rcoeff * rgb[0] + gcoeff * rgb[1] + bcoeff * rgb[2]
#
#
## Take a PIL rgb image and produce a factory that yields
## ((x,y), r,g,b)), where (x,y) are the coordinates
## of a pixel, (x,y), and its RGB values.
def gen_pix_factory(im):
    num_cols, num_rows = im.size
    r, c = 0, 0
    while r != num_rows:
        c = c % num_cols
        yield ((c, r), im.getpixel((c, r)))
        if c == num_cols - 1: r += 1
        c += 1
#
#
## take a PIL RGB image and a luminosity conversion formula,
## and return a new gray level PIL image in which each pixel
## is obtained by applying the luminosity formula to the
## corresponding pixel in the RGB values.
def rgb_to_gray_level(rgb_img, conversion=luminosity):
    gl_img = Image.new('L', rgb_img.size)
    gen_pix = gen_pix_factory(rgb_img)
    lum_pix = ((gp[0], conversion(gp[1])) for gp in gen_pix)
    for lp in lum_pix:
        gl_img.putpixel(lp[0], int(lp[1]))
    return gl_img
#
#
## Take a gray level image and a gray level threshold and
## replace a pixel's gray level with 0 (black) if it's gray
## level value is <= than the threshold and with
## 255 (white) if it's > than the threshold.
def binarize(gl_img, thresh):
    gen_pix = gen_pix_factory(gl_img)
    for pix in gen_pix:
        if pix[1] <= thresh:
            gl_img.putpixel(pix[0], 0)
        else:
            gl_img.putpixel(pix[0], 255)
#
#
## Take a binarized image and count every pixel that is black
def pixel_counter(binarized_image, black=0):
    gen_pix = gen_pix_factory(binarized_image)
    count = 0
    for pix in gen_pix:
        if pix[1] == black:
            count += 1
    return count
#
#

def rebinarizeImage(path, imagename, threshold):
    image = Image.open(os.path.join(path, imagename))
    binarized_image = rgb_to_gray_level(image)        # Converts the image that was just imported to grayscale
    binarize(binarized_image, threshold)                 # Binarizes the now grayscale image
    defect_count = pixel_counter(binarized_image)       # Counts the black pixels in the image and returns them to defect_count
    binarized_image.save(os.path.join(path, "bin_" + imagename))
    binfile = "/uploads/bin_" + imagename

    jsondict = {"image":binfile,"count":defect_count}
    return jsondict


def binarizeImage(path, imagename, threshold):
    image = Image.open(os.path.join(path, imagename))
    binarized_image = rgb_to_gray_level(image)        # Converts the image that was just imported to grayscale
    binarize(binarized_image, threshold)                 # Binarizes the now grayscale image
    defect_count = pixel_counter(binarized_image)       # Counts the black pixels in the image and returns them to defect_count
    binarized_image.save(os.path.join(path, "bin_" + imagename))
    return defect_count

def entropyImage(path, imagename):

    entropyimage_import = skimage.io.imread(os.path.join(path, imagename), as_grey=True)
    entropy_image = entropy(entropyimage_import, disk(5))
    plt.imsave(os.path.join(path, "ent_" + imagename), entropy_image)


def heatmapImage(path, imagename):

    heatmapimage_import = skimage.color.rgb2gray(mpimg.imread(os.path.join(path, imagename)))
    heatmapubyte = img_as_ubyte(heatmapimage_import)
    plt.imsave(os.path.join(path, "heat_" + imagename), heatmapubyte)
