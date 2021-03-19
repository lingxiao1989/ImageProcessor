from scipy import integrate
import math
from cv2 import cv2 as cv2
import numpy

class mapping_table:
  def __init__(self,func,r):
    self.table=[]
    self.r=r
    self.func=func
    fill_table()
  def fill_table(self):
    for i in range self.r:
      self.table[i] = integrate.quad(self.func,0,i)
  def map_point(self,input):
    return self.table[input]
  

def egg_func(x):
  return x

def circle_func(x,r):
  return r * math.sqrt(1/(r**2-x**2))

def curve_ext(input_img):
  ##make new empty image.
  pi=3.1415
  img=cv2.imread(input_img,0)
  h,w = img.shape
  h_out = int(h*pi)
  w_out = w
  result = numpy.zeros((h_out,w_out),numpy.uint8)
  table = mapping_table(circle_func, h)
  ##for iteration to calcaulate mapping point in the original image. Round the float value.
    for i in range (w_out):
      for j in range(h_out):
        result[j,i] = img[table.map_point(j),i]
  ##return the new image.
  return result

def main():
  print(integrate.quad(circle_func))

if __name__ == "__main__":
  main()