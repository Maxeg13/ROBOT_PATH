# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:07:46 2019

@author: student
"""
import cv2
import numpy as np
# black blank image
zero_img = np.zeros((512, 512, 3),np.uint8)
ones_img = 255*np.ones((10, 10, 3),np.uint8)
zero_img[0:10,0:10]=ones_img.copy()
#pts_=np.array( np.int_([[1,1],[1,20],[20,20],[20,1]]),np.uint8);
#cv2.fillPoly(blank_image,pts_,(255,255,0))
# print(blank_image.shape)
cv2.imshow("Black Blank", zero_img)

cv2.waitKey(0)
cv2.destroyAllWindows()