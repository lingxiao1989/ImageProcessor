from scipy import integrate
import math
from cv2 import cv2 as cv2
import numpy

class circle_mapping_table:
  def __init__(self,r):
    self.full_table = {}
    self.r = r
    for i in range(self.r+1):
      self.full_table[i]=self._get_table(i)

  def _get_table(self, r):
    current_table={}
    for i in range (r):
      val,err = integrate.quad(lambda x,r:r * math.sqrt(1/(r**2-x**2)),0,i,args=(r,))
      current_table[i] = int(val)
    return current_table

  def check_table(self, r):
    return self.full_table[r]

class egg_curve_mapping_table:
  def __init__(self,r,s,l):
    self.full_table_s = {}
    self.full_table_l = {}
    self.r = r
    self.s = s
    self.l = l
    self.correlations = oval_func(r, s, l)
    for i in range (self.r):
      i_s, i_l = self.correlations.get_x(i)
      self.full_table_s[i_s], self.full_table_l[i_l]= self._get_table(int(math.sqrt(self.r**2-i**2)),i_s,i_l)

  def _get_table(self, r, s, l):
    current_table_r = {}
    current_table_l = {}
    for i in range (s):
      val,err = integrate.quad(
        lambda x, r, s, l: math.sqrt(1 + (r * math.sqrt(1 - (s + l)**2 * x**2/(2*s*l + x*(l - s))**2 ) * (-0.5*(s + l)**2 * x**2 * (-2*l + 2*s)/(2*s*l + x*(l - s))**3 - (s + l)**2*x/(2*s*l + x*(l - s))**2))**2),
        i-s,0,
        args=(r, s, l,))
      current_table_r[i] = int(val)
    for j in range (l+1):
      val,err = integrate.quad(
        lambda x, r, s, l: math.sqrt(1 + (r * math.sqrt(1 - (s + l)**2 * x**2/(2*s*l + x*(l - s))**2 ) * (-0.5*(s + l)**2 * x**2 * (-2*l + 2*s)/(2*s*l + x*(l - s))**3 - (s + l)**2*x/(2*s*l + x*(l - s))**2))**2),
        0,j,
        args=(r, s, l,))
      current_table_l[j] = int(val)
    return current_table_r, current_table_l

  def check_table(self, r):
    s, l = self.correlations.get_x(r)
    return self.full_table_s[s], self.full_table_l[l]

class oval_func:
  def __init__(self,r,s,l):
    self.short_curve_x={}
    self.long_curve_x={}
    self.short_curve_y={}
    self.long_curve_y={}
    self.s = s
    temp_table={}
    last_y=0
    for i in range(s+1):
      temp = i-s
      self.short_curve_x[i] = int(r * math.sqrt(1-(s+l)**2 * temp**2/((l-s)*temp+2*s*l)**2))
      temp_table[self.short_curve_x[i]]= s-i
    for k in range(r+1):
      if k in temp_table:
        self.short_curve_y[k] = temp_table[k]
        last_y = temp_table[k]
      else:
        self.short_curve_y[k] = last_y
    temp_table={}
    last_y=0
    for j in range(l+1):
      self.long_curve_x[j] = int(r * math.sqrt(1-(s+l)**2 * j**2/((l-s)*j+2*s*l)**2))
      temp_table[self.long_curve_x[j]] = j
    for g in range(r+1):
      if g in temp_table:
        self.long_curve_y[g] = temp_table[g]
        last_y = temp_table[g]
      else:
        self.long_curve_y[g] = last_y

  def get_y(self, x):
    if x < self.s:
      return self.short_curve_x[x]
    else:
      return self.long_curve_x[x-self.s]

  def get_x(self, y):
    return self.short_curve_y[y], self.long_curve_y[y]

def curve_ext(input_img, ratio = 0.46):
  ## make new empty image.
  pi=3.14159
  img=cv2.imread(input_img)
  h,w,c = img.shape
  r = int(h/2)
  s = int(w * ratio)
  l = int(w * (1-ratio))
  h_out = int(h*pi/2)
  w_out = int(w*pi/2)
  print("input hight:", h)
  print("input weight:", w)
  print("output hight:", h_out)
  print("output weight:", w_out)

  ## for iteration to calcaulate mapping point in the original image. Round the float value.
  correlations = oval_func(r, s, l)
  table_c = circle_mapping_table(r)
  table_e = egg_curve_mapping_table(r, s, l)
  result = numpy.zeros((h_out,w_out,c),numpy.uint8)
  x_draft_s = {}
  x_draft_l = {}
  y_draft = {}
  for i in range(w):
    y = correlations.get_y(i)
    y_draft[i] = table_c.check_table(y)
  for j in range(r):
    x_draft_s[j], x_draft_l[j] = table_e.check_table(j)

  ## generating the output image.
  # for i in range (w):
  #   y_maps =  y_draft[i]
  #   for key in y_maps:
  #     result1[offset+key, i] = img[int(h/2)+key, i]
  #     result1[offset-key, i] = img[int(h/2)-key, i]
  offset=int(h_out/2)
  for k in range(c):
    for i in range (w):
      y_maps =  y_draft[i]
      for key in y_maps:
        result[offset+y_maps[key], i, k] = img[int(h/2)+key, i, k]
        result[offset-y_maps[key], i, k] = img[int(h/2)-key, i, k]

    for i in range (w):
      for j in range (2, offset):
        if result[j,i,k] == 0:
          result[j,i,k] = result[j-1,i,k]
        if result[2*offset - j,i,k] == 0:
          result[2*offset - j,i,k] = result[2*offset - j+1,i,k]

  return result

def main():
  #val,err = integrate.quad(circle_func, -2,2, args=(2,))
  #print(val)
  img_file = 'angle1.jpg'
  result1 = curve_ext(img_file, 0.46)
  # cv2.imshow('result1', result1)
  # cv2.imwrite('result1.jpg', result1)
  # cv2.waitKey(0)
  # img_file = 'angle2.jpg'
  # result2 = curve_ext(img_file)
  # cv2.imshow('result2', result2)
  # cv2.imwrite('result2.jpg', result2)
  # cv2.waitKey(0)
  # img_file = 'angle3.jpg'
  # result3 = curve_ext(img_file)
  # cv2.imshow('result3', result3)
  # cv2.imwrite('result3.jpg', result3)
  # cv2.waitKey(0)
  # img_file = 'angle4.jpg'
  # result4 = curve_ext(img_file)
  # cv2.imshow('result4', result4)
  # cv2.imwrite('result4.jpg', result4)
  # cv2.waitKey(0)

if __name__ == "__main__":
  main()