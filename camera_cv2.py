import cv2
import numpy as np
video = cv2.VideoCapture(0)
frames = []

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

#cv2.namedWindow('image_win',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
while True:
    ret, frame = video.read()
    frames.append(frame)
    print(len(frames))
    if not ret:
        # 如果图片没有读取成功
        print("图像获取失败，请按照说明进行问题排查")
        ## 读取失败？问题排查
        # **驱动问题** 有的摄像头可能存在驱动问题，需要安装相关驱动，或者查看摄像头是否有UVC免驱协议
        # **接口兼容性问题** 或者USB2.0接口接了一个USB3.0的摄像头，也是不支持的。
        # **设备挂载问题** 摄像头没有被挂载，如果是虚拟机需要手动勾选设备
        # **硬件问题** 在就是检查一下USB线跟电脑USB接口
        break
    # 更新窗口“image_win”中的图片
    #cv2.imshow('image_win',frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        # 如果按键为q 代表quit 退出程序
        print("程序正常退出")
        break
    # elif key == ord('c'):
    #     ## 如果c键按下，则进行图片保存
    #     # 写入图片 并命名图片为 图片序号.png
    #     cv2.imwrite("{}.png".format(img_count), frame)
    #     print("截图，并保存为  {}.png".format(img_count))
    #     # 图片编号计数自增1
    #     img_count += 1
pic=frames[0]
h,w,c=pic.shape
h_out = int(h*pi/2)
w_out = int(w*pi/2)
correlations = oval_func(r, s, l)
lengths={}
values={}
max_length = 0
for i in range (h):
    length = 2*3.1415*correlations.get_y(i)
    lengths[i] = length
    values[i] = {}
    if length > max_length:
        max_length = length
result = numpy.zeros((h_out,w_out,c),numpy.uint8)

value={}
for j in len(frames):
    for i in range(h):
        if i%max_length/lengths[i] is 0:
            img=frames[j]
            values[i].append(img[h,w/2,c])

for i in range(h):
    result[h,w,c] = values[i]

    
max_length/lengths[i]
video.release()
# 销毁所有的窗口
#cv2.destroyAllWindows()

