from scipy import integrate
import math

def egg_func(x):
  return x

def circle_func(x,r):
  return r * math.sqrt(1/(r**2-x**2))

def main():
  print(integrate.quad(circle_func))
  ##make new empty image.


  ##for iteration to calcaulate mapping point in the original image. Round the float value.


  ##return the new image.



if __name__ == "__main__":
  main()
