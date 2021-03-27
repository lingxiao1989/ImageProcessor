from scipy import integrate
import math
from cv2 import cv2 as cv2
import numpy

class circle_mapping_table:
  def __init__(self,r):
    self.table = {}
    self.r = r
    for i in range (self.r):
      val,err = integrate.quad(lambda x,r:r * math.sqrt(1/(r**2-x**2)),0,i,args=(self.r,))
      self.table[int(val)] = i
    self.last = 0
    for j in range (int(r*3.14/2)):
      self.map_point(j)

  def map_point(self,input):
    if input in self.table:
      self.last = self.table[input]
      return self.table[input]
    else:
      return self.last

  def get_table(self):
    return self.table

class egg_curve_mapping_table:
  def __init__(self,r,a,b):
    self.table_a = {}
    self.table_b = {}
    self.r = r
    self.a = a
    self.b = b
    for i in range (self.a):
      val,err = integrate.quad(
        lambda x, r, a, b: r * math.sqrt((1 - (a+b)**2*x**2/(2*a*b + x*(a - b))**2 )) * (-0.5*(a+b)**2*x**2*(-2*a + 2*b)/(2*a*b + x*(a - b))**3 - (a+b)**2*x/(2*a*b + x*(a - b))**2),
        0,i,
        args=(self.r,self.a,self.b))
      self.table_a[int(val)] = i
    for i in range (self.b):
      val,err = integrate.quad(
        lambda x, r, a, b: r * math.sqrt((1 - (a+b)**2*x**2/(2*a*b + x*(a - b))**2 )) * (-0.5*(a+b)**2*x**2*(-2*a + 2*b)/(2*a*b + x*(a - b))**3 - (a+b)**2*x/(2*a*b + x*(a - b))**2),
        0,i,
        args=(self.r,self.a,self.b))
      self.table_b[int(val)] = i
    self.last_a = 0
    self.last_b = 0
  def map_point_a(self,input):
    if input in self.table_a:
      self.last_a = self.table_a[input]
      return self.table_a[input]
    else:
      return self.last_a

  def map_point_b(self,input):
    if input in self.table_b:
      self.last_b = self.table_b[input]
      return self.table_b[input]
    else:
      return self.last_b

def oval_func(x, r, s, l):
  return r**2 * math.sqrt(1-(s+l)**2 * x**2/((l-s)*x+2*s*l)**2)
  
def curve_ext(input_img):
  ##make new empty image.
  pi=3.1415
  ratio = 0.4
  img=cv2.imread(input_img,0)
  h,w = img.shape
  r = int(h/2)
  s = int(w * ratio)
  l = int(w * (1-ratio))
  h_out = int(h*pi/2)
  w_out = int(w*pi/2)
  table_c = circle_mapping_table(r)
  table_e = egg_curve_mapping_table(r, s, l)
  print("input hight:", h)
  print("input weight:", w)
  print("output hight:", h_out)
  print("output weight:", w_out)
  result = numpy.zeros((h_out,w_out),numpy.uint8)
  x_draft = {}
  y_draft = {}
    for i in range(w):
      y = oval_func(i-s, r, s, l)
      y_draft[i] = table_c.get_table(y)
    for j in range(h):

  for i in range(int(h/2)):
    table=circle_mapping_table(i)
    y_draft[i]=table.get_table()
    
  table_c = circle_mapping_table(int(h/2))
  table_e = egg_curve_mapping_table(int(h/2), int(w/0.4), int(w/0.6))

  ##for iteration to calcaulate mapping point in the original image. Round the float value.
  offset=int(h_out/2)
  for i in range (w_out):
    for j in range(offset):
      result[offset+j, i] = img[int(h/2)+table_c.map_point(j), i]
      result[offset-j, i] = img[int(h/2)-table_c.map_point(j), i]
  
    #print (table.map_point(i))

  ##return the new image.
  return result

def main():
  #val,err = integrate.quad(circle_func, -2,2, args=(2,))
  #print(val)
  img_file = 'egg.png'
  result = curve_ext(img_file)
  cv2.imshow('result', result)
  cv2.imwrite('result.png', result)
  cv2.waitKey(0)

if __name__ == "__main__":
  main()