from __future__ import division
import numpy as np
import cv2
#import SimpleCV


GBARES = (240,160)

img = cv2.imread('usepursuit.png', 1)

print img.shape # (y, x, ?)
scaling_factor = (img.shape[1] / GBARES[0], img.shape[0] / GBARES[1])
print "scaling factor:", scaling_factor

template = cv2.imread('char-Pwhite.png', 1)
# resize template to match
template_oldsize = template.shape
template_newsize = (template_oldsize[1]*3, template_oldsize[0]*3)
template = cv2.resize(template, template_newsize)

result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)

print result
#matchpos = np.unravel_index(np.argmax(result), result.shape)
#print matchpos
#matchpos = (matchpos[1], matchpos[0])

minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(result)

print minLoc

cv2.rectangle(img, minLoc, (0,0), -1)

cv2.imshow('template',template)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
