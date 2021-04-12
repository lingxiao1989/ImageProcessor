from scipy import integrate
import math
from cv2 import cv2 as cv2
import numpy
import mmcv

class circle_mapping_table:
  def __init__(self,r):
    self.full_table = {}
    self.r = r
    for i in range(self.r+1):
      self.full_table[i]=self._get_table(i)

  def _get_table(self, r):
    current_table={}
    current_table[0]=0
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
    current_table_s = {}
    current_table_l = {}
    current_table_s[0]=0
    for k in range (s):
      t = numpy.arange(0, k, 0.1)
      x = t-s
      y = r * numpy.sqrt(1-(s+l)**2 * x**2/((l-s)*x+2*s*l)**2)
      area_list = []
      area_list = [numpy.sqrt( (x[i]-x[i-1])**2 + (y[i]-y[i-1])**2 ) for i in range(1,len(t))]
      area = sum(area_list)
      current_table_s[s-k] = int(area)
    for m in range (l+1):
      t = numpy.arange(0, m, 0.1)
      x = t
      y = r * numpy.sqrt(1-(s+l)**2 * x**2/((l-s)*x+2*s*l)**2)
      area_list = []
      area_list = [numpy.sqrt( (x[i]-x[i-1])**2 + (y[i]-y[i-1])**2 ) for i in range(1,len(t))]
      area = sum(area_list)
      current_table_l[m] = int(area)

    # for i in range (s):
    #   val,err = integrate.quad(
    #     lambda x, r, s, l: math.sqrt(1 + (r * math.sqrt(1 - (s + l)**2 * x**2/(2*s*l + x*(l - s))**2 ) * (-0.5*(s + l)**2 * x**2 * (-2*l + 2*s)/(2*s*l + x*(l - s))**3 - (s + l)**2*x/(2*s*l + x*(l - s))**2))**2),
    #     i-s,0,
    #     args=(r, s, l,))
    #   current_table_s[s-i] = int(val)
    # for j in range (l+1):
    #   val,err = integrate.quad(
    #     lambda x, r, s, l: math.sqrt(1 + (r * math.sqrt(1 - (s + l)**2 * x**2/(2*s*l + x*(l - s))**2 ) * (-0.5*(s + l)**2 * x**2 * (-2*l + 2*s)/(2*s*l + x*(l - s))**3 - (s + l)**2*x/(2*s*l + x*(l - s))**2))**2),
    #     0,j,
    #     args=(r, s, l,))
    #   current_table_l[j] = int(val)
    return current_table_s, current_table_l

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
  print("r:",r)
  print("s:",s)
  print("l:",l)
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
  # print("100long:",x_draft_s[100])
  # print("100short:",x_draft_s[100])
  # print("150long:",x_draft_s[150])
  # print("150short:",x_draft_s[150])
  ## generating the output image.
  offset_y=int(h_out/2)
  offset_x=int(w_out*ratio)  
  for k in range(c):
    #stretch
    for i in range (w):
      for j in range(r):
        x_maps_s = x_draft_s[j]
        x_maps_l = x_draft_l[j]
        y_maps =  y_draft[i]
        if j in y_maps:
          if i<s and s-i in x_maps_s:
            result[offset_y+y_maps[j], offset_x-x_maps_s[s-i], k] = img[int(h/2)+j, i, k]
            result[offset_y-y_maps[j], offset_x-x_maps_s[s-i], k] = img[int(h/2)-j, i, k]
          elif i-s in x_maps_l:
            result[offset_y+y_maps[j], offset_x+x_maps_l[i-s], k] = img[int(h/2)+j, i, k]
            result[offset_y-y_maps[j], offset_x+x_maps_l[i-s], k] = img[int(h/2)-j, i, k]
    #fill in
    for i in range (w_out):
      for j in range (2, offset_y):
        if result[j,i,k] == 0:
          result[j,i,k] = result[j-1,i,k]
        if result[2*offset_y - j,i,k] == 0:
          result[2*offset_y - j,i,k] = result[2*offset_y - j+1,i,k]

    for i in range (offset_x):
      for j in range (2, offset_y):
        if result[j,i,k] == 0:
          result[j,i,k] = result[j,i+1,k]
        if result[2*offset_y - j,i,k] == 0:
          result[2*offset_y - j,i,k] = result[2*offset_y - j,i+1,k]

    for i in range (w_out, offset_x):
      for j in range (2, offset_y):
        if result[j,i,k] == 0:
          result[j,i,k] = result[j,i-1,k]
        if result[2*offset_y - j,i,k] == 0:
          result[2*offset_y - j,i,k] = result[2*offset_y - j,i-1,k]
  return result

def curve_ext(r,s,l):
  correlations = oval_func(r, s, l)
  lengths={}
  max_length = 0
  for i in range h:
    length = 2*3.1415*correlations.get_y(x)
    lengths[i] = length
    if length > max_length:
      max_length = length
  
def main():
  video = mmcv.VideoReader('test.mp4')
  print(len(video))
  for frame in video:
    frame 

if __name__ == "__main__":
  main()