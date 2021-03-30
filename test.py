import numpy as np
import cv2
from cv2 import Stitcher
 
# if __name__ == "__main__":
#  img1 = cv2.imread('result1.png') 
#  img2 = cv2.imread('result2.png') 
#  img3 = cv2.imread('result3.png') 
#  img4 = cv2.imread('result4.png')
#  #res1 = cv2.resize(img1,(300,400),interpolation=cv2.INTER_CUBIC)
#  #res2 = cv2.resize(img2,(300,400),interpolation=cv2.INTER_CUBIC)

#  test1 = cv2.imread('img1.png') 
#  test2 = cv2.imread('img1.png') 
#  stitcher = cv2.createStitcher(False)
#  #stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA), 根据不同的OpenCV版本来调用
#  (_result, pano) = stitcher.stitch((test1, test2))
#  cv2.imshow('pano',pano)
#  #cv2.waitKey(0)


 
if __name__ == "__main__":
 test1 = cv2.imread('img1.png') 
 test2 = cv2.imread('img1.png') 
 stitcher = cv2.createStitcher(False)
 #stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA), 根据不同的OpenCV版本来调用
 (_result, pano) = stitcher.stitch((test1, test2))
 cv2.imshow('pano',pano)
 cv2.waitKey(0)