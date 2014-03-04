from __future__ import division
import numpy as np
import cv2
import sys
import os, os.path

CHARWINWIDTH = 7
CHARWINMOVE = 5

GBARES = (240,160)

class pkmnimage:
    overridechars = {'period': '.', 'questionmark': '?', 'space': ' ', 'exclamationmark': '!', 'apostrophe':"'", 'hyphen': '-'}
    def __init__(self, image):
        self.img = cv2.resize(image, GBARES)
        self.letters = {}
        self.initletters()
        self.showeveryletter = False # debug flag
        self.charwinwidth = {'battletext': 7, 'movetext': 5}

    def initletters(self):
        for lettermap in os.listdir('letters/'):
            self.letters[lettermap] = []
            for limg in os.listdir('letters/' + lettermap + '/'):
                letterimg = cv2.imread('letters/' + lettermap + '/' + limg, 1)
                # TODO: this is bad, fix it.
                if limg[:3] == 'cap':
                    self.letters[lettermap].append((limg[3:-4], letterimg))
                elif limg[:-4] in self.overridechars:
                    self.letters[lettermap].append((self.overridechars[limg[:-4]], letterimg))
                else:
                    self.letters[lettermap].append((limg[:-4], letterimg))

    def get_text_in_region(self, bounds, lettermap):
        line = self.read_line(self.cropimg(self.img, bounds), lettermap)
        return "".join(line)



    def id_letter(self,img,lettermap):
        #identify best letter match in a region

        smallest = "*"
        smallestVal = -1 #arbitrarily large. TODO: do something smarter
        smallestwidth = -1 # needed to advance cursor
        for l in self.letters[lettermap]:
            letterstr = l[0]
            letterimg = l[1]
            result = cv2.matchTemplate(img, letterimg, cv2.TM_SQDIFF)
            minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(result)

            if minVal < smallestVal or smallestVal == -1:
                smallestVal=minVal
                smallest = letterstr
                smallestwidth = letterimg.shape[1]

        # mark up image with found stuff
        #cv2.rectangle(img, minLoc, (0,0), -1)

        if smallest not in [' ', ''] and self.showeveryletter:
            cv2.imshow('image',img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        #if smallestVal > 7000000:
            #return ('', 2)
        return (smallest, smallestwidth)

    def read_line(self, imgline, lettermap):
        lineheight = imgline.shape[0]
        linewidth = imgline.shape[1]

        pos = 0
        chars = []
        while pos < linewidth - self.charwinwidth[lettermap]:
            # magic?
            #letter = self.id_letter(self.cropimg(imgline,((max(pos-3,0),0),(pos + CHARWINWIDTH, lineheight))), lettermap)
            letter = self.id_letter(self.cropimg(imgline,((pos,0),(pos + self.charwinwidth[lettermap], lineheight))), lettermap)
            chars.append(letter[0])
            #print "".join(chars)
            pos += letter[1]

        return chars
    def cropimg(self,img,bounds):
        return img[bounds[0][1]:bounds[1][1], bounds[0][0]:bounds[1][0]]

    def get_battletext(self):
        # return generic text displayed in battle.
        line1_bounds = ((10,122),(230,122+16))
        line2_bounds = ((10,138),(230,138+16))
        line1 = self.get_text_in_region(line1_bounds, 'battletext')
        line2 = self.get_text_in_region(line2_bounds, 'battletext')
        return [line1,line2]

    def get_movetext(self):
        # return all moves in the move selection screen
        move_bounds = [((16,125),(80,133)), ((88,125),(152,133)), ((16,141),(80,149)), ((88,141),(152,149))]
        moves = [pkimg.get_text_in_region(bound, 'movetext') for bound in move_bounds]
        return moves




pkimg = pkmnimage(cv2.imread(sys.argv[1], 1))

#textbox_bounds = ((8,120),(230,152))
#textbox_bounds = ((8,123),(230,138))

print "BATTLE TEXT:", pkimg.get_battletext()
print "MOVES:", pkimg.get_movetext()

#cv2.imshow('image',pkimg.img)
#cv2.imshow('image',cropimg(img,l2_tb_bounds))
cv2.waitKey(0)
cv2.destroyAllWindows()
