from __future__ import division
import numpy as np
import cv2
import sys
import os, os.path
import time

CHARWINWIDTH = 7
CHARWINMOVE = 5
SPACE_THRESHOLD = 3 # a space of 3 pixels wide or longer without any text pixels detected is considered a space
COLOR_THRESHOLD = 15

GBARES = (240,160)

class pkmnimage:
    overridechars = {'period': '.', 'questionmark': '?', 'space': ' ', 'exclamationmark': '!', 'apostrophe':"'", 'hyphen': '-'}
    def __init__(self, image):
        self.img = cv2.resize(image, GBARES)
        self.letters = {}
        self.initletters()
        self.showeveryletter = False # debug flag
        self.charwinwidth = {'battletext': 7, 'movetext': 5}
        self.chartextcolor = {'battletext': np.array([255,255,255]), 'movetext': np.array([74,73,74])}

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
        line = self.read_line(self.cropimg(self.img, bounds), lettermap, self.chartextcolor[lettermap])
        return "".join(line)



    def id_letter(self,img,lettermap):
        #identify best letter match in a region

        smallest = "*"
        smallestVal = -1 #arbitrarily large. TODO: do something smarter
        smallestwidth = -1 # needed to advance cursor
        for l in self.letters[lettermap]:
            letterstr = l[0]
            letterimg = l[1]

            # don't try to match if the letter is bigger than our region.
            if letterimg.shape[0] > img.shape[0] or letterimg.shape[1] != img.shape[1]:
                continue
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

    def read_line(self, imgline, lettermap, textcolor):
        lineheight = imgline.shape[0]
        linewidth = imgline.shape[1]
        left = 0
        line = []
        space = 0
        prev_num_txpx = -1
        for right in range(1,linewidth):
            # scan this column for text color pixels.
            num_txpx = 0 # number of text colored pixels found
            for y in range(0,lineheight):
                if (abs(imgline[y][right] - textcolor) < COLOR_THRESHOLD).all():
                    num_txpx += 1
            if num_txpx == 0:
                if prev_num_txpx > 0: # previous column had some text pixels in it, so this is column terminates that character
                    if space > SPACE_THRESHOLD:
                        line.append(' ')
                    space = 0

                    candidate = self.cropimg(imgline,((left,0),(right+1,lineheight)))
                    #cv2.imshow('candidate', candidate)
                    #cv2.waitKey(0)
                    letter = self.id_letter(candidate, lettermap)
                    line.append(letter[0])
                else: # the previous column was also blank, so we're in a space
                    space += 1
                left = right + 1
            prev_num_txpx = num_txpx
        return line


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
        moves = [self.get_text_in_region(bound, 'movetext') for bound in move_bounds]
        return moves




if __name__ == '__main__':
    pkimg = pkmnimage(cv2.imread(sys.argv[1], 1))

    #textbox_bounds = ((8,120),(230,152))
    #textbox_bounds = ((8,123),(230,138))

    start = time.clock()
    print "BATTLE TEXT:", pkimg.get_battletext()
    print "MOVES:", pkimg.get_movetext()
    end = time.clock()
    print "%.2gs" % (end-start)

    #cv2.imshow('image',pkimg.img)
    #cv2.imshow('image',cropimg(img,l2_tb_bounds))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
