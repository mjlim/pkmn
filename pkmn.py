from __future__ import division
import numpy as np
import cv2
import sys
import os, os.path
#import SimpleCV

CHARWINWIDTH = 8
CHARWINMOVE = 5

class scalehelper:
    def __init__(self,native, scaled):
        self.native = native
        self.scaled = scaled
        self.scaling_factor = (int(scaled[0] / GBARES[0]), int(scaled[1] / GBARES[1]))
        print "SF:", self.scaling_factor
    def scalecoords(self,coords):
        return (self.scaling_factor[0] * coords[0], self.scaling_factor[1] * coords[1])
    def scalerect(self,rect):
        return (self.scalecoords(rect[0]), self.scalecoords(rect[1]))
    def scalex(self,num):
        return self.scaling_factor[0] * num

def id_letter(img):
    #identify best letter match in a region
    global letters

    smallest = "*"
    smallestVal = -1 #arbitrarily large. TODO: do something smarter
    smallestwidth = -1 # needed to advance cursor
    for l in letters:
        letterstr = l[0]
        letterimg = l[1]
        result = cv2.matchTemplate(img, letterimg, cv2.TM_SQDIFF)
        minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(result)

        if minVal < smallestVal or smallestVal == -1:
            smallestVal=minVal
            smallest = letterstr
            smallestwidth = letterimg.shape[1]

    cv2.rectangle(img, minLoc, (0,0), -1)

    if smallest not in [' ', '']:
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #if smallestVal > 7000000:
        #return ('', 2)
    return (smallest, smallestwidth)

def read_line(imgline):
    global CHARWINWIDTH

    lineheight = imgline.shape[0]
    linewidth = imgline.shape[1]

    pos = 0
    chars = []
    while pos < linewidth - CHARWINWIDTH:
        letter = id_letter(cropimg(imgline,((pos,0),(pos + CHARWINWIDTH, lineheight))))
        chars.append(letter[0])
        print "".join(chars)
        pos += letter[1]

    return chars




def cropimg(img,bounds):
    return img[bounds[0][1]:bounds[1][1], bounds[0][0]:bounds[1][0]]

GBARES = (240,160)

img = cv2.imread(sys.argv[1], 1)

scalehelper = scalehelper(GBARES, (img.shape[1], img.shape[0]))

# update charwin vars
CHARWINWIDTH = scalehelper.scalex(CHARWINWIDTH)
CHARWINMOVE = scalehelper.scalex(CHARWINMOVE)


letters = []
for limg in os.listdir('letters/battletext'):
    letterimg = cv2.imread('letters/battletext/' + limg, 1)
    letter_oldsize = (letterimg.shape[1], letterimg.shape[0])
    letter_newsize = scalehelper.scalecoords(letter_oldsize)
    print letter_oldsize, letter_newsize
    letterimg = cv2.resize(letterimg, letter_newsize)

    # TODO: this is bad, fix it
    if limg[:3] == 'cap':
        letters.append((limg[3:-4], letterimg))
    elif limg[:-4] == 'space':
        letters.append((' ', letterimg))
    else:
        letters.append((limg[:-4], letterimg))


#textbox_bounds = ((8,120),(230,152))
#textbox_bounds = ((8,123),(230,138))
textbox_bounds = ((10,123),(230,138))
sc_tb_bounds = scalehelper.scalerect(textbox_bounds)

line2_bounds = ((9,138),(230,152))
l2_tb_bounds = scalehelper.scalerect(line2_bounds)

print sc_tb_bounds

#template = 
# resize template to match
#template_oldsize = template.shape
#template_newsize = (template_oldsize[1]*3, template_oldsize[0]*3)
#template = cv2.resize(template, template_newsize)
#
#result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)

#matchpos = np.unravel_index(np.argmax(result), result.shape)
#print matchpos
#matchpos = (matchpos[1], matchpos[0])

#minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(result)

#print minLoc

#cv2.rectangle(img, minLoc, (0,0), -1)

print read_line(cropimg(img, sc_tb_bounds))
print read_line(cropimg(img, l2_tb_bounds))
#for i in letters:
    #cv2.imshow('template'+i[0],i[1])
cv2.imshow('image',cropimg(img,l2_tb_bounds))
cv2.waitKey(0)
cv2.destroyAllWindows()
