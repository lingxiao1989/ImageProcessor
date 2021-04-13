from scipy import integrate
import math
from cv2 import cv2 as cv2
import numpy
import mmcv
from PIL import Image

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

# def curve_ext(r,s,l):
#   correlations = oval_func(r, s, l)
#   lengths={}
#   max_length = 0
#   for i in range h:
#     length = 2*3.1415*correlations.get_y(x)
#     lengths[i] = length
#     if length > max_length:
#       max_length = length
  
def main():
  #setup input
  video = mmcv.VideoReader('eggroll_color.mp4')
  frame_size=len(video)
  #frame=video[0]
  print(frame_size)
  #cv2.imwrite('video_result.jpg', frame[30:368,128:548,])
  #init
  pi=3.1415
  left=128
  right=548
  l=360-128
  s=548-360
  r=int((368-30)/2)
  correlations = oval_func(r, s, l)
  h_out = int(338*pi)
  w_out = int(420*pi)
  #get egg shape
  lengths={}
  values_r={}
  values_g={}
  values_b={}
  max_length = 0
  for i in range (s+l+1):
    length = int(2*3.1415*correlations.get_y(i))
    lengths[i] = length
    values_r[i] = []
    values_g[i] = []
    values_b[i] = []
    if length > max_length:
      max_length = length
  print(lengths)
  #get value from frames
  result = numpy.zeros((h_out,w_out,3),numpy.uint8)
  value={}
  for j in range(frame_size):
    frame=video[j]
    target=frame[30:368,128:548,]
    for i in range (s+l):
      temp=s+l-i
      if j%(max_length/(lengths[temp]+1)) < 1:
        values_r[i].append(target[r,i,0])
        values_g[i].append(target[r,i,1])
        values_b[i].append(target[r,i,2]) 
  print(values_r)
  #generate output
  # print(h_out)
  # print(w_out)  
  for i in range(1,s+l):
    line_r=values_r[i]
    line_g=values_g[i]
    line_b=values_b[i]
    offset = int((max_length-lengths[s+l-i])/4)
    for j in range(len(line_r)):
      result[j+offset,i,0] = line_r[j]
      result[j+offset,i,1] = line_g[j]
      result[j+offset,i,2] = line_b[j]

  cv2.imwrite('video_result.jpg', result)

if __name__ == "__main__":
  main()